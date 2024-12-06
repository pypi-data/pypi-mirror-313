from collections import ChainMap
from datetime import datetime, date, time, timedelta
import json
import logging
import os
from pathlib import Path
import re

import numpy as np
import pandas as pd
from scipy import stats, optimize
import shapefile
import shapely.geometry

import sa_gwdata

from .utils import *

logger = get_logger()

SEASONAL_REDUCTION_FUNCS = {
    "max": np.max,
    "min": np.min,
    "mean": np.mean,
}

wl_status_changes = ["Declining", "Stable", "Rising"]
"""List of the different values that the water level "status_change"
field can take."""

tds_status_changes = ["Decreasing", "Stable", "Increasing"]
"""List of the different values that the TDS "status_change"
field can take."""


month_dayofyears = {
    "Jan": 1,
    "Feb": 32,
    "Mar": 60,
    "Apr": 91,
    "May": 121,
    "Jun": 152,
    "Jul": 182,
    "Aug": 213,
    "Sep": 244,
    "Oct": 274,
    "Nov": 305,
    "Dec": 335,
}
"""Defines the numeric day of the year for each month. Keys
are the abbreviated month names e.g. "Jul"; values are the
numeric day of the year for each month."""


decimal_words = (
    pd.read_csv(Path(__file__).parent / "decimal_word.csv").set_index("decimal").word
)


def status_to_colours(status, param="WL"):
    """Convert a triclass trend status code to colours suitable for a text label.

    Args:
        status (str): status change code e.g. "Declining", "Rising",
            "Stable", "Increasing", "Decreasing". Also includes the old
            GSR-style status codes.
        param (str): either "WL" or "TDS"

    Returns:
        tuple: tuple of the foreground colour e.g. either "white" or "black",
        and the background colour e.g. "yellow", and so on.

    """
    if param == "WL":
        return {
            "Declining": ("black", "yellow"),
            "Rising": ("white", "blue"),
            "Stable": ("white", "green"),
            "Declining (at historical low)": ("white", "black"),
            "Rising (at historical low)": ("white", "purple"),
            "Stable (at historical low)": ("black", "grey"),
            "Declining (at historical low during trend period)": ("white", "black"),
            "Rising (at historical low during trend period)": ("white", "purple"),
            "Stable (at historical low during trend period)": ("black", "grey"),
        }[status]
    elif param == "TDS":
        return {
            "Increasing": ("black", "yellow"),
            "Decreasing": ("white", "blue"),
            "Stable": ("white", "green"),
            "Increasing (above threshold)": ("white", "black"),
            "Decreasing (above threshold)": ("white", "purple"),
            "Stable (above threshold)": ("black", "grey"),
        }[status]


def bom_classes_dict():
    """Return a dictionary of the BoM decile classes with a value of 0
    for each item in the dict.

    Returns:
        dict:

    It is essentially a static method returning this value always::

        {
            "Lowest on record": 0,
            "Very much below average": 0,
            "Below average": 0,
            "Average": 0,
            "Above average": 0,
            "Very much above average": 0,
            "Highest on record": 0,
        }

    See :class:`wrap_technote.BoMClassesColormap` for more information.


    """
    return {
        "Lowest on record": 0,
        "Very much below average": 0,
        "Below average": 0,
        "Average": 0,
        "Above average": 0,
        "Very much above average": 0,
        "Highest on record": 0,
    }


#: Deprecated! Returns the path of the wrap_technote resources folder. Please
#: don't use this.
RESOURCES = Path(__file__).parent / "resources"


def generate_yearly_periods(spacing=10, start=1900, end=2050):
    """Generate a pd.Series mapping years between `start` and `end`
    to a yearly period of `spacing` years.

    Args:
        spacing (int): length of periods
        start (int): first period at this year
        end (int): last period ends before this year

    Returns:
        pd.Series: index is each year, value is a string for the period

    The default arguments result in a mapping to decades:

    .. code-block:: python

        >>> print(generate_yearly_periods(spacing=10, start=1950, end=2000))
        1950    1950-1959
        1951    1950-1959
        1952    1950-1959
        1953    1950-1959
        1954    1950-1959
                  ...
        2015    2010-2019
        2016    2010-2019
        2017    2010-2019
        2018    2010-2019
        2019    2010-2019
        Length: 70, dtype: object

    You can then use this to assign different periods to a dataframe
    containing dates:

    .. code-block:: python

        >>> tdsann["decade"] = tdsann.collected_year.map(generate_yearly_periods(spacing=10))
        >>> tdsann["period"] = tdsann.collected_year.map(generate_yearly_periods(spacing=5))
        >>> print(tdsann.head())
             well_id  collected_year     tds     decade     period
        0  6527-1146            1989  1132.0  1980-1989  1985-1989
        1  6527-1146            1990  1149.0  1990-1999  1990-1994
        2  6527-1146            2001  1116.0  2000-2009  2000-2004
        3  6527-1146            2007  1047.0  2000-2009  2005-2009
        4  6527-1146            2008  1141.0  2000-2009  2005-2009

    """
    y = start
    labels = []
    values = []
    while y <= (end + spacing):
        y0 = y
        y1 = y + spacing - 1
        for yi in range(y0, y1 + 1):
            labels.append(f"{y0}-{y1}")
            values.append(yi)
        y += spacing
    return pd.Series(labels, index=values)


def doy(s):
    """Convert "yyyy-mm-dd" to a day of year integer.

    Args:
        s (str): string in format of "yyyy-mm-dd" or
            "MMM d" e.g. "May 1"

    Returns:
        int: the day of the year (if s omits the year) then it will the
        day of the year in 2019 i.e. non-leap-year.

    Example:

    .. code-block:: python

        >>> from wrap_technote import doy
        >>> doy("May 1")
        121
        >>> doy("2019-05-01")
        121
        >>> doy("2000-05-01")
        122

    """
    if re.match(r"\d\d\d\d-\d\d-\d\d", s):
        return pd.Timestamp(s).dayofyear
    else:
        return month_dayofyears[s[:3]] + (int(s[3:].strip()) - 1)


def doy_to_non_leap_year(dn):
    """Convert day of year number to the relevant
    day in a non-leap year.

    Args:
        dn (int): day number of the year

    Returns:
        str: in format "%a %d" e.g. "Jan 5"

    Example:

    .. code-block:: python

        >>> import wrap_technote as tn
        >>> tn.doy_to_non_leap_year(1)
        'Jan 1'

    """
    dt = datetime(2019, 1, 1) + timedelta(days=(dn - 1))
    return dt.strftime("%b %d")


def parse_australian_date(dstr):
    """Convert a string like "19/11/2014" to a :class:`datetime.date` object.

    Args:
        dstr (str): string e.g. "19/11/2014" or "5/7/97"

    Returns:
        :class:`datetime.date`: date object

    """
    day, month, year = map(int, dstr.split("/"))
    if year < 100:  # 2-digit year.
        if year <= datetime.now().year:  # assume in 21st century
            year = year + 2000
        else:  # assume in 20th century
            year = year + 1900
    return date(year, month, day)


def date_to_decimal(d):
    """Convert :class:`datetime.date` to a decimal number of days since
    1st Jan 1900.

    Args:
        d (:class:`datetime.date`): date object

    Returns:
        float: floating point number of days since 1st Jan 1900.

    """
    if isinstance(d, pd.Timestamp):
        d = d.date()
    return (d - date(1900, 1, 1)).days


def decimal_to_date(dec):
    """Convert decimal number of days since 1st Jan 1900 to
    :class:`datetime.date`.

    Args:
        dec (float): floating-point number of days since
            1st January 1900.

    Returns:
        :class:`datetime.date`: date object

    """
    return date(1900, 1, 1) + timedelta(days=dec)


