.. _utils_reference:

Utility Functions Reference
=========================

.. currentmodule:: triggercalib.utils

The utils module provides helper functions for working with ROOT and zFit objects.
These functions assist with data format conversion and fitting operations.

Functions
--------

ROOT Utilities
~~~~~~~~~~~~

.. autofunction:: bins_from_taxis
.. autofunction:: split_paths
.. autofunction:: tgraph_to_th

zFit Utilities
~~~~~~~~~~~~

.. autofunction:: create_zfit_dataset
.. autofunction:: zfit_fit

Usage Examples
------------

Converting ROOT graphs to histograms:

.. code-block:: python

   from triggercalib.utils import tgraph_to_th

   # Convert TGraphAsymmErrors to TH1D
   hist = tgraph_to_th(
       graph,
       name="converted_hist"
   )

Creating zFit datasets:

.. code-block:: python

   from triggercalib.utils import create_zfit_dataset

   # Create dataset from NumPy arrays
   dataset = create_zfit_dataset(
       data={"B_M": mass_array},  # Branch name in data
       observable=mass_space      # zFit observable
   )
