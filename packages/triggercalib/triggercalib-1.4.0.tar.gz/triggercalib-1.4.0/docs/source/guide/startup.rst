.. _getting-started:

Getting started
=======================================================

TriggerCalib is a Python package which can be installed `from PyPI <https://pypi.org/project/triggercalib>`_ using ``pip install triggercalib`` and is compatible with Python 3.6+.
In the near future, TriggerCalib will also be installable with ``conda``.
Most of the dependencies TriggerCalib are handled by ``pip``; however, ``ROOT`` cannot currently be ``pip install``\ ed, and so must be included in the environment from which TriggerCalib is run.
By default, TriggerCalib is installed without ``zfit``; however, ``pip install triggercalib[zfit]`` installs TriggerCalib with ``zfit``.
The ``zfit`` backend is only enabled if ``zfit`` can be imported.

TriggerCalib provides a ROOT-based implementation of the TISTOS [1]_ method of calculating trigger efficiencies and is designed to run out of the box on your analysis ntuples.
Following the steps of this user guide, TriggerCalib can beconfigured to produce histograms of event counts in TIS/TOS/trigger categories and TIS/TOS/trigger efficiencies for desired HLT1 and/or HLT2 lines, in either 1- or 2-dimensions.

It is recommended that you read through \":ref:`introduction`\" first to understand the TISTOS method and its implementation.
The tutorial given in \":ref:`tutorial`\" walks through the main functionality of TriggerCalib's ``HltEff`` class: an efficiency calculator described in \":ref:`hlteff_reference`\".
Additional, advanced, functionality is described in \":ref:`advanced`\".


.. [1] \S. Tolk et al., *Data driven trigger efficiency determination at LHCb* (`LHCb-PUB-2014-039 <https://cds.cern.ch/record/1701134/files/LHCb-PUB-2014-039.pdf>`_), 2014