def date_to_wateruseyear(d):
    """Convert :class:`datetime.date` to water-use year as string.

    e.g. date(2016, 5, 3) -> "2015-16", while date(2016, 11, 1) -> "2016-17"

    Args:
        d (:class:`datetime.date`): date

    Returns:
        str: financial/water-use year e.g. "2019-20"

    """
    year = d.year
    if d.month >= 7:
        return "{}-{}".format(year, str(year + 1)[2:])
    else:
        return "{}-{}".format(year - 1, str(year)[2:])


def date_to_season(d):
    """Convert :class:`datetime.date` object to the season.

    Args:
        d (:class:`datetime.date`): date

    Returns:
        str: either "summer", "autumn", "winter" or "spring"

    """
    if d.month <= 2:
        return "summer"
    elif d.month <= 5:
        return "autumn"
    elif d.month <= 8:
        return "winter"
    elif d.month <= 11:
        return "spring"
    else:
        return "summer"


months_to_seasons = {
    1: "summer",
    2: "summer",
    3: "autumn",
    4: "autumn",
    5: "autumn",
    6: "winter",
    7: "winter",
    8: "winter",
    9: "spring",
    10: "spring",
    11: "spring",
    12: "summer",
}
"""Conversion map of months to seasons; keys are zero-indexed month numbers
 e.g. January is 1, and values are the season e.g. "summer"."""


def get_wu_year_from_month_and_year(df, year_col="year", month_col="month"):
    """Convert year and month from a pandas DataFrame to the water-use/financial
    year.

    Args:
        df (pandas DataFrame): must contain *year_col* with years as integers
            and *month_col* with months as integers.
        year_col (str): name of year column
        month_col (str): name of month column

    Returns:
        pd.Series: pandas Series of water-use years e.g. "2017-18"

    """
    to_wu_year = lambda y: f"{y}-{str(y + 1)[2:]}"
    return df.apply(
        lambda row: to_wu_year(row[year_col])
        if row[month_col] >= 7
        else to_wu_year(row[year_col] - 1),
        axis="columns",
    )


def get_spanning_dates(
    date_series: pd.Series, year_type: str = "calendar"
) -> pd.DatetimeIndex:
    """Given a pandas Series of datetimes, return a DatetimeIndex which
    spans all the days within the range of years that *date_series*
    spans.

    Args:
        date_series (pd.Series): a sequence of dates
        year_type (str): either 'calendar' or 'financial' - defines what
            'year' means

    Returns:
        pd.DatetimeIndex: pandas DateTimeIndex of contiguous dates.

    e.g.

    .. code-block:: python

        >>> dates = pd.Series([pd.Timestamp(x) for x in ["2018-02-02"]])
        >>> print(dates)
        0   2018-02-02
        dtype: datetime64[ns]
        >>> get_spanning_dates(dates, year_type="calendar")
        DatetimeIndex(['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04',
                       '2018-01-05', '2018-01-06', '2018-01-07', '2018-01-08',
                       '2018-01-09', '2018-01-10',
                       ...
                       '2018-12-22', '2018-12-23', '2018-12-24', '2018-12-25',
                       '2018-12-26', '2018-12-27', '2018-12-28', '2018-12-29',
                       '2018-12-30', '2018-12-31'],
                      dtype='datetime64[ns]', length=365, freq='D')
        >>> get_spanning_dates(dates, year_type="financial")
        DatetimeIndex(['2017-07-01', '2017-07-02', '2017-07-03', '2017-07-04',
                       '2017-07-05', '2017-07-06', '2017-07-07', '2017-07-08',
                       '2017-07-09', '2017-07-10',
                       ...
                       '2018-06-21', '2018-06-22', '2018-06-23', '2018-06-24',
                       '2018-06-25', '2018-06-26', '2018-06-27', '2018-06-28',
                       '2018-06-29', '2018-06-30'],
                      dtype='datetime64[ns]', length=365, freq='D')

    """
    if year_type == "calendar":
        year_min = date_series.min().year
        year_max = date_series.max().year
        logger.debug(f"year_min {year_min}, year_max {year_max}")
        start_day = pd.Timestamp(year=year_min, month=1, day=1)
        finish_day = pd.Timestamp(year=year_max, month=12, day=31)
    elif year_type == "financial":
        first_day = date_series.min()
        last_day = date_series.max()
        if first_day.month >= 7:
            year_min = first_day.year
        else:
            year_min = first_day.year - 1
        if last_day.month >= 7:
            year_max = last_day.year + 1
        else:
            year_max = last_day.year
        logger.debug(f"year_min {year_min}, year_max {year_max}")
        start_day = pd.Timestamp(year=int(year_min), month=7, day=1)
        finish_day = pd.Timestamp(year=year_max, month=6, day=30)
    else:
        raise KeyError("year_type must be either 'calendar' or 'financial'")
    logger.debug(f"start_day: {start_day}, finish_day: {finish_day}")
    return pd.date_range(start_day, finish_day)


def find_missing_days(
    df: pd.DataFrame,
    dt_col: str = "timestamp",
    year_type: str = "financial",
    value_col: str = "value",
) -> pd.Series:
    """Find the number of missing days in a year from a daily dataset.

    Args:
        df (pd.DataFrame): table including dates and values
        dt_col (str): name of column in *df* which contains datetimes.
        year_type (str): what does "year" mean? either "financial" or
            "calendar"
        value_col (str): name of column in *df* which contains the data itself

    See :func:`wrap_technote.get_spanning_dates` for more information on
    the keyword argument *year_type*.

    Returns:
        pd.Series: pandas Series with the relevant *year_type* values as the index,
        and the number of missing days within each year.

    """
    all_days = get_spanning_dates(df[dt_col], year_type=year_type)
    day_is_missing = (
        df.set_index(dt_col).reindex(all_days)[value_col].isnull().reset_index()
    )
    day_is_missing["year"] = day_is_missing["index"].dt.year
    day_is_missing["wu_year"] = [
        date_to_wateruseyear(d) for d in day_is_missing["index"]
    ]
    year_type_col = {"financial": "wu_year", "calendar": "year"}[year_type]
    missing_days = day_is_missing.groupby([day_is_missing[year_type_col]]).sum()
    return missing_days[value_col]


def get_yearspans_between(first_year, last_year, span_length=10):
    """Get a list of the first year in a set of adjacent year-spans
    (e.g. decades) which encompass years between *first_year* and
    *last_year*.

    Args:
        first_year (int): first year to be included
        last_year (int): last year to be included
        span_length (int): length of a year-span e.g. 10 would be a
            decade

    Returns:
        iterator: iterates over the first years in the relevant year-spans.

    """
    assert span_length == int(span_length)
    first_decade = int(np.floor(first_year / span_length) * span_length)
    last_decade = int(np.ceil(last_year / span_length) * span_length)
    return range(first_decade, last_decade, span_length)


def filter_to_between_years(df, first_year, last_year, dt_col="obs_date"):
    """Filter out rows which are not between two years.

    Args:
        df (:class:`pandas.DataFrame`): data.
        first_year (int): start of range of years to keep (inclusive).
        last_year (int): end of range of years to keep (inclusive)
        dt_col (str): name of *df* columns containing datetimes

    Returns:
        :class:`pandas.DataFrame`: a filtered view of df

    """
    return df[(df[dt_col].dt.year >= first_year) & (df[dt_col].dt.year <= last_year)]


