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

"""Trigger efficiency calculation module

This module provides the core functionality for calculating trigger efficiencies:

- HltEff: Main class for efficiency calculations with multiple methods
- Plot: Helper class for visualizing efficiency results
- Sideband: Helper class for background subtraction
"""

from .hlteff import HltEff
from .objects import Plot, Sideband

__all__ = ["HltEff", "Plot", "Sideband"]
