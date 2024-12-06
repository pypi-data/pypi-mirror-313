##########################
Rainfall data
##########################

Rainfall data is obtained from stations via two different places:

1. Bureau of Meteorology, via SILO Patched Point Data (PPD) service.
   SILO is run by the Queensland Government.

2. Aquarius TS, for stations operated by DEW.

There is also spatial rainfall data in the technical notes - this is
not processed or touched by this code, it's done manually.

TLDR; easiest way to use 
=========================

You can download and access data via the 
:class:`wrap_technote.RainfallStationData` class:

.. autoclass:: wrap_technote.RainfallStationData
   :members:


Downloading data
======================

This is done through a variety of avenues, but fundamentally these
two functions do the work:

.. autofunction:: wrap_technote.download_bom_rainfall
.. autofunction:: wrap_technote.download_aquarius_rainfall