def load_qc_removals(
    df,
    qc,
    parameter,
    dt_col="obs_date",
    data_validation_filename="Data_validation",
    conn=None,
):
    """Load and parse validation rules from the Data_validation spreadsheet(s).

    Arguments:
        df (pandas DataFrame): data table to apply removals to
        qc (either
            :class:`wrap_technote.ReportingPeriod` or
            :class:`wrap_technote.Resource`): data validation QC
            information.
        parameter (str): either "WL" or "TDS"
        dt_col (str): column of *df* with datetimes
        data_validation_filename (str): name of data validation file stem
        conn (dew_gwdata.SAGeodataConnection): database connection

    Returns:
        list: a list of dicts. Each dict specfies the labels to be removed from
        *df*, in a format designed for :func:`filter_wl_observations` and
        :func:`filter_tds_observations`.

    What type of rules are parsed by this function? Each row of the QC table
    should have at least these field names: "well_id", "action", "comment",
    "database", "start_period", and "end_period". The string in "well_id" will
    be parsed by :meth:`dew_gwdata.SAGeodataConnection.find_wells`, and each
    rule will be applied to data from those wells.

    1. "action" == "Exclude well" - this will remove all data from these wells.
    2. "action" == "Remove sample_no 12345" - this will remove the (salinity)
       record with sample_no 12345. Obviously you should substitute the correct
       sample_no.
    3. "action" == "Remove extract_method BAIL" - this will remove the
       (salinity) records with extract_method "BAIL". Obviously you can
       substitue other types of extract_method.
    4. "action" == "Remove period of data" - this will remove all data between
       "start_period" and "end_period", from the database mentioned in
       "database" (can be either "SA Geodata" or "Aquarius")
    5. "action" == "Remove period of data [keep final sample]" - this will
       remove all data between "start_period" and "end_period" except for the
       record which has "[final sample]" in the comment field from SA Geodata
       e.g. for a pumping test. Removals will only be applied from the database
       mentioned in "database" (can be either "SA Geodata" or "Aquarius")

    Note that this function doesn't actually remove data - it is the above
    functions (:func:`filter_wl_observations` and
    :func:`filter_tds_observations`) that apply the list of removals returned
    from this function.

    """
    if conn is None:
        import dew_gwdata

        conn = dew_gwdata.sageodata()

    removals = []
    logger.debug("Starting load_qc_removals()")
    data_val = qc.read_table(data_validation_filename)
    data_val = data_val[data_val.parameter == parameter]
    logger.debug(f"Length of data_val table: {len(data_val)}")
    for val_idx, row in data_val.iterrows():
        logger.debug(f"Parsing validation rule: {row.to_dict()}")

        applicable_well_ids = conn.find_wells(row.well_id)
        if len(applicable_well_ids) == 0:
            logger.warning(f"No drillhole identified for data_validation row {row}")
            continue
        applicable_wells = conn.drillhole_details(applicable_well_ids)

        reason = f"{row.action}: {row.comment}"

        if "Exclude well" in str(row.action):
            removals.append(
                {
                    "reason": reason,
                    "idx": (df.unit_long.isin(applicable_wells.unit_long)),
                    "well_ids": ", ".join(applicable_wells.well_id),
                }
            )
        if "Remove sample_no" in str(row.action):
            sample_no = int(str(row.action).split()[-1])
            removals.append(
                {
                    "reason": reason,
                    "idx": (df.sample_no == sample_no),
                    "well_ids": ", ".join(applicable_wells.well_id),
                }
            )

        if "Remove extract_method" in str(row.action):
            extract_method = str(row.action).split()[-1]
            removals.append(
                {
                    "reason": reason,
                    "idx": (df.extract_method == extract_method),
                    "well_ids": ", ".join(applicable_wells.well_id),
                }
            )

        start_date = row.start_period
        end_date = row.end_period
        if type(start_date) == str:
            start_date = datetime.strptime(start_date, "%d/%m/%Y")
        if type(end_date) == str:
            end_date = datetime.strptime(end_date, "%d/%m/%Y")
        logger.debug(
            f"start_date type={type(start_date)} end_date type={type(end_date)}"
        )

        if "Remove period of data" in str(row.action):
            if "keep [final sample]" in str(row.action):
                idx = (
                    (df.unit_long.isin(applicable_wells.unit_long))
                    & (
                        df["database"].isin(
                            [d.strip() for d in str(row.database).split(",")]
                        )
                    )
                    & (df[dt_col] >= start_date)
                    & (df[dt_col] <= end_date)
                    & (~df.comments.astype(str).str.contains(r"\[final sample\]"))
                )
            else:
                idx = (
                    (df.unit_long.isin(applicable_wells.unit_long))
                    & (
                        df["database"].isin(
                            [d.strip() for d in str(row.database).split(",")]
                        )
                    )
                    & (df[dt_col] >= start_date)
                    & (df[dt_col] <= end_date)
                )

            removals.append(
                {
                    "reason": reason,
                    "idx": idx,
                    "well_ids": ", ".join(applicable_wells.well_id),
                }
            )
    for removal in removals:
        logger.debug(
            f"QC Removal:\n"
            f"\treason: {removal['reason']}\n"
            f"\twell_ids: {removal['well_ids']}\n"
            f"\tidx == True: {removal['idx'][removal['idx'] == True]}"
        )
    return removals


