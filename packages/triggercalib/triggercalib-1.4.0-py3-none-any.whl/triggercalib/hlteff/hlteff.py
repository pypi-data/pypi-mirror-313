###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

from hepstats.splot import compute_sweights
import numpy as np
import ROOT as R
from uncertainties import ufloat

from array import array
import itertools as it
import json
import logging
import os
import re
from typing import Dict, List, Literal, Union

from .objects import Plot, Sideband
from ..utils import split_paths, tgraph_to_th

HAS_ZFIT = True
try:
    import zfit
except ModuleNotFoundError:
    HAS_ZFIT = False

if HAS_ZFIT:
    observable_type_hint = Union[R.RooAbsReal, zfit.Space]
    pdf_type_hint = Union[R.RooAbsPdf, zfit.pdf.BasePDF]
    from ..utils import create_zfit_dataset, zfit_fit
else:
    observable_type_hint = R.RooAbsReal
    pdf_type_hint = R.RooAbsPdf


class HltEff:
    """Class for calculating trigger efficiencies

    This class provides functionality for calculating trigger efficiencies using
    either RooFit or zFit as the backend. It supports various methods of efficiency
    calculation including direct counting and fitting methods. It also handles
    different trigger categories (TIS, TOS, TISTOS) and provides utilities for
    binning, plotting, and saving results.
    """

    # Magic methods #

    def __init__(  # <- TODO: order the arguments!
        self,
        name: str,
        path: Union[str, List[str]],  # <- TODO: add direct passing of RDataFrame object
        probe: Union[str, List[str]],  # <- line(s) to be used as the probe
        tag: Union[str, List[str]],  # <- line(s) to be used as the tag
        particle: str,
        binning: Union[
            str, Dict[str, Dict[str, Union[List[float], str]]]
        ] = {},  # <- provide binning directly as dict or as path to .json/.yaml file
        cut: Union[str, List[str]] = "",
        observable: observable_type_hint = None,
        pdf: pdf_type_hint = None,
        sideband: Dict[str, List[float]] = None,
        sweights: str = False,
        expert_mode: bool = False,
        lazy: bool = False,
        max_fit_attempts: int = 5,
        plots: bool = True,  # <- TODO: implement central plotting framework
        prefix: str = "",
        output_path: str = "",
        threads: int = 1,
        verbose: bool = False,
    ):
        """Initialize a new HltEff instance

        Args:
            name: Unique identifier for this efficiency calculation
            path: Path(s) to the input data file(s) or RDataFrame, of the form <path>:<tree>
            probe: Trigger selection (line(s)) of interest
            tag: Reference trigger selection used to define the tag sample
            particle: Name of particle chosen as signal
            binning: Binning scheme as dict or path to binning config .json file
            cut: Additional selection criteria to apply to both tag and probe sample
            observable: Variable for fitting, as a RooAbsReal or zfit.Space object
            pdf: Probability density function for fitting, as a RooAbsPdf or zfit.pdf
            sideband: Sideband regions for sideband subtraction
            sweights: Name of coefficient from which corresponding sWeights will be used
            expert_mode: Enable advanced features and controls, and disable convergence checks
            lazy: Defer computation until explicitly requested
            plots: Generate plots when performing fitting
            prefix: Prefix to prepend to names of counts/error TH and TGraph objects
            output_path: Directory to which fit results should be saved
        """

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
        self.logger.info(f"Initialising HltEff object {name}")

        self.name = name
        self.particle = particle

        if isinstance(path, str):
            path = [path]

        self.tree, self.path = split_paths(path, require_same_tree=True)

        self.cut = [cut] if isinstance(cut, str) and len(cut) > 0 else cut
        self.rdf = self._load_rdf()

        self.tag = self._parse_selection(tag, "TIS")
        self.probe = self._parse_selection(probe, "TOS")
        self.selection = self._parse_selection(probe)

        if isinstance(binning, str):
            with open(binning, "r") as binning_file:
                binning = json.load(binning_file)
        self.set_binning(binning)

        self.observable = observable
        self.pdf = pdf
        if bool(observable) != bool(pdf):
            ValueError(
                "If observable is provided, then pdf must also be provided (and vice versa)"
            )
        if pdf is not None or observable is not None:
            if isinstance(pdf, R.RooAbsPdf) and isinstance(observable, R.RooAbsReal):
                self.backend = "roofit"
                if sweights and not (
                    any(sweights == coef.GetName() for coef in pdf.coefList())
                ):
                    raise ValueError(
                        f"Yield '{sweights}' could not be found in '{pdf}'"
                    )

            elif (
                HAS_ZFIT
                and isinstance(pdf, zfit.pdf.BasePDF)
                and isinstance(observable, zfit.Space)
            ):
                self.backend = "zfit"
                if sweights and not (
                    any(sweights == component.extended.name for component in pdf.pdfs)
                ):
                    raise ValueError(
                        f"Yield '{sweights}' could not be found in '{pdf}'"
                    )
            else:
                raise ValueError(
                    "Unsupported combination of 'observable' and 'pdf' arguments. These must be either both RooFit objects or both zFit objects."
                )

        self.sweights = sweights

        self.output_path = output_path
        if output_path:
            os.makedirs(output_path, exist_ok=True)

        self.fit_path = os.path.join(output_path, "fits")
        os.makedirs(self.fit_path, exist_ok=True)

        self.plot_path = os.path.join(output_path, "plots") if plots else None
        if self.plot_path:
            os.makedirs(self.plot_path, exist_ok=True)

        self.threads = threads
        self.expert_mode = expert_mode
        self.max_fit_attempts = max_fit_attempts

        self.method = "raw"

        if bool(sideband) and bool(pdf):
            ValueError("Sideband and fit model cannot both be provided")

        self._min_entries_for_fit = 50  # <- TODO: configure this from an argument

        if sideband:
            if len(sideband.keys()) != 1:
                ValueError("Sideband should be provided as a single-entry dictionary")
            self.method = "sideband"
            sideband_var = list(sideband.keys())[0]
            sideband_range = sideband[sideband_var]
            if "range" not in sideband_range or "sideband" not in sideband_range:
                raise RuntimeError(
                    "Sideband must be specified with 'range' and 'sideband' entries"
                )
            if (
                "signal" not in sideband_range
            ):  # If no signal range given, assume that the range between the sidebands is the signal range
                sideband_range["signal"] = sideband_range["sideband"]

            self.sideband = Sideband(
                sideband_var,
                sideband_range["range"],
                sideband_range["sideband"],
                sideband_range["signal"],
            )
            self.logger.info(f"Count mode '{self.method}' chosen")
        else:
            self.sideband = None
            if pdf:
                self.method = "sweights" if self.sweights else "fit_count"
                self.logger.info(f"Count mode '{self.method}' chosen")
            else:
                if not expert_mode:
                    raise RuntimeError(
                        "Expert mode must be enabled to use 'raw' count mode"
                    )

        self.verbose = verbose
        if lazy:
            self._counts = {}
            self._efficiencies = {}
            self._sweights = {}
        else:
            if not self.binning:
                raise RuntimeError(
                    "Binning must be provided at initialisation unless running in lazy mode, i.e. lazy = True"
                )
            self.counts(prefix)
            self.efficiencies(prefix)

    def __getitem__(self, key):

        if key not in ("counts", "efficiencies"):
            raise ValueError("Can only obtain 'counts' or 'efficiencies' objects")
        if key == "counts":
            return self._counts
        return self._efficiencies

    def get_count(self, name):
        if name not in self._counts:
            raise KeyError(f"Count '{name}' not found in counts")
        return self._counts[name]

    def get_eff(self, name: str, as_th: bool = False):
        if name not in self._efficiencies:
            raise KeyError(f"Efficiency '{name}' not found in efficiencies")
        _eff = self._efficiencies[name]

        if as_th:
            self.logger.info(
                "Conversion of efficiency from TGraph(2D)AsymErrors will combine asymmetric errors"
            )
            return tgraph_to_th(_eff, name=name)

        return _eff

    def set_binning(
        self,
        scheme: Dict[str, Union[List[float], float, str]],
        compute_bins: bool = False,
        bin_cut: Union[
            str, List[str]
        ] = "",  # Only applied when binning is being generated (i.e., scheme["bins"] is not a Dict)
    ):

        if any("bins" not in entry for entry in scheme.values()):
            raise ValueError("Binning scheme does not contain argument 'bins'")
        if compute_bins:
            self.binning_scheme = {}
            # Compute bins if a list of bins is given instead of the bins themselves
            rdf = self.rdf

            if bin_cut and len(bin_cut) > 0:
                if isinstance(bin_cut, str):
                    bin_cut = [bin_cut]
                for bin_cut_i in bin_cut:
                    rdf = rdf.Filter(bin_cut_i)

            # Before computing bins, apply cuts on each dimension
            for var, entry in scheme.items():
                if isinstance(entry["bins"], List):
                    _, lower, upper = entry["bins"]
                    rdf = rdf.Filter(f"({var} > {lower}) & ({var} < {upper})")

            df = rdf.AsNumpy((var for var in scheme.keys()))
            for var, entry in scheme.items():
                if isinstance(entry["bins"], float):
                    nbins = entry["bins"]
                    lower = np.min(df[var])
                    upper = np.max(df[var])
                else:
                    nbins, lower, upper = entry["bins"]

                edges = np.quantile(df[var], np.arange(1, nbins) / nbins)
                edges = np.append((lower,), np.append(edges, (upper,)))
                self.binning_scheme[var] = {
                    "bins": list(edges),
                    "label": entry["label"] if "label" in scheme else var,
                }

            self.set_binning(self.binning_scheme)
        else:
            self.binning_scheme = scheme
            self.binning = {
                var: entry["bins"] for var, entry in self.binning_scheme.items()
            }
            if any(
                bins[n + 1] <= bins[n]
                for bins in self.binning.values()
                for n in range(len(bins) - 1)
            ):
                raise ValueError("Bins must be increasing")
            self.variables = {
                var: entry["label"] if "label" in entry else var
                for var, entry in self.binning_scheme.items()
            }
            self.midpoints = [
                (np.array(axis_bins[1:]) + np.array(axis_bins[:-1])) / 2
                for axis_bins in self.binning.values()
            ]
            self.nbins = np.prod([len(b) for b in self.midpoints])

        self.logger.info(
            f"Binning scheme set for variables '{', '.join(self.variables.keys())}'"
        )

        for variable, bins in self.binning.items():
            self.rdf = self.rdf.Filter(
                f"{variable} > {bins[0]} && {variable} < {bins[-1]}"
            )

    def counts(self, prefix=""):

        self._counts = {}
        if not self.binning or not self.path or not self.tree:
            raise ValueError(
                "Path, tree and binning must all be set before calculating counts"
            )

        self._counts = {}
        prefix = f"{prefix}_" if prefix else ""

        if self.method == "fit_count":  # <- TODO: require fit model
            _counts = self._fit_count(prefix)
        else:
            _counts = self._hist_count(prefix)

        for category in ("tis", "tos"):
            category_name = (
                f"{prefix}{category}_only_count_{'_'.join(self.variables.keys())}"
            )
            _counts[category_name] = _counts[
                f"{prefix}{category}_count_{'_'.join(self.variables.keys())}"
            ].Clone(category_name)
            _counts[category_name].SetTitle(category_name)
            _counts[category_name].Add(
                _counts[f"{prefix}tistos_count_{'_'.join(self.variables.keys())}"], -1
            )

        for count_label, count_hist in dict(_counts).items():
            if self._to_project(count_label):
                _counts[
                    count_label.replace(
                        "_".join(self.variables.keys()), list(self.variables.keys())[0]
                    )
                ] = count_hist.ProjectionX()
                _counts[
                    count_label.replace(
                        "_".join(self.variables.keys()), list(self.variables.keys())[1]
                    )
                ] = count_hist.ProjectionY()

        self._counts = _counts
        return self._counts

    def efficiencies(self, prefix=""):

        self.logger.info("Calculating TIS, TOS and Trig efficiencies")

        self._efficiencies = {}
        _counts = self._counts
        prefix = f"{prefix}_" if prefix else ""

        _efficiencies = {}
        axes = [None, 0, 1]
        suffixes = (
            [
                "_".join(self.variables.keys()),
                list(self.variables.keys())[0],
                list(self.variables.keys())[1],
            ]
            if len(self.variables.keys()) > 1
            else ["_".join(self.variables.keys())]
        )

        # <- TODO: Condense this iteration?
        for axis, suffix in zip(axes, suffixes):
            for total in ("", "total_"):
                for efficiency_category, denominator_category in zip(
                    ("tos", "tis"), ("tis", "tos")
                ):
                    _efficiencies[
                        f"{prefix}{efficiency_category}_{total}efficiency_{suffix}"
                    ] = self._base_efficiency(
                        f"{prefix}{efficiency_category}_{total}efficiency_{suffix}",
                        _counts[f"{prefix}tistos_count_{suffix}"],
                        _counts[f"{prefix}{denominator_category}_count_{suffix}"],
                        axis=axis,
                        integrated=bool(total),
                    )

                _efficiencies[f"{prefix}trig_{total}efficiency_{suffix}"] = (
                    self._trigger_efficiency(
                        f"{prefix}trig_{total}efficiency_{suffix}",
                        _counts[f"{prefix}trig_count_{suffix}"],
                        _counts[f"{prefix}tistos_count_{suffix}"],
                        _counts[f"{prefix}tis_count_{suffix}"],
                        _counts[f"{prefix}tos_count_{suffix}"],
                        _counts[f"{prefix}tis_only_count_{suffix}"],
                        _counts[f"{prefix}tos_only_count_{suffix}"],
                        axis=axis,
                        integrated=bool(total),
                    )
                )

        self._efficiencies = _efficiencies
        return self._efficiencies

    def write(self, path, mode="RECREATE", prefix=""):
        if not path.endswith(".root"):
            raise ValueError("Path to write HltEff output to must end with '.root'")
        prefix = f"{prefix}_" if prefix else ""
        if "/" in path and not os.path.exists(path.rsplit("/", 1)[0]):
            os.makedirs(path.rsplit("/", 1)[0])

        output_file = R.TFile.Open(path, mode)
        _results = {
            f"{prefix}counts": self._counts,
            f"{prefix}efficiencies": self._efficiencies,
        }
        for name, results in _results.items():
            if results:
                output_dir = output_file.mkdir(name)
                output_dir.cd()
                for key, hist in results.items():
                    hist.Write(key)

        output_file.Close()

    def write_bins(self, path):
        if self.binning_scheme:
            if "/" in path:
                os.makedirs(path.rsplit("/", 1)[0], exist_ok=True)
            with open(path, "w") as output_file:
                json.dump(
                    self.binning_scheme,
                    output_file,
                    indent=4,
                )
            return
        raise RuntimeError("Binning scheme has not been set")

    def _load_rdf(self):
        """Create and store ROOT RDataFrame object from the input files

        Returns:
            RDataFrame: Loaded data with any specified cuts applied
        """
        self.logger.info(
            f"Creating RDF from tree '{self.tree}' in path(s) '{self.path}'"
        )
        rdf = R.RDataFrame(self.tree, self.path)
        if self.cut and len(self.cut) > 0:
            for cut in self.cut:
                rdf = rdf.Filter(cut)
        return rdf

    def _parse_selection(
        self, selection: Union[str, List[str]], category: Literal["", "TIS", "TOS"] = ""
    ):
        """Parse trigger selection strings into ROOT cut expressions

        Args:
            selection: Trigger line(s) to create selection for
            category: Optional trigger outcome category (TIS/TOS) to append

        Returns:
            str: ROOT cut expression combining the selections
        """

        if isinstance(selection, str):
            # Inspired by equivalent in HltEfficiencyChecker: https://gitlab.cern.ch/lhcb/DaVinci/-/blob/edc0bc4860643dc82c7c9b84828a4208426d9f15/HltEfficiencyChecker/python/HltEfficiencyChecker/config.py#L71-L72

            branches = {str(branch) for branch in self.rdf.GetColumnNames()}
            search = re.compile(f"{selection}Decision")
            selection = [
                branch.replace("Decision", "")
                for branch in branches
                if search.fullmatch(branch)
            ]

            if category:
                for line in selection:
                    if f"{self.particle}_{line}Decision_{category}" not in branches:
                        raise KeyError(
                            f"Branch '{self.particle}_{line}Decision_{category}' could not be found"
                        )

        selection.sort()

        cuts = []
        for level in ("Hlt1", "Hlt2"):
            cut = " || ".join(
                (
                    f"{self.particle}_{line}Decision_{category}"
                    if category
                    else f"{line}Decision"
                )
                for line in selection
                if line.startswith(level)
            )
            if cut:
                cuts += [f"({cut})"]

        return " && ".join(cuts)

    def _empty_histogram(self, name, binning=None):
        """Create an empty ROOT.TH1D with specified binning scheme

        Args:
            name: Name for the histogram
            binning: Optional custom binning scheme

        Returns:
            TH1D or TH2D: Empty histogram with appropriate binning
        """
        if not (binning):
            binning = self.binning

        bin_vars = list(binning.keys())
        if len(bin_vars) == 1:
            return R.TH1D(
                name,
                name,
                len(binning[bin_vars[0]]) - 1,
                array("d", binning[bin_vars[0]]),
            )
        elif len(bin_vars) == 2:
            return R.TH2D(
                name,
                name,
                len(binning[bin_vars[0]]) - 1,
                array("d", binning[bin_vars[0]]),
                len(binning[bin_vars[1]]) - 1,
                array("d", binning[bin_vars[1]]),
            )
        raise RuntimeError("Calculations can only be performed in 1D or 2D")

    def _rdf_histo(self, rdf, name, weight="", binning=None):
        """Create a histogram from a branch in a given RDataFrame object

        Args:
            rdf: Input RDataFrame
            name: Name for the histogram
            weight: Optional weight branch
            binning: Optional binning scheme

        Returns:
            Pointer to booked RDataFrame histogram (1D or 2D)
        """
        if not (binning):
            binning = self.binning

        bin_vars = list(binning.keys())

        if len(bin_vars) == 1:
            args = [
                (
                    name,
                    name,
                    len(binning[bin_vars[0]]) - 1,
                    array("d", binning[bin_vars[0]]),
                ),
                bin_vars[0],
            ]
            if weight:
                args += [weight]

            return rdf.Histo1D(*args)
        elif len(bin_vars) == 2:
            args = [
                (
                    name,
                    name,
                    len(binning[bin_vars[0]]) - 1,
                    array("d", binning[bin_vars[0]]),
                    len(binning[bin_vars[1]]) - 1,
                    array("d", binning[bin_vars[1]]),
                ),
                bin_vars[0],
                bin_vars[1],
            ]
            if weight:
                args += [weight]

            return rdf.Histo2D(*args)
        raise RuntimeError("Calculations can only be performed in 1D or 2D")

    def _trigger_cut(self, category):
        """Obtain ROOT cut string for a trigger outcome category

        Args:
            category: One of 'tis', 'tos', 'tistos', or 'trig'

        Returns:
            str: ROOT cut expression for the specified trigger outcome category

        Raises:
            ValueError: If category is not one of the allowed values
        """
        if category not in ("tis", "tos", "tistos", "trig"):
            ValueError("Category must be one of 'tis', 'tos', 'tistos' or 'trig'")

        if category == "tis":
            return self.tag
        elif category == "tos":
            return self.probe
        elif category == "tistos":
            return f"({self.tag}) && ({self.probe})"
        return self.selection

    def _to_project(self, label, bin_requirement=True, include_mass=True):
        """Check if a histogram should be projected, based on its label

        Args:
            label: Histogram label to check
            bin_requirement: Whether to require binning variables
            include_mass: Whether to include mass in the check

        Returns:
            bool: True if the histogram should be projected
        """
        test_parts = [f"_{var}" for var in self.variables.keys()]
        if include_mass:
            test_parts += ["mass"]
        return (len(self.variables.keys()) > 1 or not bin_requirement) and not any(
            l in label and "_".join(self.variables.keys()) not in label
            for l in test_parts
        )

    def _run_fit(self, pdf, data):
        """Run a fit using either RooFit or zFit backend

        Args:
            pdf: PDF to fit (RooAbsPdf or zfit.pdf)
            data: Data to fit to (RooDataSet or zfit.Data)

        Returns:
            Fit result object from the respective backend

        Raises:
            RuntimeError: If fit does not converge (if expert_mode is not set)
        """
        attempts = 1
        max_attempts = self.max_fit_attempts

        converged = False
        while attempts < max_attempts:
            attempts += 1

            if self.backend == "roofit":
                fit_result = pdf.fitTo(
                    data,
                    Extended=True,
                    NumCPU=self.threads,
                    Save=True,
                    PrintLevel=1 if self.verbose else 0,
                )
                converged = fit_result.status() == 0 and fit_result.covQual() == 3

            elif self.backend == "zfit":
                nll = zfit.loss.ExtendedUnbinnedNLL(model=pdf, data=data)
                fit_result, converged = zfit_fit(nll)

            if converged:
                break

            if not self.expert_mode:
                raise RuntimeError(
                    "Fit did not converge, please reconfigure fit and try again"
                )

        return fit_result

    def _fit_count(self, prefix=""):
        """Perform fit-based counting of events to fill histograms

        Args:
            prefix: Optional prefix for histogram names

        Returns:
            dict: Dictionary of histograms containing fit yields for different trigger outcome categories
        """
        rdf = self.rdf
        if self.backend == "roofit":
            pdfs = {}

        dataset_ptrs = {}
        _counts = {}
        for category in ("tis", "tos", "tistos", "trig", "sel"):
            _counts[f"{prefix}{category}_count_{'_'.join(self.variables.keys())}"] = (
                self._empty_histogram(
                    f"{prefix}{category}_count_{'_'.join(self.variables.keys())}"
                )
            )

            count_rdf = (
                rdf.Filter(self._trigger_cut(category)) if category != "sel" else rdf
            )

            for midpoint_coords in it.product(*self.midpoints):
                xaxis = _counts[
                    f"{prefix}{category}_count_{'_'.join(self.variables.keys())}"
                ].GetXaxis()
                xbin = xaxis.FindBin(midpoint_coords[0])
                x_low = xaxis.GetBinLowEdge(xbin)
                x_up = xaxis.GetBinUpEdge(xbin)

                bin_cut = f"({list(self.variables.keys())[0]}>{x_low} && {list(self.variables.keys())[0]}<{x_up})"
                dataset_name = f"{prefix}{category}_dataset_bin_{xbin}"

                if len(midpoint_coords) > 1:
                    yaxis = _counts[
                        f"{prefix}{category}_count_{'_'.join(self.variables)}"
                    ].GetYaxis()
                    ybin = yaxis.FindBin(midpoint_coords[1])
                    y_low = yaxis.GetBinLowEdge(ybin)
                    y_up = yaxis.GetBinUpEdge(ybin)

                    bin_cut = f"{bin_cut} && ({list(self.variables.keys())[1]} > {y_low} && {list(self.variables.keys())[1]} < {y_up})"
                    dataset_name = f"{dataset_name}_{ybin}"

                bin_rdf = count_rdf.Filter(bin_cut)

                if self.backend == "roofit":
                    obs_list = [self.observable.GetName()]

                    pdf_name = dataset_name.replace("_dataset_", "_pdf_")
                    pdfs[pdf_name] = self.pdf.cloneTree(pdf_name)
                    R.SetOwnership(pdfs[pdf_name], False)

                elif self.backend == "zfit":
                    obs_list = [self.observable.obs[0]]
                dataset_ptrs[dataset_name] = bin_rdf.AsNumpy(obs_list, lazy=True)

        results = {}
        for category in ("tis", "tos", "tistos", "trig", "sel"):
            hist = _counts[f"{prefix}{category}_count_{'_'.join(self.variables)}"]

            for midpoint_coords in it.product(*self.midpoints):
                nbin = hist.FindBin(*midpoint_coords)
                xaxis = hist.GetXaxis()
                xbin = xaxis.FindBin(midpoint_coords[0])
                dataset_name = f"{prefix}{category}_dataset_bin_{xbin}"
                if len(midpoint_coords) > 1:
                    yaxis = hist.GetYaxis()
                    ybin = yaxis.FindBin(midpoint_coords[1])
                    dataset_name = f"{dataset_name}_{ybin}"

                if self.backend == "roofit":
                    data = R.RooDataSet.from_numpy(
                        dataset_ptrs[dataset_name].GetValue(), [self.observable]
                    )

                    pdf = pdfs[dataset_name.replace("_dataset_", "_pdf_")]
                elif self.backend == "zfit":
                    data = create_zfit_dataset(
                        dataset_ptrs[dataset_name].GetValue(), self.observable
                    )
                    pdf = self.pdf
                fit_result = self._run_fit(pdf, data)
                results[dataset_name.replace("_dataset_", "_result_")] = fit_result

                with open(
                    os.path.join(
                        self.fit_path,
                        dataset_name.replace("_dataset_", "_") + "_fit.txt",
                    ),
                    "w",
                ) as result_file:
                    if self.backend == "roofit":
                        if self.verbose:
                            print(f"Fit result for {category} bin {nbin}")
                            for var in fit_result.floatParsFinal():
                                result_file.write(
                                    f"{var.GetName()}: {var.getVal()} +/- {var.getError()}\n"
                                )
                            print()
                        result_file.write("\n\n")
                        result_file.write(
                            f"Covariance quality: {fit_result.covQual()}\n"
                        )
                        result_file.write(f"Fit status: {fit_result.status()}\n")
                    if self.backend == "zfit":
                        if self.verbose:
                            print(f"Fit result for {category} bin {nbin}")
                            for param, param_info in fit_result.params.items():
                                print(
                                    f"{param.name}: {param_info['value']} +/- {param_info['hesse']['error']}"
                                )
                            print()
                        result_file.write("\n\n")
                        result_file.write(f"Converged: {fit_result.converged}\n")
                        result_file.write(f"Minimum value: {fit_result.fmin}\n")
                if self.plot_path:
                    plot_name = dataset_name.replace("_dataset_", "_").replace(
                        ".root", "_plot"
                    )

                    plot = Plot(
                        plot_name, self.observable, data, pdf, backend=self.backend
                    )
                    plot.save(self.plot_path)

                if self.backend == "roofit":
                    pdf_yields = {coef.GetName(): coef for coef in pdf.coefList()}
                elif self.backend == "zfit":
                    pdf_yields = {
                        component.extended.name: fit_result.params[
                            component.extended.name
                        ]
                        for component in self.pdf.pdfs
                    }

                for coef_name, coef in pdf_yields.items():
                    count_name = f"{prefix}{category}_{coef_name}_count_{'_'.join(self.variables)}"
                    if (
                        f"{prefix}{category}_{coef_name}_count_{'_'.join(self.variables)}"
                        not in _counts
                    ):
                        _counts[count_name] = hist.Clone(count_name)
                        _counts[count_name].SetTitle(count_name)
                    temp_hist = _counts[count_name]
                    if self.backend == "roofit":
                        temp_hist.SetBinContent(nbin, coef.getVal())
                        temp_hist.SetBinError(
                            nbin, np.abs(coef.getPropagatedError(fit_result))
                        )
                    elif self.backend == "zfit":
                        temp_hist.SetBinContent(nbin, coef["value"])
                        temp_hist.SetBinError(nbin, np.abs(coef["hesse"]["error"]))

                signal_count = list(pdf_yields.values())[0]
                if self.backend == "roofit":
                    hist.SetBinContent(nbin, signal_count.getVal())
                    hist.SetBinError(nbin, np.abs(signal_count.getError()))
                elif self.backend == "zfit":
                    hist.SetBinContent(nbin, signal_count["value"])
                    hist.SetBinError(nbin, np.abs(signal_count["hesse"]["error"]))

        for category in ("tis", "tos"):
            category_name = f"{prefix}{category}_only_count_{'_'.join(self.variables)}"
            _counts[category_name] = _counts[
                f"{prefix}{category}_count_{'_'.join(self.variables)}"
            ].Clone(category_name)
            _counts[category_name].SetTitle(category_name)
            _counts[category_name].Add(
                _counts[f"{prefix}tistos_count_{'_'.join(self.variables)}"], -1
            )

        return _counts

    def _calculate_sweights(self, rdf, prefix=""):
        """Calculate sWeights for background mitigation

        Args:
            rdf: Input RDataFrame
            prefix: Optional prefix for output names

        Returns:
            dict: Dictionary containing sWeights for each trigger outcome category
        """
        dataset_ptrs = {}
        pdfs = {}

        if self.backend == "roofit":

            observables = [
                self.observable,
            ] + [
                R.RooRealVar(var, var, bins[0], bins[-1])
                for var, bins in self.binning.items()
            ]

            obs_list = [obs.GetName() for obs in observables]
        elif self.backend == "zfit":
            obs_list = [self.observable.obs[0]] + list(self.binning.keys())

        for category in ("tis", "tos", "tistos", "trig", "sel"):
            category_rdf = (
                rdf.Filter(self._trigger_cut(category)) if category != "sel" else rdf
            )

            if self.backend == "roofit":
                pdf_name = f"{prefix}{category}_pdf"
                pdfs[pdf_name] = self.pdf.cloneTree(pdf_name)

            dataset_name = f"{prefix}{category}_dataset"
            dataset_ptrs[dataset_name] = category_rdf.AsNumpy(obs_list, lazy=True)

        sweight_path = os.path.join(self.output_path, "sweighted_data.root")
        sweight_trees = {}
        # <- TODO: There's probably a nice way to refactor all of this
        if self.backend == "roofit":
            for category in ("tis", "tos", "tistos", "trig", "sel"):

                data = R.RooDataSet.from_numpy(
                    dataset_ptrs[f"{prefix}{category}_dataset"].GetValue(), observables
                )
                pdf = pdfs[f"{prefix}{category}_pdf"]

                if data.sumEntries() <= self._min_entries_for_fit:
                    raise RuntimeError(
                        f"Insufficient events in the '{category}' category to perform sWeight fit"
                    )
                fit_result = self._run_fit(pdf, data)

                with open(
                    os.path.join(
                        self.fit_path,
                        f"{prefix}{category}_fit.txt",
                    ),
                    "w",
                ) as result_file:
                    for var in fit_result.floatParsFinal():
                        result_file.write(
                            f"{var.GetName()}: {var.getVal()} +/- {var.getError()}\n"
                        )
                    result_file.write("\n\n")
                    result_file.write(f"Covariance quality: {fit_result.covQual()}\n")
                    result_file.write(f"Fit status: {fit_result.status()}\n")

                if self.plot_path:
                    plot_name = f"{prefix}{category}_plot"

                    plot = Plot(
                        plot_name, self.observable, data, pdf, backend=self.backend
                    )
                    plot.save(self.plot_path)

                splot = R.RooStats.SPlot(
                    f"{prefix}{category}_sdata",
                    f"{prefix}{category}_sdata",
                    data,
                    pdf,
                    pdf.coefList(),
                )
                sdata = splot.GetSDataSet()
                sweight_trees[category] = sdata.GetClonedTree()
                sweight_trees[category].SetName(
                    f"{prefix}{category.capitalize()}DecayTree"
                )

            with R.TFile.Open(sweight_path, "RECREATE") as sweight_file:
                sweight_file.cd()
                for category in ("tis", "tos", "tistos", "trig", "sel"):
                    sweight_trees[category].Write()

            return sweight_path

        elif self.backend == "zfit":

            sweight_trees = {}
            for category in ("tis", "tos", "tistos", "trig", "sel"):

                data = create_zfit_dataset(
                    dataset_ptrs[f"{prefix}{category}_dataset"].GetValue(),
                    self.observable,
                    extra_observables=obs_list,
                )
                pdf = self.pdf

                if len(data.value().numpy()) <= self._min_entries_for_fit:
                    RuntimeError(
                        f"Insufficient events in the '{category}' category to perform sWeight fit"
                    )
                fit_result = self._run_fit(pdf, data)

                with open(
                    os.path.join(
                        self.fit_path,
                        f"{prefix}{category}_fit.txt",
                    ),
                    "w",
                ) as result_file:
                    for param, param_info in fit_result.params.items():
                        print(
                            f"{param.name}: {param_info['value']} +/- {param_info['hesse']['error']}"
                        )
                    result_file.write("\n\n")
                    result_file.write(f"Converged: {fit_result.valid}\n")
                    result_file.write(f"Minimum value: {fit_result.fmin}\n")

                if self.plot_path:
                    plot_name = f"{prefix}{category}_plot"

                    plot = Plot(
                        plot_name, self.observable, data, pdf, backend=self.backend
                    )
                    plot.save(self.plot_path)

                # Compute sWeights using hepstats.splot
                sweights = compute_sweights(pdf, data)

                weights = None
                for sweight_var, sweight_data in sweights.items():
                    if sweight_var.name == self.sweights:
                        weights = np.ndarray(
                            (len(sweight_data),), buffer=np.array(sweight_data)
                        )
                        break

                if weights is None:
                    raise RuntimeError(
                        f"Could not identify sWeights '{self.sweights}'."
                    )

                sweight_trees[category] = data.with_weights(weights)

            rdf_opts = R.RDF.RSnapshotOptions()
            rdf_opts.fMode = "UPDATE"
            rdf_opts.fOverwriteIfExists = True
            for category in ("tis", "tos", "tistos", "trig", "sel"):
                dataset = sweight_trees[category]
                data_df = dataset.to_pandas()
                data_dict = {
                    key if key else f"{self.sweights}_sw": data_df[key].to_numpy()
                    for key in data_df.columns
                }

                rdf = R.RDF.FromNumpy(data_dict)
                rdf.Snapshot(
                    f"{prefix}{category.capitalize()}DecayTree",
                    str(sweight_path),
                    "",
                    rdf_opts,
                )

            return sweight_path

    def _hist_count(self, prefix=""):
        """Perform direct counting of events to fill histograms

        Args:
            prefix: Optional prefix for histogram names

        Returns:
            dict: Dictionary of histograms containing counts for different trigger outcome categories
        """
        rdf = self.rdf
        ptrs = {}

        if self.sweights:
            sweight_path = self._calculate_sweights(rdf, prefix=prefix)

        for category in ("tis", "tos", "tistos", "trig", "sel"):
            if self.sweights:
                _count_rdf = R.RDataFrame(
                    f"{prefix}{category.capitalize()}DecayTree", sweight_path
                )
            else:
                _count_rdf = (
                    rdf.Filter(self._trigger_cut(category))
                    if category != "sel"
                    else rdf
                )

            if self.sideband:  # <- TODO make loop over cuts
                mass_binning = {
                    self.sideband.variable: np.linspace(
                        self.sideband.range[0], self.sideband.range[1], 200
                    )
                }
                for cut_label, cut in zip(
                    ("all", "signal", "sideband"),
                    (
                        self.sideband.range_cut(),
                        self.sideband.signal_cut(),
                        self.sideband.sideband_cut(),
                    ),
                ):
                    _temp_rdf = _count_rdf.Filter(cut)
                    ptrs[
                        f"{prefix}{category}_{cut_label}_count_{'_'.join(self.variables)}"
                    ] = self._rdf_histo(
                        _temp_rdf,
                        f"{prefix}{category}_{cut_label}_count_{'_'.join(self.variables)}",
                    )
                    ptrs[f"{prefix}{category}_{cut_label}_mass"] = self._rdf_histo(
                        _temp_rdf,
                        f"{prefix}{category}_{cut_label}_mass",
                        binning=mass_binning,
                    )
            else:
                ptrs[
                    f"{prefix}{category}_unweighted_count_{'_'.join(self.variables)}"
                ] = self._rdf_histo(
                    _count_rdf,
                    f"{prefix}{category}_unweighted_count_{'_'.join(self.variables)}",
                )
                ptrs[f"{prefix}{category}_count_{'_'.join(self.variables)}"] = (
                    self._rdf_histo(
                        _count_rdf,
                        f"{prefix}{category}_count_{'_'.join(self.variables)}",
                        weight=(f"{self.sweights}_sw" if self.sweights else ""),
                    )
                )

        R.RDF.RunGraphs(ptrs.values())

        _counts = {}
        for key, count in ptrs.items():
            hist = count.GetValue()
            _counts[key] = hist
            if self._to_project(key):
                _counts[
                    key.replace(
                        "_".join(self.variables), list(self.variables.keys())[0]
                    )
                ] = hist.ProjectionX()
                _counts[
                    key.replace(
                        "_".join(self.variables), list(self.variables.keys())[1]
                    )
                ] = hist.ProjectionY()

        if self.sideband:
            for key in list(_counts.keys()):
                if (
                    self._to_project(key, bin_requirement=False, include_mass=False)
                    and "_signal_" in key
                ):
                    new_key = key.replace("_signal_", "_")
                    _counts[new_key] = _counts[key].Clone(new_key)
                    _counts[new_key].SetTitle(new_key)

                    _subtract_hist = _counts[
                        key.replace("_signal_", "_sideband_")
                    ].Clone(f"{new_key}_subtract_hist")

                    if "count" in key:
                        _counts[new_key].Add(_subtract_hist, -1 * self.sideband.scale())
                    else:
                        _sideband_count = _counts[
                            key.replace("_signal_", "_sideband_")
                        ].GetEntries()

                        if _subtract_hist.GetNbinsY() > 1:
                            bin_nums = it.product(
                                (
                                    list(range(1, _subtract_hist.GetNbinsX() + 1)),
                                    list(range(1, _subtract_hist.GetNbinsY() + 1)),
                                )
                            )
                        else:
                            bin_nums = zip(
                                list(range(1, _subtract_hist.GetNbinsX() + 1))
                            )

                        for b in bin_nums:
                            n_bin = _subtract_hist.GetBin(*b)
                            if (
                                _subtract_hist.GetBinCenter(n_bin)
                                > self.sideband.signal[0]
                                and _subtract_hist.GetBinCenter(n_bin)
                                < self.sideband.signal[1]
                            ):
                                width = (
                                    _subtract_hist.GetBinWidth(n_bin)
                                    if "count" not in key
                                    else None
                                )
                                _subtract_hist.SetBinContent(
                                    n_bin, _sideband_count * self.sideband.scale(width)
                                )
                            else:
                                _subtract_hist.SetBinContent(n_bin, 0)

                        _counts[new_key].Add(_subtract_hist, -1)

        return _counts

    def _bin_to_ufloat(self, hist, n):
        """Convert histogram bin content and error to uncertainty float

        Args:
            hist: Input histogram
            n: Bin number

        Returns:
            ufloat: Bin content with uncertainty
        """
        return ufloat(hist.GetBinContent(n), hist.GetBinError(n))

    def _calc_eff(self, numerator: float, denominator: float, confidence: float = 0.68):
        # Calculate a single efficiency with Wilson interval method uncertainties

        if denominator > 0:
            eff_value = numerator / denominator
            eff_low = eff_value - R.TEfficiency.Wilson(
                denominator, numerator, confidence, False
            )
            eff_up = (
                R.TEfficiency.Wilson(denominator, numerator, confidence, True)
                - eff_value
            )

            return eff_value, eff_low, eff_up
        return 0, 0, 0

    def _base_efficiency(
        self, name, numerator_hist, denominator_hist, axis=None, integrated=False
    ):
        """Calculate efficiency from two histograms for the TIS or TOS trigger outcome categories

        Args:
            name: Name for the efficiency histogram
            numerator_hist: Histogram of passing events
            denominator_hist: Histogram of total events
            axis: Optional axis to project onto
            integrated: Whether to calculate as an integrated efficiency

        Returns:
            TGraphAsymmErrors or TGraph2DAsymmErrors: Efficiency histogram (in 1D or 2D)
        """
        _is_2D = isinstance(numerator_hist, R.TH2)
        xaxis = numerator_hist.GetXaxis()

        if _is_2D:
            yaxis = numerator_hist.GetYaxis()
            eff = R.TGraph2DAsymmErrors()
        else:
            eff = R.TGraphAsymmErrors()

        if integrated:
            numerator_value = numerator_hist.GetSumOfWeights()
            denominator_value = denominator_hist.GetSumOfWeights()
            if numerator_value > denominator_value:
                self.logger.info(
                    "Bin contains more passing events than total events (efficiency > 1), setting N(passing) to N(total)"
                )
                numerator_value = denominator_value

            eff_value, eff_low, eff_up = self._calc_eff(
                numerator_value, denominator_value
            )

            x_min = xaxis.GetXmin()
            x_max = xaxis.GetXmax()
            x_center = (x_min + x_max) / 2
            x_low = x_center - x_min
            x_up = x_max - x_center

            if _is_2D:
                yaxis = numerator_hist.GetYaxis()
                y_min = yaxis.GetXmin()
                y_max = yaxis.GetXmax()
                y_center = (y_min + y_max) / 2
                y_low = y_center - y_min
                y_up = y_max - y_center

                eff.AddPoint(x_center, y_center, eff_value)
                eff.SetPointError(0, x_low, x_up, y_low, y_up, eff_low, eff_up)
            else:
                eff.AddPoint(x_center, eff_value)
                eff.SetPointError(0, x_low, x_up, eff_low, eff_up)

        else:
            for n, midpoint_coords in enumerate(it.product(*self.midpoints)):
                coords = [midpoint_coords[axis]] if axis else midpoint_coords

                numerator_value = numerator_hist.GetBinContent(
                    numerator_hist.FindBin(*coords)
                )
                denominator_value = denominator_hist.GetBinContent(
                    denominator_hist.FindBin(*coords)
                )
                if numerator_value > denominator_value:
                    self.logger.info(
                        "Bin contains more passing events than total events (efficiency > 1), setting N(passing) to N(total)"
                    )
                    numerator_value = denominator_value

                eff_value, eff_low, eff_up = self._calc_eff(
                    numerator_value, denominator_value
                )

                xbin = xaxis.FindBin(coords[0])
                x_center = xaxis.GetBinCenter(xbin)
                x_low = x_center - xaxis.GetBinLowEdge(xbin)
                x_up = xaxis.GetBinUpEdge(xbin) - x_center

                if _is_2D:
                    ybin = yaxis.FindBin(coords[1])
                    y_center = yaxis.GetBinCenter(ybin)
                    y_low = y_center - yaxis.GetBinLowEdge(ybin)
                    y_up = yaxis.GetBinUpEdge(ybin) - y_center

                    eff.AddPoint(x_center, y_center, eff_value)
                    eff.SetPointError(n, x_low, x_up, y_low, y_up, eff_low, eff_up)
                else:
                    eff.AddPoint(x_center, eff_value)
                    eff.SetPointError(n, x_low, x_up, eff_low, eff_up)

            eff.SetName(name)
            eff.SetTitle(name)

        return eff

    def _trigger_efficiency(
        self,
        name,
        trig_hist,
        tistos_hist,
        tis_hist,
        tos_hist,
        tis_only_hist,
        tos_only_hist,
        axis=None,
        integrated=False,
    ):
        """Calculate the full trigger efficiency

        Args:
            name: Name for the efficiency histogram
            trig_hist: Histogram of 'triggered' category events
            tistos_hist: Histogram of 'TISTOS' category events
            tis_hist: Histogram of 'TIS' category events
            tos_hist: Histogram of 'TOS' category events
            tis_only_hist: Histogram of 'TIS' category-only events
            tos_only_hist: Histogram of 'TOS' category-only events
            axis: Optional axis to project onto
            integrated: Whether to calculate as integrated efficiency

        Returns:
            TGraphAsymmErrors or TGraph2DAsymmErrors: Efficiency histogram (in 1D or 2D)
        """
        # Construct a data-driven N(sel) per bin of N(TIS) * N(TOS) / N(TISTOS), which forms our denominator
        denominator_hist = tis_hist.Clone()

        # Correct the errors on N(sel) to avoid c_double-counting of events
        for midpoint_coords in it.product(*self.midpoints):
            coords = [midpoint_coords[axis]] if axis else midpoint_coords
            n_bin = trig_hist.FindBin(*coords)

            tistos = self._bin_to_ufloat(tistos_hist, n_bin)  # d_i in Equation 11

            tis = self._bin_to_ufloat(tis_hist, n_bin)  # b_i + d_i in Equation 11
            tis_only = self._bin_to_ufloat(tis_only_hist, n_bin)  # b_i in Equation 11

            tos = self._bin_to_ufloat(tos_hist, n_bin)  # c_i + d_i in Equation 11
            tos_only = self._bin_to_ufloat(tos_only_hist, n_bin)  # c_i in Equation 11

            if tistos.n > 0:
                bin_value = tis.n * tos.n / tistos.n
                bin_error = np.sqrt(
                    np.abs(tos.n / tistos.n) ** 2 * tis_only.s**2
                    + np.abs(tis.n / tistos.n) ** 2 * tos_only.s**2
                    + np.abs(1 - tis_only.n * tos_only.n / tistos.n**2) ** 2
                    * tistos.s**2
                )
            else:
                bin_value = 0
                bin_error = 0

            denominator_hist.SetBinContent(n_bin, bin_value)
            denominator_hist.SetBinError(n_bin, bin_error)

        return self._base_efficiency(
            name, trig_hist, denominator_hist, axis=axis, integrated=integrated
        )
