.. _tistos:

Data-driven efficiencies with the TISTOS method
===============================================

TISTOS is a data-driven method for determining trigger efficiencies, discussed (including full proof) in full in Ref. [1]_.
This method is briefly outlined below.

Ideally, the efficiency of a trigger selection could be calculated as

.. math::

    \varepsilon_\mathrm{Trig} = \frac{N_\mathrm{Trig}}{N_\mathrm{Total}},

where :math:`N_\mathrm{Total}` is the total number of events within the acceptance (i.e., which could be triggered) and :math:`N_\mathrm{Trig}` is the number of events which are triggered on.
More frequently :math:`\varepsilon_\mathrm{Trig}` is defined in terms of the number of events in a sample subject to some form of selection, :math:`N_\mathrm{Sel}`:.
The Trig, TIS, TOS and TISTOS categories discussed here are all assumed to be conditional on this selection, with the :math:`\mathrm{\vert Sel}` generally dropped for convenience.

.. math::

    \varepsilon_\mathrm{Trig.} = \frac{N_\mathrm{Trig\vert Sel}}{N_\mathrm{Sel}}.

However, since triggering is a destructive process, :math:`N_\mathrm{Total}/N_\mathrm{Sel}`  are not known quantities in data (in simulation we can keep this information, which makes our lives much easier).
As such, we will need to get a bit more creative.


Defining the TIS and TOS categories
------------------------------

We start by defining categories in terms of the trigger response on each event and with respect to a given signal (i.e., a particle in the channel of interest):

* **Trig.**: The trigger fires on the event.
* **TOS**: The presence of the signal causes the trigger to fire on the event. Specifically, at least 70% of hits in the reconstructed trigger candidates are hits associated with the signal.
* **TIS**: The trigger fires on the event regardless of the signal. Specifically, if any of the reconstructed trigger candidates share fewer than 1% of hits with the signal.
* **TISTOS**: The event is both TIS and TOS.

.. _fig1:
.. figure:: /_static/tistos.png
    :align: center
    :width: 90%

    Diagram illustrating TIS/TOS/TISTOS/Trig. categories.

From categories to efficiencies
-------------------------------

Each of the TIS/TOS/TISTOS categories then has a corresponding efficiency:

.. math::

    \varepsilon_\mathrm{TIS/TOS/TISTOS} = \frac{N_\mathrm{TIS/TOS/TISTOS}}{N_\mathrm{Sel}}.

These are particularly useful because :math:`\varepsilon_\mathrm{Trig.}` can be expanded as

.. math::

    \varepsilon_\mathrm{Trig.} = \frac{N_\mathrm{Trig}}{N_\mathrm{Sel}} =  \frac{N_\mathrm{Trig}}{N_\mathrm{TIS}} \frac{N_\mathrm{TIS}}{N_\mathrm{Sel}} = \frac{N_\mathrm{Trig}}{N_\mathrm{TIS}} \varepsilon_\mathrm{TIS}.

Whilst :math:`\varepsilon_\mathrm{TIS}` was previously defined in terms of :math:`N_\mathrm{Sel}`, this efficieny can be defined within the TOS subsample as

.. math::

    \varepsilon_\mathrm{TIS\vert TOS} = \frac{N_\mathrm{TISTOS}}{N_\mathrm{TOS}},

which is equivalent to :math:`\varepsilon_\mathrm{TIS}` under the assumption that :math:`\varepsilon_\mathrm{TIS}` of any subsample is identical to that of the full sample.
Plugging this into the expression for \varepsilon_\mathrm{Trig.} yields the final expression for \varepsilon_\mathrm{Trig.} (as implemented in the tools),

.. math::

    \varepsilon_\mathrm{Trig.} = \frac{N_\mathrm{Trig}}{N_\mathrm{TIS}} \frac{N_\mathrm{TISTOS}}{N_\mathrm{TOS}}.

A frequently-used proxy for this trigger efficiency, :math:`\varepsilon_\mathrm{TOS}` can be defined in a similar way to :math:`\varepsilon_\mathrm{TIS}`:

.. math::

    \varepsilon_\mathrm{TOS\vert TIS} = \frac{N_\mathrm{TISTOS}}{N_\mathrm{TIS}},

equivalent to :math:`\varepsilon_\mathrm{TOS}` under a similar assumption that :math:`\varepsilon_\mathrm{TOS}` is the same in the whole sample as in any subsample.
Both :math:`\varepsilon_\mathrm{TOS}` and :math:`\varepsilon_\mathrm{TIS}` are also implemented in the tool.

Mitigating correlation between TIS and TOS
------------------------------------------
The assumptions of TIS/TOS subsample-independence are not strictly true as, the signal and the rest of the event are frequently correlated, e.g.,, in the case of :math:`B` mesons, where the :math:`b\bar{b}` are produced as a pair and hence both :math:`B` are correlated.
This correlation can be circumvented by calculating the counts detailed above in sufficiently small phase space bins.
Performing such a binning, the expression for :math:`\varepsilon_\mathrm{Trig.}` becomes

.. math::

    \varepsilon_\mathrm{Trig.} = \frac{N_\mathrm{Trig}}{\sum\limits_i \frac{N^i_\mathrm{TIS}N^i_\mathrm{TOS}}{N^i_\mathrm{TISTOS}}}.

For more details and a derivation of the error propagation for :math:`\varepsilon_\mathrm{Trig.}` (also as implemented in the tools), it is highly recommended that you read Ref. [1]_

.. [1] \S. Tolk et al., *Data driven trigger efficiency determination at LHCb* (`LHCb-PUB-2014-039 <https://cds.cern.ch/record/1701134/files/LHCb-PUB-2014-039.pdf>`_), 2014