class WellSelectionQuery:
    """Select wells using a resource definition.

    Args:
        resource (either pd.Series, dict): the
            resource for which we are finding wells.
        key (str): resource key (optional)
        shapefile_path (str): default ".", where to find the shapefile referenced
            below
        resource_key (str): resource key (optional, alias for "key" argument)
        resource (str): resource key (optional, alias for "key" argument)
        parameter (str): either "WL" (water level) or "TDS" (salinity)
        where_1 (str): first clause for SA Geodata query (see below)
        where_2 (str): second clause for SA Geodata query (see below), optional
        shapefile (str): path to shapefile, optional
        shapefile_field (str): name of shapefile field to filter on (optional)
        shapefile_value (str): value or comma-separated list values within
            "shapefile_field" column to filter by
        additional_wells (str): additional wells to include (will be parsed
            by :meth:`sageodata_db.SAGeodataConnection.find_wells`)
        include_replacements (bool): include replaced wells in the data retrieved.

    Attributes:
        where (str): the full where clause (without the verb "WHERE")

    The arguments above which come from the resource definition are:

    - parameter
    - where_1
    - where_2
    - shapefile
    - shapefile_field
    - shapefile_value
    - additional_wells

    The SA Geodata query is run across a join of the views dhdb.dd_drillhole_vw
    as dh and dhdb.dd_drillhole_summary_vw as summ.

    .. todo::

        simplify this. You should be able to pass it the :class:`wrap_technote.Resource`
        object alone.

    """

    N_OBS_QUERY = """SELECT
        subquery.n_obs,
        dh.drillhole_no,
        dh.dhp_exists_stage_1,
        dh.dhp_no,
        dh.conf_ind,
        dh.deletion_ind,
        dh.map_100000_no,
        dh.plot_1,
        dh.plot_2,
        dh.dh_seq_no,
        dh.unit_no,
        dh.strata_sample_seq_no,
        dh.obs_well_plan_code,
        dh.obs_well_seq_no,
        dh.dh_name1,
        dh.dh_name2,
        dh.dh_name3,
        dh.dh_name,
        dh.peps_well_id,
        dh.peps_devtype,
        dh.peps_devnumb,
        dh.peps_ind,
        dh.dh_other_name,
        dh.engineering_class,
        dh.mineral_class,
        dh.petroleum_class,
        dh.seismic_point_class,
        dh.stratigraphic_class,
        dh.water_point_class,
        dh.water_point_type_code,
        dh.water_well_class,
        dh.amg_easting,
        dh.amg_northing,
        dh.amg_zone,
        dh.lat_degrees,
        dh.lat_minutes,
        dh.lat_seconds,
        dh.long_degrees,
        dh.long_minutes,
        dh.long_seconds,
        dh.lat_deg_real,
        dh.long_deg_real,
        dh.neg_lat_deg_real,
        dh.parent_drillhole_no,
        dh.svy_accrcy_horiz,
        dh.svy_method_horiz_code,
        dh.hundred_name,
        dh.plan_type_code,
        dh.plan_no,
        dh.parcel_type_code,
        dh.parcel_no,
        dh.title_prefix,
        dh.title_volume,
        dh.title_folio,
        dh.hundred_no_old,
        dh.plan_type_code_old,
        dh.plan_no_old,
        dh.parcel_type_code_old,
        dh.parcel_no_old,
        dh.parcel_part_ind_old,
        dh.state_code_old,
        dh.map_250000_code,
        dh.state_code,
        dh.operator_code,
        dh.tenmt_type_code,
        dh.tenmt_no,
        dh.start_depth,
        dh.max_drilled_depth,
        dh.cored_length,
        dh.replacement_drillhole_no,
        dh.replacement_date,
        dh.drillers_log_exists_st1,
        dh.geochem_exists,
        dh.geochron_exists,
        dh.geolog_logging_exists,
        dh.geophys_logging_exists,
        dh.hydro_strat_exists,
        dh.hydro_unit_no,
        dh.mon_netwk_code,
        dh.penetr_hygeol_unit_ind,
        dh.project_no,
        dh.geotech_exists,
        dh.hydrogeol_exists,
        dh.headwork_exists,
        dh.sa_coal_ind,
        dh.palaeo_exists,
        dh.petrology_exists,
        dh.petrophysical_exists,
        dh.rock_sample_exists,
        dh.strata_sample_exists,
        dh.full_water_chem_anal_exists,
        dh.pumping_test_exists,
        dh.data_logger_exists,
        dh.water_qty_meter_exists,
        dh.well_constrn_insp_ind,
        dh.other_tests,
        dh.aquifer_storage_recovery,
        dh.pace_dh,
        dh.pace_round_no,
        dh.pace_proposal_no,
        dh.obswell_notes,
        dh.comments,
        dh.dentry_checked_by,
        dh.dentry_checked_date,
        dh.data_val_by,
        dh.data_val_date,
        dh.data_val_comment,
        dh.latest_open_depth,
        dh.latest_open_depth_date,
        dh.max_drilled_depth_date,
        dh.drilled_after_1992_ind,
        dh.mfiche_ver_by,
        dh.mfiche_ver_date,
        dh.orig_drilled_depth,
        dh.orig_drilled_date,
        dh.basement_depth,
        dh.basement_gtr_ind,
        dh.geolog_logging_by,
        dh.dhp_comments,
        dh.site_no,
        dh.artesian_ind,
        dh.site_map_100000_no,
        dh.map_50k_no,
        dh.map_10k_no,
        dh.map_2500_code,
        dh.map_1000_code,
        dh.min_upload_no,
        dh.prev_orig_drilled_depth,
        dh.prev_orig_drilled_date,
        dh.prev_max_drilled_depth,
        dh.prev_max_drilled_depth_date,
        dh.prev_latest_open_depth,
        dh.prev_latest_open_depth_date,
        dh.dh_creation_date,
        dh.dh_created_by,
        dh.dh_modified_date,
        dh.dh_modified_by,
        dh.tene_id,
        dh.drillhole_load_no,
        dh.drillhole_load_data_no,
        dh.water_drillhole_flag,
        dh.state_asset,
        dh.state_asset_status,
        dh.state_asset_retained,
        dh.state_asset_comments,
        dh.owner_code,
        dh.licensed_well_flag,
        dh.easement_ind,
        dh.land_access_agreement_ind,
        dh.prescribed_well_area_code,
        dh.presc_water_res_area_code,
        dh.nrm_region_code,
        dh.telemetered_flag,
        dh.swl_flag,
        dh.salinity_flag,
        dh.export_quality_flag,
        dh.wcr_load_no,
        dh.wcr_load_data_no,
        dh.basement_dep_conf,
        summ.deletion_ind,
        summ.confidential_flag,
        summ.source_data_change_time,
        summ.denorm_time,
        summ.global_pop,
        summ.primary_litho_log_no,
        summ.purpose_code1,
        summ.purpose_code2,
        summ.purpose_code3,
        summ.latest_status_date,
        summ.latest_status_code,
        summ.latest_yield_date,
        summ.latest_yield,
        summ.yield_extr_dur_hour,
        summ.yield_extr_dur_min,
        summ.yield_meas_method_code,
        summ.yield_extr_code,
        summ.latest_sal_date,
        summ.latest_ec,
        summ.latest_tds,
        summ.latest_ph_date,
        summ.latest_ph,
        summ.latest_swl_date,
        summ.latest_swl,
        summ.latest_rswl,
        summ.latest_dtw,
        summ.latest_dry_ind,
        summ.latest_ec_tds_sample_no,
        summ.latest_ground_elevation,
        summ.latest_elevation_date,
        summ.latest_ref_point_type,
        summ.latest_ref_elevation,
        summ.latest_case_fr,
        summ.latest_case_to,
        summ.latest_min_diam,
        summ.latest_permit_no,
        summ.latest_permit_ex,
        summ.latest_rework_date,
        summ.latest_screened,
        summ.shallowest_wat_cut_depth_from,
        summ.shallowest_wat_cut_depth_to,
        summ.aq_subaq,
        summ.data_logger_start_date,
        summ.data_logger_end_date,
        summ.db_dtw_data_logger,
        summ.db_yield_data_logger,
        summ.db_ec_data_logger,
        summ.db_temp_data_logger,
        summ.db_rain_data_logger,
        summ.db_hour_rain_data_logger,
        summ.db_logger_data,
        summ.db_telemetry_data,
        summ.db_drillers_log,
        summ.db_hydro_strat_log,
        summ.db_pumping_test,
        summ.db_core,
        summ.db_core_spectral_scanned,
        summ.min_core_spectral_scan_depth,
        summ.max_core_spectral_scan_depth,
        summ.db_core_hazard,
        summ.db_strat_log,
        summ.db_litho_log,
        summ.db_geophysical_log,
        summ.db_petrophysical_log,
        summ.db_dh_doc_image,
        summ.db_dh_doc_image_sarig,
        summ.db_easement_dh_doc_image,
        summ.db_land_acc_agree_dh_doc_image,
        summ.db_dh_image,
        summ.db_water_sample,
        summ.db_water_chem,
        summ.db_water_info,
        summ.db_rock_sample,
        summ.db_rock_geochem,
        summ.db_rock_geochem_major,
        summ.db_geochron,
        summ.db_biostrat_analysis,
        summ.db_biostrat_result,
        summ.db_biostrat_product,
        summ.db_biostrat_chart,
        summ.db_biostrat_palynology,
        summ.db_biostrat_foram,
        summ.db_petrology,
        summ.highest_declin_meas_no,
        summ.highest_declin_svy_depth,
        summ.highest_declin_from_horiz,
        summ.highest_azimuth,
        summ.target_commod_code1,
        summ.target_commod_code2,
        summ.target_commod_code3,
        summ.target_commod_code4,
        summ.target_commod_code5,
        summ.target_commod_name1,
        summ.target_commod_name2,
        summ.target_commod_name3,
        summ.target_commod_name4,
        summ.target_commod_name5,
        summ.drill_meth1,
        summ.drill_meth2,
        summ.drill_meth3,
        summ.drill_meth1_desc,
        summ.drill_meth2_desc,
        summ.drill_meth3_desc,
        summ.highest_priority_dh_doc1,
        summ.comments_dh_doc1,
        summ.info_type_code_dh_doc1,
        summ.doc_type_code_dh_doc1,
        summ.doc_ref_id_dh_doc1,
        summ.highest_priority_dh_doc2,
        summ.comments_dh_doc2,
        summ.info_type_code_dh_doc2,
        summ.doc_type_code_dh_doc2,
        summ.doc_ref_id_dh_doc2,
        summ.db_doc_refs,
        summ.db_dh_note,
        summ.bkf_ind,
        summ.db_obs_well,
        summ.dh_uf_denorm_time,
        summ.db_core_scan_results,
        summ.db_core_scan_interpretation,
        summ.db_core_scan_image,
        summ.db_core_image,
        summ.db_rock_sample_image,
        summ.db_dh_file,
        summ.earliest_well_date,
        summ.primary_class,
        gdh.group_code,
        gdh.stand_water_level_status,
        gdh.swl_freq,
        gdh.salinity_status,
        gdh.salinity_freq
    FROM dhdb.dd_drillhole_vw dh
    INNER JOIN dhdb.dd_drillhole_summary_vw summ ON dh.drillhole_no = summ.drillhole_no
    INNER JOIN dhdb.dd_drillhole_geodetic_vw gd ON dh.drillhole_no = gd.drillhole_no
    LEFT JOIN dhdb.dd_dh_group_vw gdh ON dh.drillhole_no = gdh.drillhole_no
    INNER JOIN
    (SELECT drillhole_no,
            Count(*) AS n_obs
    FROM
        ({subquery_select} )
    GROUP BY drillhole_no
    HAVING Count(*) >= {min_data_pts:.0f}) subquery ON dh.drillhole_no = subquery.drillhole_no
    {where_over_dh_summ}"""

    NO_PARAMETER_SUBQUERY = """SELECT drillhole_no 
        FROM dhdb.dd_drillhole_vw 
        WHERE deletion_ind = 'N'"""

    WL_SUBQUERY = """SELECT drillhole_no
        FROM dhdb.wa_water_level_vw
        WHERE obs_date BETWEEN date '{start_year:.0f}-01-01' AND date '{end_year:.0f}-12-31'
            AND series_type = 'T'
            AND (depth_to_water IS NOT NULL OR standing_water_level IS NOT NULL OR rswl IS NOT NULL)"""

    TDS_SUBQUERY = """SELECT drillhole_no
        FROM dhdb.sm_sample_vw
        WHERE collected_date BETWEEN date '{start_year:.0f}-01-01' AND date '{end_year:.0f}-12-31'
            AND series_type = 'T'
            AND (tds IS NOT NULL OR ec IS NOT NULL)"""

    def __init__(self, resource=None, shapefile_path=None, **kwargs):
        if shapefile_path is None:
            shapefile_path = Path(".")
        self.shapefile_path = shapefile_path
        logger.debug(f"setting shapefile_path = {self.shapefile_path}")
        if resource is not None:
            if isinstance(resource, dict):
                kwargs.update(resource)
            elif isinstance(resource, pd.Series):
                kwargs.update(resource.to_dict())
            elif isinstance(resource, pd.DataFrame):
                kwargs.update(resource.iloc[0].to_dict())
            else:
                raise KeyError("resource has to be a mapping type")
        for column in (
            "where_1",
            "where_2",
            "shapefile",
            "shapefile_field",
            "shapefile_value",
            "additional_wells",
            "include_replacements",
        ):
            value = kwargs.get(column, None)
            if str(value).strip() == "nan":
                value = None
            logger.debug(f"setting attr: {column} {value}")
            setattr(self, column, value)
        if "key" in kwargs:
            self.resource_key = kwargs["key"]
        elif "resource_key" in kwargs:
            self.resource_key = kwargs["resource_key"]

    @property
    def polygon_points(self):
        """Provide a list of the X, Y points in each polygon in the referenced
        and filtered shapefile.

        """
        polys = []
        # filename = str(Path(__file__).parent / "resources" / str(self.shapefile))
        filename = str(self.shapefile_path / str(self.shapefile))
        logger.debug("Loading polygons from {filename}")
        with shapefile.Reader(filename) as shp:
            for value in self.shapefile_value.split(","):
                value = value.strip()
                for sr in shp.shapeRecords():
                    if sr.record[self.shapefile_field] == value:
                        poly = sr.shape.points
                        polys.append(poly)
        return polys

    @property
    def polygon_coord_arrays(self):
        """Provide a list of X and Y arrays for each polygon in the referenced
        and filtered shapefile.

        """
        coord_arrays = []
        for poly in self.polygon_points:
            xs = []
            ys = []
            for x, y in poly:
                xs.append(x)
                ys.append(y)
            coord_arrays.append([xs, ys])
        return coord_arrays

    @property
    def polygons(self):
        """Provide a list of the :class:`shapely.geometry.Polygon` objects
        for each polygon in the referenced and filtered shapefile.

        """
        polys = []
        for points in self.polygon_points:
            polys.append(shapely.geometry.Polygon(points))
        return polys

    @property
    def where(self):
        """Final SQL WHERE clause."""
        if self.where_2:
            clause = f"{self.where_1} and ({self.where_2})"
        else:
            clause = self.where_1
        return clause

    def get_parameter_subquery(self, parameter):
        """Get SQL subquery for parameter.

        Args:
            parameter (str): either "WL" or "TDS"

        Returns:
            str: SQL subquery as a string.

        """
        if parameter == "WL":
            return self.WL_SUBQUERY
        elif parameter == "TDS":
            return self.TDS_SUBQUERY
        raise KeyError

    def sql(
        self,
        parameter=None,
        start_year=None,
        end_year=None,
        min_data_pts="auto",
        **kwargs,
    ):
        """Get SQL to find wells with at least *min_data_pts* for *parameter*
        between *start_year* and *end_year* (inclusive).

        Args:
            parameter (str): either "WL" or "TDS", see
                :meth:`wrap_technote.WellSelectionQuery.get_parameter_subquery`
            start_year (int): start year of period, inclusive
            end_year (int): end year of period, inclusive
            min_data_pts (int): minimum number of data points in the period,
                or "auto" which will use at least one per year.

        Returns:
            str: SQL query as string.

        """
        if parameter is not None:
            assert start_year is not None
            assert end_year is not None

        if min_data_pts == "auto":
            if parameter is None:
                min_data_pts = 1
            else:
                min_data_pts = (end_year - start_year) + 1

        if parameter is None:
            parameter = "NO_PARAMETER"
            subquery = self.get_parameter_subquery(parameter)
            where_over_dh_summ = f"WHERE {self.where}"
        else:
            subquery = self.get_parameter_subquery(parameter).format(
                start_year=start_year, end_year=end_year
            )
            where_over_dh_summ = f"WHERE {self.where}"

        return self.N_OBS_QUERY.format(
            subquery_select=subquery,
            min_data_pts=min_data_pts,
            where_over_dh_summ=where_over_dh_summ,
        )

    def find_wells(self, *args, conn=None, **kwargs):
        """Find wells using :meth:`dew_gwdata.SAGeodataConnection.find_wells`.

        Args:
            parameter (str): "WL", "TDS", or None
            min_data_pts (int): can be None for parameter None
            start_year (int): can be None for parameter None
            end_year (int): can be None for parameter None

        Returns:
            :class:`pandas.DataFrame`: the dataframe returned by
            :meth:`dew_gwdata.SAGeodataConnection.drillhole_details`.

        See :meth:`wrap_technote.WellSelectionQuery.sql` for details
        of these keyword arguments.

        It will also filter by the "shapefile" etc. fields in the
        original query.

        """
        if conn is None:
            import dew_gwdata

            conn = dew_gwdata.sageodata()
        query = self.sql(*args, **kwargs)
        table = conn.query(query)
        keep_ix = []
        if self.shapefile:
            for poly in self.polygons:
                for ix, row in table.iterrows():
                    if poly.contains(
                        shapely.geometry.Point(row.long_deg_real, row.neg_lat_deg_real)
                    ):
                        keep_ix.append(ix)
            table = table.iloc[keep_ix]
        dh_nos = list(table.drillhole_no)
        if self.additional_wells:
            dh_nos += list(conn.find_wells(self.additional_wells).dh_no)
        return conn.drillhole_details(dh_nos).drop_duplicates()


