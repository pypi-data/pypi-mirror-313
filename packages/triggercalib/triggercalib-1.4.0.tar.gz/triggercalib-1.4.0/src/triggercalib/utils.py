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

import numpy as np
import ROOT as R

from array import array
from ctypes import c_double
from typing import List, Union

HAS_ZFIT = True
try:
    import zfit
except ModuleNotFoundError:
    HAS_ZFIT = False


def bins_from_taxis(axis, as_array=False):
    """Extract bin edges from a ROOT TAxis object

    Args:
        axis: ROOT TAxis object to extract bins from
        as_array: Whether to return bins as a ROOT array

    Returns:
        list or array: List of bin edges or ROOT array of bin edges
    """
    bins = [axis.GetBinLowEdge(0)] + [
        axis.GetBinUpEdge(i) for i in range(1, axis.GetNbins() + 1)
    ]

    if as_array:
        return array("d", bins)
    return bins


def split_paths(paths: Union[List[str], str], require_same_tree: bool = True):
    """Split ROOT file paths into tree names and file paths

    Args:
        paths: Path(s) to ROOT file(s) of the form <path>:<tree>
        require_same_tree: Whether all paths must reference the same tree

    Returns:
        tuple: Tree name(s) and file path(s)

    Raises:
        ValueError: If require_same_tree is True and different trees are provided
    """
    if isinstance(paths, str):
        paths = [paths]
    split_trees, split_paths = zip(*(reversed(p.rsplit(":", 1)) for p in paths))

    if len(set(split_trees)) == 1 and require_same_tree:
        return split_trees[0], split_paths
    elif not require_same_tree:
        return split_trees, split_paths

    raise ValueError(
        f"Same tree must be provided for all paths. Trees '{split_trees}' were provided."
    )


def tgraph_to_th(graph, name="", title=""):
    """Convert a ROOT TGraph(2D)AsymmErrors to a TH1(2)D

    Args:
        graph: ROOT TGraph(2D)AsymmErrors to convert
        name: Optional name for output histogram
        title: Optional title for output histogram

    Returns:
        TH1D or TH2D: Histogram containing graph points with symmetric errors
    """
    if not name:
        name = graph.GetName()

    if not title:
        title = graph.GetTitle()

    x = c_double(0)
    y = c_double(0)

    xbins = bins_from_taxis(graph.GetXaxis(), as_array=True)

    if isinstance(graph, R.TGraphAsymmErrors):
        hist = R.TH1D(name, title, len(xbins) - 1, xbins)
        for point in range(graph.GetN()):
            graph.GetPoint(point, x, y)
            _bin = hist.FindBin(x)
            hist.SetBinContent(_bin, y)
            hist.SetBinError(_bin, graph.GetErrorY(point))

    elif isinstance(graph, R.TGraph2DAsymmErrors):
        z = c_double(0)

        ybins = bins_from_taxis(graph.GetYaxis(), as_array=True)

        hist = R.TH2D(
            name,
            title,
            len(xbins) - 1,
            xbins,
            len(ybins) - 1,
            ybins,
        )
        for point in range(graph.GetN()):
            graph.GetPoint(point, x, y, z)
            _bin = hist.FindBin(x, y)
            hist.SetBinContent(_bin, z)
            hist.SetBinError(_bin, graph.GetErrorZ(point))
    else:
        raise TypeError(f"Object '{name}' of unrecognised type '{type(graph)}'")

    return hist


if HAS_ZFIT:

    def create_zfit_dataset(data, observable, extra_observables=[]):
        """Create a zfit dataset from numpy data

        Args:
            data: Dictionary of numpy arrays
            observable: zfit Space object defining the observable
            extra_observables: List of additional observables to include

        Returns:
            zfit.Data: Dataset for zfit operations
        """
        spaces = [observable]
        if extra_observables:
            for extra_observable in extra_observables:
                if extra_observable not in spaces and not any(
                    extra_observable == o.obs[0] for o in spaces
                ):
                    if isinstance(extra_observable, str):
                        space = zfit.Space(
                            extra_observable,
                            limits=(
                                np.min(data[extra_observable]),
                                np.max(data[extra_observable]),
                            ),
                        )
                        spaces.append(space)

        spaces = [observable]
        if extra_observables:
            for extra_observable in extra_observables:
                if extra_observable not in spaces and not any(
                    extra_observable == o.obs[0] for o in spaces
                ):
                    if isinstance(extra_observable, str):
                        space = zfit.Space(
                            extra_observable,
                            limits=(
                                np.min(data[extra_observable]),
                                np.max(data[extra_observable]),
                            ),
                        )
                        spaces.append(space)

                    elif isinstance(extra_observables, zfit.Space):
                        spaces.append(extra_observables)

        obs = zfit.dimension.combine_spaces(*spaces)

        np_dataset = np.array(list(data.values())).T
        return zfit.Data.from_numpy(obs=obs, array=np_dataset)

    def zfit_fit(nll):
        """Perform a fit using zfit

        Args:
            nll: Negative log-likelihood to minimize

        Returns:
            tuple: Fit result and convergence status
        """
        minimizer = zfit.minimize.Minuit()
        fit_result = minimizer.minimize(nll)
        fit_result.hesse()
        criterion = minimizer.create_criterion(fit_result.loss, fit_result.params)
        converged = criterion.converged(fit_result)

        return fit_result, converged
