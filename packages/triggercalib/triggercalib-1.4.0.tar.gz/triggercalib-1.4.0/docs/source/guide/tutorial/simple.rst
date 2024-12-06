Calculating the efficiency of a single HLT1 line
================================================

As a simple example, the efficiency of `Hlt1TrackMVA` will be calculated from a preselected sample of Block 1 data selected as :math:`B^+\to J/\psi\left(\mu^+\mu^-\right)K^+`.
This sample can be found at ``root://eoslhcb.cern.ch//eos/lhcb/wg/rta/WP4/TriggerCalib/Bu2JpsiK_Jpsi2MuMu_block1_ntuple.root``.
We start by using a sideband subtraction approach.

Sideband subtraction approach
-----------------------------
The configuration of `HltEff` to run with sideband subtraction is fairly straightforward:

.. code-block:: python

    hlt_eff = HltEff(
        "simple_example",
        "root://eoslhcb.cern.ch//eos/lhcb/wg/rta/WP4/TriggerCalib/Bu2JpsiK_Jpsi2MuMu_block1_ntuple.root:Tuple/DecayTree",
        probe="Hlt1TrackMVA",
        tag=["Hlt1TrackMVA", "Hlt1TwoTrackMVA"],
        particle="B",
        binning={
            "B_PT" : {
                "bins" : [
                    n*1e3 for n in (
                        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                        14, 15, 16, 17, 18, 19, 20, 21, 22, 25
                    )
                ]
            }
        },
        sideband={
            "B_DTF_Jpsi_MASS": {
                "range": [5280 - 150, 5280 + 150], # Define outer sideband edges as 5130 and 5430
                "sideband": [5280 - 55, 5280 + 55], # Define inner sideband edges as 5225 and 5335 (signal window inferred between)
            }
        }
    )

A name, sample and tree are passed in the first two arguments.
The tag and probe (TIS and TOS) for the efficiencies are then defined, along with the particle of interest.
The binning scheme is laid out in the control variable—in this case ``B_PT``.
Finally, the sideband is defined based on the full range of the window and the inner/outer edges of the sideband.
In this case, the sidebands are defined as 5130-5225 MeV and 5335-5430 MeV.


Fit-and-count approach
----------------------

🚧 Work in progress, please check back another time

sPlot approach
--------------

🚧 Work in progress, please check back another time

Trigger efficiencies with 2D binning schemes
--------------------------------------------

🚧 Work in progress, please check back another time