class Seasons:
    """Define seasonal periods e.g. "summer" and "recovery".

    Args:
        periods (sequence of dicts, optional): see
            :meth:`wrap_technote.Seasons.append`
            for a definition of each dict here

    Attributes:
        dayofyear_map (dict): mapping from day of year
            (int) to tuple (period number, period dict).
        dayofyear_season_map (dict): mapping from day of year
            (int) to season (str).

    Example:

    .. code-block:: python

        >>> from wrap_technote import doy
        >>> seasons = (
        ...     wrap_technote.Seasons()
        ...     .append("summer", "min", end=doy("2018-05-15"), marker="v", color="red")
        ...     .append("recovery", "max", marker="^", color="blue")
        ... )
        >>> seasons.periods
        [{'season': 'summer',
          'start': 1,
          'end': 135,
          'func': 'min',
          'marker': 'v',
          'color': 'red'},
         {'season': 'recovery',
          'start': 135,
          'end': 366,
          'func': 'max',
          'marker': '^',
          'color': 'blue'}]

    """

    def __init__(self, periods=None):
        if periods is None:
            periods = []
        self.periods = periods
        self.generate_dayofyear_map()

    @property
    def period_kws(self):
        """

        .. todo:: Document this property.

        """
        p = {}
        for period in self.periods:
            season = period["season"]
            if not season in p:
                p[season] = {}
            p[season].update(
                {
                    k: v
                    for k, v in period.items()
                    if not k in ("start", "end", "func", "season")
                }
            )
            if not "marker" in p[season]:
                if "recover" in season.lower():
                    p[season]["marker"] = "^"
                    p[season]["color"] = "blue"
                elif (
                    "pump" in season.lower()
                    or "stress" in season.lower()
                    or "summer" in season.lower()
                ):
                    p[season]["marker"] = "v"
                    p[season]["color"] = "red"
        return p

    @property
    def spanning(self):
        """If the first seasonal period of the year is the same as
        the last seasonal period of the year, then this is true.

        Returns:
            bool

        """
        if len(self.periods) == 1:
            return False
        elif self.periods[0]["season"] == self.periods[-1]["season"]:
            return True
        else:
            return False

    def generate_dayofyear_map(self):
        """Internal-use method to generate a mapping of
        the season for each day of the year.

        It creates or updates dictionaries stored as the
        attributes :attr:`wrap_technote.Seasons.dayofyear_map`
        and :attr:`wrap_technote.Seasons.dayofyear_to_season`.

        Returns:
            dict: keys are the day numbers of the year, from 1 to
            366; values are the season.

        """

        self.dayofyear_map = {}
        for i, period in enumerate(self.periods):
            for j in range(period["start"], period["end"] + 1):
                self.dayofyear_map[j] = (i, period["season"])
        self.dayofyear_to_season = {}
        for k, (i, s) in self.dayofyear_map.items():
            self.dayofyear_to_season[k] = s

    def label_year(self, dt):
        """Generate a label of the year based on the season definition.

        Args:
            dt (:class:`datetime.datetime`)

        Returns:
            str: a string in the format of either year "2019" or the spanning
            year e.g. "2019-20", if the season spans the end of the calendar
            year.

        """
        year = dt.year
        doy_ = dt.dayofyear
        if doy_ == 366:
            doy_ = 365
        i, season = self.dayofyear_map[doy_]
        if self.spanning:
            if i == 0:
                year = f"{year - 1}-{str(year)[-2:]}"
            if i == (len(self.periods) - 1):
                year = f"{year}-{str(year + 1)[-2:]}"
        else:
            year = str(year)
        return f"{year}"

    def label_year_and_season(self, dt):
        """Generate a label of the year and season
        for a given date.

        Args:
            dt (:class:`datetime.datetime`)

        Returns:
            str: a string in the format "{year}-{season}" e.g.
            "2019-recovery"

        """
        year = dt.year
        doy_ = dt.dayofyear
        if doy_ == 366:
            doy_ = 365
        i, season = self.dayofyear_map[doy_]
        if self.spanning:
            if i == 0:
                year = f"{year - 1}-{str(year)[-2:]}"
            if i == (len(self.periods) - 1):
                year = f"{year}-{str(year + 1)[-2:]}"
        else:
            year = str(year)
        return f"{year}-{season}"

    def append(self, season, func, start=None, end=None, **kws):
        """Add a new seasonal period.

        Args:
            season (``str``): name of the season e.g. "recovery",
                "summer"
            func (str): reduction function which is used to
                reduce the observations in a single seasonal period
                to one value. For example, if the season contains
                recovered water levels and the parameter being
                analysed is RSWL in elevation, then the appropriate
                function would be "max". The value should be a string
                which is in the ``SEASONAL_REDUCTION_FUNCS`` constant in
                this module. If it is "none", then the observations are
                not reduced to a single value.
            start (int): day of the year on which the period begins
            end (int): day of the year on which the period ends

        Returns:
            :class:`wrap_technote.Seasons`: returns itself, to allow
            chaining this method.

        If *start* is omitted, the period will immediately follow
        whatever the most recently defined period is. Or if there
        are no other periods, it will start on Jan 1.

        If *end* is omitted, the period will end on December 31st.

        """
        if start is None:
            if len(self.periods) == 0:
                start = 1
            else:
                start = self.periods[-1]["end"]
        if end is None:
            end = 365
        self.periods.append(
            dict({"season": season, "start": start, "end": end, "func": func}, **kws)
        )
        self.generate_dayofyear_map()
        return self

    @property
    def funcs(self):
        d = {}
        for period in self.periods:
            d[period["season"]] = period["func"]
        return d

    def apply_season_func(
        self, df, data_col="rswl", season_col="season", dt_col="obs_date"
    ):
        """Reduce multiple observations in a seasonal period
        to a single record, if the seasonal reduction function is not "all".

        Args:
            df (:class:`pandas.DataFrame`)
            data_col (``str``): column of *df* with data values
            season_col (``str``): column of *df* which contains the
                season of each observation. This is used to look up
                the reduction function (see :meth:`wrap_technote.Seasons.append`
                for more details)
            dt_col (``str``): column of *df* with datetime for the situation where the
                reduction function results in a new date i.e. "mean"

        Returns:
            either a pd.DataFrame (if reduction function == "all"), otherwise
            a pd.Series.

        This function is intended to be used with :meth:`pandas.DataFrame.apply`.

        """
        season = df[season_col].iloc[0]
        func_name = self.funcs[season]
        if func_name != "all":
            func = SEASONAL_REDUCTION_FUNCS[func_name]
            if func_name in ("max", "min"):
                result = df[df[data_col] == func(df[data_col])]
                if len(result):
                    return result.iloc[0]
                else:
                    return None
            elif func_name in ["mean"]:
                data_value = func(df[data_col].values)
                dtdec_values = [date_to_decimal(d) for d in df[dt_col]]
                dtdec_value = func(dtdec_values)
                dt_value = pd.Timestamp(decimal_to_date(dtdec_value))
                record = df.iloc[0]
                record[dt_col] = dt_value
                record[data_col] = data_value
                return record
        else:
            return df[data_col]

    @property
    def seasons(self):
        return list(set([p["season"] for p in self.periods]))

    def to_json(self):
        """Save the definition of this seasonal variation to JSON.

        Returns:
            str: JSON as a string

        """
        return json.dumps(self.periods)

    @classmethod
    def from_json(cls, txt):
        """Create a :class:`wrap_technote.Seasons` object from
        JSON.

        Args:
            txt (str or filename)

        Returns:
            :class:`wrap_technote.Seasons` object

        """
        if os.path.isfile(txt):
            with open(txt, "r") as f:
                return cls.from_json(f.read())
        else:
            return cls(json.loads(txt))

    def __str__(self):
        parts = "/".join(
            [
                f"{p['season']}:{doy_to_non_leap_year(p['start'])}"
                f"-{doy_to_non_leap_year(p['end'])}"
                for p in self.periods
            ]
        )
        return "S/" + parts

    def to_str(self):
        """Create a string definition for a simple recovery season
        definition e.g. one period per year.

        Returns:
            str:

        See :meth:`wrap_technote.Seasons.from_str` for the format of the string.

        """
        elements = []
        for period in self.periods:
            elements.append(
                f"{period['season']} to {doy_to_non_leap_year(period['end'])}"
            )
        return ", ".join(elements)

    @property
    def reduces_to_one_value_per_season(self):
        for func_name in self.funcs.values():
            if func_name != "all":
                return True
        return False

    @classmethod
    def from_str(cls, s):
        """Create a :class:`wrap_technote.Seasons` object from a
        simple string definition.

        Args:
            s (str): comma separated seasons starting from Jan 1 and the last
                must end on Dec 31

        Returns:
            :class:`wrap_technote.Seasons` object

        Example definitions:

        "pumping(min) to May 31, recovery(max) to Dec 31"

        "recovery(max) to Jan 31, pumping(min) to Jul 14, recovery(max) to Dec 31"

        """
        append_arguments = []
        elements = s.split(",")
        for e in elements:
            name = e.strip().split()[0]
            func = re.search(r"\(([a-z]*)\)", name.lower()).group(1)
            if "recovery" in name.lower():
                name = "recovery"
                kws = {"color": "blue"}
            elif "pumping" in name.lower():
                name = "pumping"
                kws = {"color": "pink"}
            else:
                kws = {"color": "gray"}
            if func == "min":
                kws["marker"] = "v"
            elif func == "mean":
                kws["marker"] = "s"
            elif func == "max":
                kws["marker"] = "^"
            date_match = re.search(
                r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ?[0-9]{1,2}", e
            )
            if date_match:
                kws["end"] = doy(date_match.group())
                append_arguments.append(((name, func), kws))
            else:
                raise KeyError("did not find a date match!")
        obj = cls()
        for args, kwargs in append_arguments:
            obj = obj.append(*args, **kwargs)
        return obj


