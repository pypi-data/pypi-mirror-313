.. _hlteff_reference:

HltEff Class Reference
======================

.. currentmodule:: triggercalib.hlteff

The HltEff class is the core calculator for trigger efficiencies.
It supports:
- Multiple trigger categories (TIS, TOS, TISTOS)
- Flexible 1- and 2-dimensional binning schemes
- Background mitigation via sideband subtraction, fit-and-count and sPlot methods
- A unified interface to both RooFit and zFit fitting backends

Class Documentation
-----------------

.. autoclass:: HltEff
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __getitem__

Usage Example
------------

.. code-block:: python

   from triggercalib import HltEff

   # Initialize HltEff instance
   hlteff = HltEff(
       name="example",
       path="data.root:DecayTree",
       probe="Hlt1TrackMVA",
       tag=["Hlt1TrackMVA", "Hlt1TwoTrackMVA"],
       particle="B",
       binning={"B_PT": {"bins": [0, 1000, 2000, 3000], "label": "B transverse momentum [MeV]"}},
       # <- Specify your background mitigation here
   )

   # Calculate efficiencies
   hlteff.counts()
   hlteff.efficiencies()

   # Save results
   hlteff.write("output.root")