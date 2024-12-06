TriggerCalib: a one-stop-shop for trigger efficiencies at LHCb
==============================================================

Welcome to the official documentation for the TriggerCalib software package.
This Python package provides offline analysis tools for calculating trigger efficiencies in LHCb with the data-driven TISTOS method.
TriggerCalib was written with Run 3 in mind; however, it should be applicable for use in Run 2 analyses/studies.
The source can be found at `lhcb-rta/TriggerCalib <https://gitlab.cern.ch/lhcb-rta/triggercalib>`_ and installed `from PyPI <https://pypi.org>`_ by ``pip install triggercalib``.


The documentation is split into two parts:

- :ref:`user-guide`, introducing trigger efficiency calculations and walking through the steps to calculate trigger efficiencies with the tooling provided in TriggerCalib.
- :ref:`reference`, providing a full reference for the classes introduced by TriggerCalib.

For any queries please join the `TriggerCalib Mattermost channel <https://mattermost.web.cern.ch/lhcb/channels/triggercalib>`_.


Acknowledgements
-------------------------------------------------------

We acknowledge funding from the European Union Horizon 2020 research and innovation programme, call H2020-MSCA-ITN-2020, under Grant Agreement n. 956086

|smarthep-logo| |eu-flag| |msca-logo|

.. toctree::
   :caption: Table of contents
   :includehidden:
   :maxdepth: 4

   guide/index
   reference/index
   resources
   contributing
   changelog


.. |smarthep-logo| image:: https://www.smarthep.org/wp-content/uploads/2022/11/SmartHEP-Logo-Full-Colour.jpg
   :height: 64
.. |eu-flag| image:: https://www.smarthep.org/wp-content/uploads/2022/11/EU-Logo.jpg
   :height: 64
.. |msca-logo| image:: https://www.smarthep.org/wp-content/uploads/2022/11/marie_curie_logo-300x182-1.png
   :height: 64