def rank_and_classify(df, param_name="rswl", param_col="rswl", dt_col="year+season"):
    """Rank and classify against BoM decile groups.

    Args:
        s (pandas.Series): data
        param_name (str): name of data to be used.

    Returns:
        pd.DataFrame: dataframe, with a column for the percentile and another for
        the BoM decile class.

    """
    if param_name != "":
        param_name += "_"
    new_df = df[[dt_col, param_col]].copy()
    percentile_col = f"{param_name}percentile"
    bom_class_col = f"{param_name}bom_class"
    new_df[percentile_col] = df[param_col].rank(pct=True) * 100
    new_df[bom_class_col] = percentile_to_bom_class(new_df[percentile_col])
    return new_df


def calc_well_record_quality(
    df,
    years_to_extract=(),
    unique_grouper=None,
    dt_col="obs_date",
    spans_to_count_in=(),
):
    """Calculate statistics of the quality of the record
    of observations for a single well.

    Args:
        df (:class:`pandas.DataFrame`): observed measurements
        unique_grouper (``str``): argument to ``df.groupby()`` which will
            split the dataframe appropriately. If you are grouping by year,
            the correct value here could be ``df[dt_col].dt.year`` (this is the
            default). If you
            have already calculated using a seasonal definition function
            like :func:`wrap_technote.analyse_wl_by_seasons`, the value should
            be the column "year+season".
        dt_col (``str``): column of *df* containing datetimes
        years_to_extract (sequence of ints): for each year in this sequence,
            a statistic column will be produced with a boolean value
            indicating whether there was an observation in that year.
        spans_to_count_in (sequence of 2-tuples): for each span of years in this
            sequence, calculate how many years have observations.

    Returns:
        :class:`pandas.DataFrame`: a dataframe with with statistic columns:

        - "n_years_with_obs": number of years in record with an observation
        - "first_year": first year with an observation
        - "max_gap_years": largest gap in years between years with observations
        - "mean_gap_years": average gap in years between years with observations
        - "obs_in_XXXX": whether or not there was an observation in
          year XXXX

    """
    logger.debug(f"unique_grouper = {unique_grouper}")
    if unique_grouper is None:
        unique_grouper = df[dt_col].dt.year
    logger.debug(f"Final unique_grouper = {unique_grouper}")

    # Group the observation by years, so there is a single row per year:
    if dt_col == "season_year":
        obs_1_per_year = (
            df.groupby(unique_grouper)[dt_col].first().str[:4].astype(int).to_list()
        )
    else: # assume it is a datetime column
        obs_1_per_year = df.groupby(unique_grouper)[dt_col].first().dt.year.to_list()

    logger.debug(f"{df.well_id.iloc[0]}: obs_1_per_year = \n{obs_1_per_year}")

    # Calculate gaps between observations, in years. There should not be any zeroes.
    year_gaps = np.diff(np.sort(obs_1_per_year))
    results = {
        "first_year": np.min(obs_1_per_year),
        "max_gap_years": np.nan,
        "mean_gap_years": np.nan,
    }
    if dt_col == "obs_date":
        results["n_years_with_obs"] = len(df.groupby(df[dt_col].dt.year).first())
    elif dt_col == "season_year":
        results["n_years_with_obs"] = len(df.groupby(df[dt_col]).first())
    if len(year_gaps):
        results.update(
            {"max_gap_years": year_gaps.max(), "mean_gap_years": np.mean(year_gaps)}
        )
    for year in years_to_extract:
        results[f"obs_in_{year}"] = year in obs_1_per_year
        results[f"n_obs_in_{year}"] = int(year in obs_1_per_year)

    for year0, year1 in spans_to_count_in:
        results[f"n_obs_btwn_{year0}_{year1}"] = len(
            [x for x in obs_1_per_year if (x >= year0) and (x <= year1)]
        )
    series = pd.Series(results).fillna(0)
    logger.debug(f"{df.well_id.iloc[0]} - final result: \n{series.to_dict()}")
    return series


