Configuration
================================

Codes
-----------------

Codes are provided as lookup table lists for a variety of reasons.

For the "status_change" variable (5 year trend class)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autodata:: wrap_technote.gwutils.wl_status_changes
.. autodata:: wrap_technote.gwutils.tds_status_changes

For the "bom_rswl_class" variable (ranked water levels)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are all part of the BoM colourmap :class:`wrap_technote.BoMClassesColormap`.

.. autoattribute:: wrap_technote.charts.BoMClassesColormap.class_names

Colours and chart marker shapes etc.
--------------------------------------

Generally speaking, colours are defined in only one place somewhere in the wrap_technote
module code, to ensure they are consistent throughout all the figures produced.

For the "status_change" variable (5 year trend class)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autodata:: wrap_technote.charts.status_change_colours
.. autodata:: wrap_technote.charts.wl_status_change_colours
.. autodata:: wrap_technote.charts.tds_status_change_colours

This function converts a status_change code to two colours (one background, one foreground)
suitable for a text label:

.. autofunction:: wrap_technote.gwutils.status_to_colours

For the "bom_rswl_class" variable (ranked water levels)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are all part of the BoM colourmap :class:`wrap_technote.BoMClassesColormap`.

.. autodata:: wrap_technote.charts.BoMClassesColormap.class_names
.. autodata:: wrap_technote.charts.BoMClassesColormap.colours
.. autodata:: wrap_technote.charts.BoMClassesColormap.colours_nodata
.. autodata:: wrap_technote.charts.BoMClassesColormap.foreground_colours
.. autodata:: wrap_technote.charts.BoMClassesColormap.foreground_colours_2

Data and other things
~~~~~~~~~~~~~~~~~~~~~

For salinity data, lookup tables are provided to assist with drawing figures:

.. autodata:: wrap_technote.charts..extract_method_lut
.. autodata:: wrap_technote.charts..measured_during_lut
.. autodata:: wrap_technote.charts..extract_method_markers
.. autodata:: wrap_technote.charts..meas_during_colours
.. autodata:: wrap_technote.charts..removal_reason_colours

A similar set of colours for water level data:

.. autodata:: wrap_technote.charts..season_colours

For rainfall charts, the colours are defined in:

.. autodata:: wrap_technote.charts.rainfall_colours



Other constants
---------------

.. autodata:: wrap_technote.gwutils.month_dayofyears

