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

from lhcbstyle import LHCbStyle
import matplotlib.pyplot as plt
import mplhep as hep  # Import mplhep for HEP style plotting
import numpy as np
import os
from ROOT import RooAbsPdf, RooAbsReal, RooDataSet, TCanvas
from typing import Annotated, List, Union

HAS_ZFIT = True
try:
    import zfit
except ModuleNotFoundError:
    HAS_ZFIT = False

if HAS_ZFIT:
    observable_type_hint = Union[RooAbsReal, zfit.Space]
    data_type_hint = Union[RooDataSet, zfit.Data]
    pdf_type_hint = Union[RooAbsPdf, zfit.pdf.BasePDF]
else:
    observable_type_hint = RooAbsReal
    data_type_hint = RooDataSet
    pdf_type_hint = RooAbsPdf


class Plot:
    """Class for trigger efficiency plots

    This class provides functionality to create and save plots of fits to discriminating variable,
    supporting both RooFit and zFit backends. It handles the plotting of data and fitted PDFs (with
    their components if relevant), with appropriate styling for LHCb publications.
    """

    def __init__(
        self,
        name: str,
        observable: observable_type_hint,
        data: data_type_hint,
        pdf: pdf_type_hint,
        extension: str = ".pdf",
        backend: str = "roofit",
    ):
        """Initialize a new Plot instance

        Args:
            name: Name of the plot, used to define the filename
            observable: Variable being plotted (RooAbsReal or zfit.Space)
            data: Dataset to plot (RooDataSet or zfit.Data)
            pdf: Probability density function (RooAbsPdf or zfit.pdf.BasePDF)
            extension: File extension for saved plots (default: .pdf)
            backend: Fitting backend to use ('roofit' or 'zfit')
        """

        self.name = name
        self.observable = observable
        self.data = data
        self.pdf = pdf
        self.extension = extension
        self.backend = backend

        if self.backend == "roofit":
            with LHCbStyle():
                self.canvas = TCanvas(self.name)
                self.canvas.cd()

                self.frame = self.observable.frame()
                self.data.plotOn(self.frame)
                if hasattr(self.pdf, "coefList") and callable(
                    getattr(self.pdf, "coefList")
                ):
                    colors = ["r", "g", "b", "o"]

                    for pdf_i, color in zip(self.pdf.pdfList(), colors):
                        self.pdf.plotOn(
                            self.frame,
                            Components=[pdf_i],
                            LineStyle="--",
                            LineColor=color,
                        )
                self.pdf.plotOn(self.frame)

                self.frame.Draw()

        elif self.backend == "zfit":
            if not HAS_ZFIT:
                raise RuntimeError(
                    "zfit is not installed - please either install triggercalib[zfit] or zfit"
                )

            hep.style.use("LHCb2")
            self.fig, self.ax = plt.subplots()

            _, bin_edges, _ = self.ax.hist(
                self.data.value(self.observable).numpy(),
                bins=100,
                density=False,
                label="Data",
                color="black",
                histtype="step",
            )

            pdf_xvals = np.linspace(bin_edges[0], bin_edges[-1], 1000)

            for component in self.pdf.pdfs:
                component_yield = component.get_yield().numpy()
                component_yvals = (
                    component.pdf(pdf_xvals)
                    * component_yield
                    * (bin_edges[1] - bin_edges[0])
                )
                self.ax.plot(
                    pdf_xvals, component_yvals, label=component.name, marker="none"
                )

            total_yield = self.pdf.get_yield().numpy()
            pdf_yvals = (
                self.pdf.pdf(pdf_xvals) * total_yield * (bin_edges[1] - bin_edges[0])
            )
            self.ax.plot(
                pdf_xvals, pdf_yvals, label=self.pdf.name, marker="none", color="r"
            )

            self.fig.legend()

            self.ax.set_xlim(bin_edges[0], bin_edges[-1])

            self.ax.set_title(self.name)
            self.ax.set_xlabel(self.observable.obs[0])
            self.ax.set_ylabel("Counts per bin")
            hep.lhcb.label(loc=0, ax=self.ax, label="Preliminary", data=True, rlabel="")

    def save(self, plot_path: str):
        """Save the plot to a file

        Args:
            plot_path: Directory path where the plot should be saved. The filename will
                       be constructed from the configured name and extension
        """
        if not os.path.exists(plot_path):
            os.makedirs(plot_path)

        path = os.path.join(plot_path, self.name)

        if self.backend == "roofit":
            self.canvas.SaveAs(f"{path}{self.extension}")
        elif self.backend == "zfit":
            self.fig.savefig(f"{path}{self.extension}")
            plt.close(self.fig)


class Sideband:
    """Handler for sidebands in the sideband subtraction mitigation method

    This class manages the definition and manipulation of signal and sideband regions
    for background subtraction in trigger efficiency calculations. It provides methods
    to define cuts and the appropriate scale factor to estimate the number of background
    events in a given width.
    """

    def __init__(
        self,
        variable: str,
        variable_range: Annotated[List[float], 2],
        sideband_range: Annotated[List[float], 2],
        signal_range: Annotated[List[float], 2] = None,
    ):
        """Initialize a new Sideband instance

        Args:
            variable: Name of the variable used for sideband subtraction
            variable_range: Full range of the variable [min, max]
            sideband_range: Range defining the sideband regions [lower, upper]
            signal_range: Optional signal region range, calculated as the region between sidebands
                          if not provided
        """

        self.variable = variable
        self.range = variable_range
        self.sideband = sideband_range

        if signal_range:
            self.signal = signal_range
        else:
            self.signal = [
                self.sideband[0] - self.range[0],
                self.range[1] - self.sideband[1],
            ]

    def scale(self, width=None):
        """Calculate the scaling factor for sideband subtraction

        Args:
            width: Optional width to use instead of signal region width

        Returns:
            float: Scaling factor for sideband subtraction, calculated as
                  signal_width / (lower_sideband_width + upper_sideband_width)
        """
        if not (width):
            width = self.signal[1] - self.signal[0]
        return width / (
            (self.sideband[0] - self.range[0]) + (self.range[1] - self.sideband[1])
        )

    def range_cut(self):
        """Generate a cut string for the full variable range

        Returns:
            str: Cut string in ROOT format selecting events in the full range
        """
        var = self.variable
        return f"({var} > {self.range[0]}) && ({var} < {self.range[1]})"

    def sideband_cut(self):
        """Generate a cut string for the sideband regions

        Returns:
            str: Cut string in ROOT format selecting events in both lower and upper sidebands
        """
        var = self.variable
        lower_cut = f"({var} > {self.range[0]}) && ({var} < {self.sideband[0]})"
        upper_cut = f"({var} < {self.range[1]}) && ({var} > {self.sideband[1]})"
        return f"({lower_cut}) || ({upper_cut})"

    def signal_cut(self):
        """Generate a cut string for the signal region

        Returns:
            str: Cut string in ROOT format selecting events in the signal region
        """
        var = self.variable
        return f"({var} > {self.signal[0]}) && ({var} < {self.signal[1]})"