def linear_trend(
    ddf, param_col="rswl", dt_col="ndays", regression_method="least-squares"
):
    """Calculate linear trend line.

    Args:
        ddf (pandas DataFrame): contains data to calculate trend against.
        param_col (str): column containing dependent value
        dt_col (str): column containing independent values
        regression_method (str): either "least-squares" or "L2" for ordinary least squares
            or "least-absolute-deviation" or "L1" for deviation

    Returns:
        pd.Series: pandas Series containing columns "slope_yr_ndays", "y_int_ndays", and
        "slope_yr".

    """
    ddf = ddf.sort_values(dt_col)
    x = ddf[dt_col].values
    y = ddf[param_col].values
    regression_methods = ("least-squares", "least-absolute-deviation")
    if regression_method == "least-squares":
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            x,
            y,
        )
    elif regression_method == "least-absolute-deviation":
        # Use OLS parameters for a starting point for LAD fitting (L1 norm)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        def model(data, *curve_parameters):
            m, c = curve_parameters
            return data * m + c

        def cost_function(curve_parameters, input_data, observed_outputs):
            predicted_outputs = model(input_data, *curve_parameters)
            return np.sum(np.abs(predicted_outputs - observed_outputs))

        output = optimize.minimize(cost_function, (slope, intercept), args=(x, y))
        slope, intercept = output.x
    else:
        raise KeyError(f"regression_method must be one of {regression_methods}")
    return pd.Series(
        {"slope_yr_ndays": slope, "y_int_ndays": intercept, "slope_yr": slope * 365.25}
    )


