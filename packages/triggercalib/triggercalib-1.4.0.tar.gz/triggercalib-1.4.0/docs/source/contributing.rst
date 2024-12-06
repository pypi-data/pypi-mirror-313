.. _contributing:

Contributing
============

Contributions to TriggerCalib are very welcome! Bug reports, feature requests and code contributions are encouraged: bug reports and feature requests can be submitted as `issues <https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues>`_; code contributions can be proposed in `merge requests <https://gitlab.cern.ch/lhcb-rta/triggercalib/-/merge_requests>`_. Details on how to submit these are provided below.

For more information and to ask questions, we recommend joining the `TriggerCalib Mattermost channel <https://mattermost.web.cern.ch/lhcb/channels/triggercalib>`_.


.. _issues:
Submitting bug reports/feature requests
---------------------------------------

To submit a bug report or feature request, please open an `issue <https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues>`_.
Bug reports should contain a description of the bug and the circumstances in which the bug was discovered.
If possible, a `minimal reproducible example <https://en.wikipedia.org/wiki/Minimal_reproducible_example>`_ should be included.
Feature requests should contain a description of the requested feature, an explanation of why this is required.
Feature requests can be supplemented with information on how to approach implementing the feature or with a corresponding merge request (see `Developing TriggerCalib`_).

We kindly ask that you add the ``bug`` or ``feature`` label to your issue so that we can keep track.


Developing TriggerCalib
-----------------------

Developments to TriggerCalib are encouraged and can be proposed in a `merge request <https://gitlab.cern.ch/lhcb-rta/triggercalib/-/merge_requests>`_.
Merge requests should ideally aim to close a raised issue (see `Submitting bug reports/feature requests`_).
When a merge request is ready for review, please assign Jamie (`@jagoodin <https://gitlab.cern.ch/jagoodin>`_) as a reviewer.
For a merge request to be merged it must:

* Passes the CI pipeline (see `Running the tests`_ and `Fixing the formatting`_ for troubleshooting)
* Has received an approval

A few labels currently exist to help track merge requests; please use these if they cover an aspect of the code under development.

To develop TriggerCalib locally:

1. Clone the repository
2. Source ``LbEnv``::

    source /cvmfs/lhcb.cern.ch/lib/LbEnv

3. Create a virtual environment, e.g.::

    lb-conda-dev virtual-env default/2024-06-08 .venv

4. Install the packages required for development::

    .venv/run pip install -r requirements-dev.txt

Running the tests
-----------------

The CI pipeline job ``testing`` runs a set of tests in ``pytest``.
These tests can be run locally by running ``pytest`` from the top level of the repository.

Fixing the formatting
---------------------

The CI pipeline applies a formatting check with ``black``.
Fixes to the formatting can be made by running ``black src`` from the top level of the repository