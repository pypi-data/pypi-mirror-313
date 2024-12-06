.. _backgrounds:

Mitigation of backgrounds
=========================

Most samples from which we would wish to extract a trigger efficiency are not entirely signal and instead contain some background component(s).
To compute signal efficiencies in such samples, the background(s) must be mitigated.
Three methods for mitigating background are presented here: sideband subtraction, fit-and-count and `sPlot`.
The validity and limitations of each method are also discussed below.

This section will make frequent use of the terms control variable(s) and discriminating variable(s).
The control variable is the variable we are interested in making some measurement in, e.g., th transverse momentum of a :math:`B^0`, whilst the discriminating variable is the variable which is used to make a distinction between signal and background, e.g., invariant mass of :math:`B^0` products.

Subtraction of sideband density
-------------------------------

For well-behaved (near-linear) backgrounds lying beneath the signal in the discriminating variable distribution, the  background beneath the signal can be estimated from the sidebands: regions in the discriminating variable well-separated from the signal region.
The background density is calculated by counting the number of events in the sidebands and normalising by the width of the sidebands.
This density is converted to a background count by multiplying by the width of the region of interest (either the whole signal region or a single bin).
The signal count in the region of interest can then be calculated by simply subtracting this estimated background count.
This can be repeated per-bin in the control variable(s) to subtract the background density in every bin.

Per-bin fitting and counting (fit-and-count)
--------------------------------------------
More complicated backgrounds, e.g., peaking backgrounds overlapping with the signal, cannot be well-mitigated using sideband subtraction.
Instead, a more thorough approach is involved, wherein an extended fit is performed to the discriminating variable, with a signal component and one or more background components.
The yield of the signal component can then be taken to be the signal count.
This too can be repeated per-bin in the control variable(s) to build up a useful histogram of signal counts.
This is more precise but typically also more computationally expensive than sideband subtraction and requires bins to be coarse enough that all fits converge.

Weighting from global fits with `sPlot` 
---------------------------------------
A compromise with the fit-and-count approach can be found in the `sPlot` method, in which per-event weights are computed from a fit to the discriminating variable which is global in the control variable(s).
These weights can then be counted when binning the control variable(s) to obtain a signal histogram.
This approach is only valid if all components of the fit are uncorrelated between discriminating and control variables.
