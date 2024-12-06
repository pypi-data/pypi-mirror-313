.. _factorisation_reference:

Factorisation Class Reference
===========================

.. currentmodule:: triggercalib.crosscheck.factorisation

The Factorisation class implements tests to validate the use of the sPlot method by determining whether the control variable(s) are independent of the discriminating variable.
This is achieved by splitting the dataset in the control variable(s), performing a simultaneous fit across the full sample (with shape parameters shared between subsets) and individual fits in each subset, and comparing the likelihoods.
It supports both RooFit and zFit backends.

A special thanks goes to Hans Dembinski for providing the factorisation test in the `factorisation tests notebook of the sweights package <https://github.com/sweights/sweights/blob/main/doc/notebooks/factorization_test.ipynb>`_.


Class Documentation
-----------------

.. autoclass:: Factorisation
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Usage Example
------------

.. code-block:: python

    from triggercalib.crosscheck import Factorisation

    # Create factorisation test
    test = Factorisation(
        discriminating_obs=mass_var, # A RooFit or zFit observable to fit to
        control_var="B_PT", # Branch of control variable in sample
        sample="data.root:DecayTree",
        pdf=model, # A RooFit or zFit PDF
        threshold=0.05 # p-value set for likelihood comparison
    )

    # Analyse results
    if test.factorisable:
        print("Variables are independent!")