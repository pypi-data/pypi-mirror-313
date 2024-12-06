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

import ROOT as R
from .utils import example_file

R.gROOT.SetBatch(True)


def test_raw(example_file):
    from triggercalib import HltEff

    tree, path = example_file

    hlteff = HltEff(
        "test_raw",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        expert_mode=True,
    )
    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [5, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts("raw")
    hlteff.efficiencies("raw")
    hlteff.write("results/output_test_raw.root")
