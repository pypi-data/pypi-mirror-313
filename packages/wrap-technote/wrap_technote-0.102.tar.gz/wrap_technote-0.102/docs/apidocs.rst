##########################################
wrap_technote developer API
##########################################

************************
API table of contents
************************

.. contents:: Table of Contents
   :depth: 6
   :local:
   :backlinks: none

****************************************
Running the analysis - stages and steps 
****************************************

Analysis framework
==================
.. autoclass:: wrap_technote.Run
    :members:

Water level
===============
.. autoclass:: wrap_technote.QueryAndValidateWaterLevels
    :members:
.. autoclass:: wrap_technote.CalculateSeasonalWaterLevels
    :members:

*************************************************
Reporting periods, reports, resources, etc.
*************************************************

Reporting period
============================
.. autofunction:: wrap_technote.load_reporting_period
.. autoclass:: wrap_technote.ReportingPeriod
    :members:

.. autodata:: wrap_technote.reporting.ANNUAL_WRA_PATH
    :no-value:
.. autodata:: wrap_technote.reporting.reporting_period_paths
    :no-value:
.. autodata:: wrap_technote.reporting.paths_reporting_period
    :no-value:

Report
===========================
A report is equivalent to a single Technical Note.

.. autofunction:: wrap_technote.load_report
.. autoclass:: wrap_technote.Report
    :members:

Resource
==============================================
Each resource represents a single groundwater resource.

.. autofunction:: wrap_technote.load_resource
.. autoclass:: wrap_technote.Resource
    :members:

Multiple resources in one go (e.g. aggregate resources)
----------------------------------------------------------

.. autofunction:: wrap_technote.read_data
.. autoclass:: AggregateGroundwaterResource
    :members:

Selecting wells
===================
.. autoclass:: wrap_technote.WellSelectionQuery
    :members:

***************************************
General data filtering or analysis
***************************************

Filtering monitoring data
==================================
.. autofunction:: wrap_technote.load_qc_removals
.. autofunction:: wrap_technote.filter_to_between_years

Data analysis
========================================
.. autofunction:: wrap_technote.calc_well_record_quality
.. autofunction:: wrap_technote.linear_trend
.. autofunction:: wrap_technote.calculate_trendline_at_dates
.. autofunction:: wrap_technote.get_median_class

BoM percentile ranking functions
=========================================
These functions relate to the BoM classification of deciles into 
the categories: Lowest on record, Very much below average, Below
average, average, above average, very much above average, and 
highest on record.

.. autofunction:: wrap_technote.percentile_to_bom_class
.. autofunction:: wrap_technote.map_percentile_into_bom_class
.. autofunction:: wrap_technote.rank_and_classify
.. autofunction:: wrap_technote.get_median_ranking

Triclass trends 
=================================
.. autodata:: wrap_technote.reporting.increasing_codes
.. autodata:: wrap_technote.reporting.decreasing_codes
.. autofunction:: wrap_technote.get_median_trend_triclass

Charting
==================================

BoM ranking functions
-----------------------------------------
.. autoclass:: wrap_technote.MonthlyColormap
    :members:
.. autoclass:: wrap_technote.BoMClassesColormap
    :members:
.. autofunction:: wrap_technote.bom_classes_dict

Triclass trends
----------------------------------------------------------
.. autofunction:: wrap_technote.status_to_colours

************************************
Water level data
************************************

Processing and analysis
=========================
.. autofunction:: wrap_technote.filter_wl_observations

Seasonal analysis
-------------------------
.. autoclass:: wrap_technote.Seasons
    :members:
.. autofunction:: wrap_technote.analyse_wl_by_seasons
    
Charts
====================
.. autofunction:: wrap_technote.plot_wl_data_validation
.. autofunction:: wrap_technote.plot_wl_months_coloured
.. autofunction:: wrap_technote.plot_wl_seasonality
.. autofunction:: wrap_technote.plot_wl_seasonal_timeseries
.. autofunction:: wrap_technote.plot_wl_bom_classes
.. autofunction:: wrap_technote.plot_wls_with_logger
.. autofunction:: wrap_technote.plot_wl_trend
.. autofunction:: wrap_technote.plot_wl_rankings_internal
.. autofunction:: wrap_technote.plot_wl_historical_rankings
.. autofunction:: wrap_technote.plot_wl_ranking_classes
.. autofunction:: wrap_technote.plot_wl_ranking_map
.. autofunction:: wrap_technote.plot_wl_trend_triclass_bars

Reporting
===========================
.. autofunction:: wrap_technote.collate_waterlevel_summary_data
.. autofunction:: wrap_technote.get_majority_categories
.. autofunction:: wrap_technote.construct_waterlevel_template_sentences

************************************
Salinity data
************************************

Processing and analysis
=========================
.. autofunction:: wrap_technote.filter_tds_observations
.. autofunction:: wrap_technote.reduce_to_annual_tds
.. autofunction:: wrap_technote.calculate_annual_tds_stats
.. autofunction:: wrap_technote.linear_salinity_trend
.. autofunction:: wrap_technote.calculate_historical_salinity_trends
.. autofunction:: wrap_technote.generate_salinity_bins
.. autofunction:: wrap_technote.calculate_salinity_indicator_results
.. autofunction:: wrap_technote.calculate_salinity_indicator_summary_results
.. autofunction:: wrap_technote.calculate_historical_pct_diff_values

Charts
============================

Reporting
=============================
.. autofunction:: wrap_technote.collate_salinity_summary_data
.. autofunction:: wrap_technote.construct_salinity_template_sentences

************************************
Rainfall data
************************************

General
====================================
.. autoclass:: wrap_technote.RainfallStationData
    :members:

Downloading data
==============================
.. autofunction:: wrap_technote.download_bom_rainfall
.. autofunction:: wrap_technote.download_aquarius_rainfall

Data analysis
============================
.. autofunction:: wrap_technote.get_seasonal_rainfall_data
.. autofunction:: wrap_technote.reduce_daily_to_monthly

************************
Utility functions
************************

Reporting
========================
.. autofunction:: wrap_technote.load_html_templates

General
===============================
.. autofunction:: wrap_technote.get_logger
.. autofunction:: wrap_technote.chunk
.. autofunction:: wrap_technote.intround
.. autofunction:: wrap_technote.round_to_100_percent
.. autofunction:: wrap_technote.append_comment_to_dataframe_column
.. autofunction:: wrap_technote.highlight_fields
.. class:: wrap_technote.DataFileDict

File utilities
----------------------
.. autofunction:: wrap_technote.read_csv
.. autofunction:: wrap_technote.df_to_shp

Context managers
-----------------
.. autofunction:: wrap_technote.add_import_path
.. autofunction:: wrap_technote.cd


Date manipulation
==================================
.. autofunction:: wrap_technote.doy
.. autofunction:: wrap_technote.doy_to_non_leap_year
.. autofunction:: wrap_technote.parse_australian_date
.. autofunction:: wrap_technote.date_to_decimal
.. autofunction:: wrap_technote.decimal_to_date
.. autofunction:: wrap_technote.date_to_wateruseyear
.. autofunction:: wrap_technote.date_to_season
.. autofunction:: wrap_technote.get_yearspans_between
.. autofunction:: wrap_technote.filter_to_between_years
.. autofunction:: wrap_technote.generate_yearly_periods
.. autofunction:: wrap_technote.get_wu_year_from_month_and_year
.. autofunction:: wrap_technote.get_spanning_dates
.. autofunction:: wrap_technote.find_missing_days
.. autodata:: wrap_technote.gwutils.months_to_seasons
.. autodata:: wrap_technote.gwutils.month_dayofyears

