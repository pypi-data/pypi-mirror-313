######################################
Changelog and planned development
######################################

***************************
List of versions
***************************

Unreleased changes
--------------------

Version 0.92 (20th November 2023)
----------------------------------
- Replace ``np.float()`` with ``float()`` and ``np.int()`` with ``int()``
- Change backcalculated reporting period paths to resolve tricky error.
- Simplify installation instructions

Version 0.15.0 (8 Apr 2020)
---------------------------
- Add map_limits variables

Version 0.14.0 (2 Apr 2020)
---------------------------
- Add report command to scripts

Version 0.13.0 (10 Mar 2020)
----------------------------
- Add Waterkennect map links to static html output pages

Version 0.12.1 (3 Mar 2020)
---------------------------
- Add waterlevels script

Version 0.11.0 (26 Feb 2020)
----------------------------
- Add round_to_100_percent() function

Version 0.10.0 (25 Feb 2020)
----------------------------
- Allow passing mpl figure to plot_tds_validation
- Add more removal reason colours
- Fix bug assuming pd.Series in trend line function
- Fix bug in trend historical max calculation
- Add salinity trend functions

Version 0.9.0 (19 Feb 2020)
---------------------------
- Add salinity data validation charts
- Fix memory leaks for data validation charts

Version 0.8.3 (19 Feb 2020)
---------------------------
- make DPI better default and configurable

Version 0.8.2 (19 Feb 2020)
---------------------------
- Add adjustText to plot_wl_data_validation

Version 0.8.1 (18 Feb 2020)
---------------------------
- Fix CRAZY SQL bug which broke the GW resource selection queries

Version 0.8.0 (13 Feb 2020)
----------------------------
- Add WL trend functions
- Add rainfall chart proposals

Version 0.7.3 (10 Feb 2020)
---------------------------
- Add "season_year" column to recovered WL tables.

Version 0.7.2 (6 Feb 2020)
--------------------------
- Fix bug where 'nan' is undefined for eval()

Version 0.7.1 (6 Feb 2020)
--------------------------
- Filter out Hydstra records coded as 'below recordable range'
- Order data validation charts alphabetically

Version 0.7.0 (6 Feb 2020)
--------------------------
- Add WL QC ranking spreadsheet

Version 0.6.1 (5 Feb 2020)
--------------------------
- Add hydstra/sag colour to data val chart

Version 0.6.0 (5 Feb 2020)
--------------------------
- Add ReportingPeriod and ReportingPeriodResource classes. Major re-org.
- Fix pandas Timestamp bug

Version 0.5.1 (4 Feb 2020)
--------------------------
- Fix add_subplot(111) bug

Version 0.5.0 (4 Feb 2020)
--------------------------
- Add data validation process and charts
  - see e.g. plot_wl_data_validation()
- Add seasons definition spreadsheet process
- Show comments on data validation plot

Version 0.4.5 (3 Feb 2020)
--------------------------
- Fix bug resulting in incorrectly dropping all SAG WLs with comments
- Update report figure notebooks - many improvements

Version 0.4.4 (29 Jan 2020)
---------------------------
- Fix subtle leap year bug
- Provide a variant foreground color for BoM classes
- Update report figure notebooks

Version 0.4.3 (21 Jan 2020)
---------------------------
- Add function to retrieve analysis tables
- Fix bug where filter_wl_observations was dropping all Hydstra data
- Fix bug in calc_well_record_quality() for wells with gaps in years
- Fix bug with Seasons.from_str and Seasons.to_str

Version 0.4.2 (21 Jan 2020)
---------------------------
- Fix bug with incorrectly labelled Y axis on plot_wl_months_coloured()

Version 0.4.1 (21 Jan 2020)
---------------------------
- Fix bug with plot_wls_with_logger() when logger_df is empty

Version 0.4.0 (21 Jan 2020)
----------------------------
- Improve readability and colours on charts.plot_wl_seasonality()
- Remove unneeded scripts (replaced with Jupyter Notebooks for now)
- Add filter to WL filter func to remove "Missed peak recovery" comments
- Add plot_wls_with_logger() function for Hydstra data
- Add draft notebook for the new per-aquifer results page in the TN

Version 0.3.9 (17 Jan 2020)
---------------------------
- Minor changes, additions to update Saeed on latest
  notebook

Version 0.3.6 (16 Jan 2020)
----------------------------
- Add notebook for putting six hydrographs in a panel plot
- Add code (still in development) for retrieving logger data
  from Hydstra and combining it with manual observations
- Add a simpler definition of a recovery season
- Update the WL rankings scripts and static HTML summary

Version 0.3.5
-------------
- Fix bugs with ranking script

Version 0.3.4
-------------
- Add wl_rankings_v1.py script

Version 0.3.3
-------------
- Update documentation and bugs

Version 0.3.2
--------------
- Fix bug with wrap_technote.load_gw_resources()

Version 0.2.0
---------------
- Add TDS_SUBQUERY to WellSelectionQuery
- Add filter_tds_observations: anom_ind = "N" & measured_during != "D" (that's it)

Version 0.1.0
----------------
- Initial version for selecting wells and filtering WLs

************************************
Planned development
************************************

.. todolist::