def calculate_trendline_at_dates(trend_line, datetimes):
    """Calculate the value for a given linear trend at certain dates.

    Args:
        trend_line (pandas Series): a row from the result of
            :meth:`wrap_technote.Resource.apply_trend`.
        datetimes (sequence of datetimes): predict value for each of
            these

    Returns:
        numpy.ndarray: numpy array of values, same length as `datetimes`.

    """
    timestamps = [pd.Timestamp(dt) for dt in datetimes]
    ndays = np.asarray([date_to_decimal(ts.date()) for ts in timestamps])
    func = lambda nday: nday * trend_line["slope_yr_ndays"] + trend_line["y_int_ndays"]
    return np.array([func(nday) for nday in ndays])


def get_median_ranking(curr_ranks, rank_classes="BoM", closed_at_end="lower"):
    """Return the median water level ranking for a set of wells.

    Args:
        curr_ranks (pd.Series): must contain the rank classes
        rank_classes (iterable or 'BoM'): if 'BoM', this will use
            the BoM classifications, otherwise it should be a list, in
            order, of the ranking classes.
        closed_at_end (str): either 'upper' or 'lower'; if the median
            well sits between two ranking classes, e.g. 50% of wells
            are 'Lowest on record' and 50% are 'Highest on record', then
            how do we resolve it? If 'lower' then the interval is closed on the
            lower boundary, and in this case the result would be 'Highest on record'.
            If 'upper' then the interval is closed on the upper
            boundary and in this case the result would be 'Lowest on record'.

    Return:
        str: one of the BoM decile range classes: "Lowest on record",
        "Very much below average", "Below average", "Average", "Above average",
        "Very much above average", "Highest on record".

    """
    if rank_classes == "BoM":
        rank_classes = [
            "Lowest on record",
            "Very much below average",
            "Below average",
            "Average",
            "Above average",
            "Very much above average",
            "Highest on record",
        ]
    assert closed_at_end in ("upper", "lower")
    class_counts = {r: 0 for r in rank_classes}
    class_counts.update(curr_ranks.value_counts().to_dict())
    bc_counts = [class_counts[x] for x in rank_classes]
    percentage_counts = [
        y / sum(bc_counts) * 100 if sum(bc_counts) > 0 else 0 for y in bc_counts
    ]
    cum_sums = np.cumsum(percentage_counts)
    for i in range(len(cum_sums)):
        if closed_at_end == "lower":
            if cum_sums[i] > 50:
                return rank_classes[i]
        elif closed_at_end == "upper":
            if cum_sums[i] >= 50:
                return rank_classes[i]


def get_median_trend_triclass(
    trends, classes=("Declining", "Stable", "Rising"), closed_at_end="lower"
):
    """Return the median triclass trend value for a set of wells.

    Args:
        trends (pd.Series): data
        classes (iterable): list of the class values.
        closed_at_end (str): either 'upper' or 'lower'; if the median
            well sits between two classes, e.g. 50% of wells
            are 'Declining' and 50% are 'Rising', then
            how do we resolve it? If 'lower' then the interval is closed on the
            lower boundary, and in this case the result would be 'Rising'.
            If 'upper' then the interval is closed on the upper
            boundary and in this case the result would be 'Declining'.

    Return:
        str: the relevant triclass from *classes*

    """
    assert closed_at_end in ("upper", "lower")
    class_counts = {r: 0 for r in classes}
    class_counts.update(trends.value_counts().to_dict())
    bc_counts = [class_counts[x] for x in classes]
    percentage_counts = [y / sum(bc_counts) * 100 for y in bc_counts]
    cum_sums = np.cumsum(percentage_counts)
    for i in range(len(cum_sums)):
        if closed_at_end == "lower":
            if cum_sums[i] > 50:
                return classes[i]
        elif closed_at_end == "upper":
            if cum_sums[i] >= 50:
                return classes[i]


def get_median_class(class_counts, class_values="use-index", closed_at_end="lower"):
    """Return the median class value for a list of class counts.

    Args:
        class_counts (pd.Series): data
        class_values (iterable): list of the class values or 'use-index' to use
            the index on `class_counts`.
        closed_at_end (str): either 'upper' or 'lower'; if the median
            well sits between two classes, e.g. 50% of wells
            are 'class1' and 50% are 'class2', then
            how do we resolve it? If 'lower' then the interval is closed on the
            lower boundary, and in this case the result would be 'class2'.
            If 'upper' then the interval is closed on the upper
            boundary and in this case the result would be 'class1'.

    Return:
        str: the median class

    """
    assert closed_at_end in ("upper", "lower")
    if str(class_values) == "use-index":
        class_values = class_counts.index.values
    class_counts_dict = {r: 0 for r in class_values}
    # logger.debug(f"class_counts_dict {class_counts_dict}")
    for i, class_value in enumerate(class_values):
        v = class_counts.iloc[i]
        if v:
            class_counts_dict[class_value] = v
    # class_counts_dict.update(
    #     {k: v for k, v in class_counts.to_dict().items() if not np.isnan(v)}
    # )
    # logger.debug(f"class_counts_dict {class_counts_dict}")
    bc_counts = [class_counts_dict[x] for x in class_values]
    # logger.debug(f"bc_counts {bc_counts}")
    percentage_counts = [y / np.nansum(bc_counts) * 100 for y in bc_counts]
    # logger.debug(f"percentage_counts {percentage_counts}")
    cum_sums = np.cumsum(
        percentage_counts,
    )
    for i in range(len(cum_sums)):
        if closed_at_end == "lower":
            if cum_sums[i] > 50:
                return class_values[i]
        elif closed_at_end == "upper":
            if cum_sums[i] >= 50:
                return class_values[i]


def get_majority_categories(trends):
    """Return majority category or categories for a set of trends.

    Args:
        trends (pd.DataFrame): dataframe with column "n_wells"
            and the name of the category as the index.

    Returns:
        pd.DataFrame ?

    .. todo:: check return arguments.

    """
    # There could be more than one "majority" trend category.
    maj_tr3 = trends[trends.n_wells == trends.n_wells.max()]
    if len(maj_tr3) == 1:
        maj_category = maj_tr3.iloc[0].name.lower()
    elif len(maj_tr3) == 2:
        cats = sorted(maj_tr3.index.values)
        maj_category = f"{cats[0].lower()} and {cats[1].lower()}"
    elif len(maj_tr3) == 3:
        cats = sorted(maj_tr3.index.values)
        maj_category = f"{cats[0].lower()}, {cats[1].lower()}, and {cats[2].lower()}"
    m = maj_tr3.sum()
    m.name = maj_category
    return m


decimal_words = (
    pd.read_csv(Path(__file__).parent / "decimal_word.csv").set_index("decimal").word
)
