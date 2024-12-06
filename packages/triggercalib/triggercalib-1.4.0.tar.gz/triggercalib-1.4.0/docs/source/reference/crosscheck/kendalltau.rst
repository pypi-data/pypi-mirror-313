.. _kendalltau_reference:

KendallTau Class Reference
==========================

.. currentmodule:: triggercalib.crosscheck.kendall_tau

The KendallTau class provides an implementation of  for validating sWeight calculations using Kendall's tau correlation coefficient.
This is particularly useful when the assumptions of the
factorisation test in :ref:`factorisation_reference` may not hold.

A special thanks goes to Hans Dembinski for providing the Kendall's tau test in the `factorisation tests notebook of the sweights package <https://github.com/sweights/sweights/blob/main/doc/notebooks/factorization_test.ipynb>`_.

Class Documentation
-----------------

.. autoclass:: KendallTau
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Usage Example
------------

.. code-block:: python

   from triggercalib.crosscheck import KendallTau

   # Create correlation test
   test = KendallTau(
       discriminating_obs=mass_var,
       control_var="pt",
       sample="data.root:DecayTree",
       pdf=model
   )

   # Check correlation
   print(f"Correlation coefficient: {test.tau}")
   print(f"P-value: {test.p_value}")