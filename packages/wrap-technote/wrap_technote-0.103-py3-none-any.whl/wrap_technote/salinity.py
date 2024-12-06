from collections import namedtuple
from pathlib import Path
import logging

# import datatest
import dew_gwdata as gd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import ticker as mticker

# import pytest
from matplotlib import gridspec
import wrap_technote as tn

from scipy import optimize, stats

from .utils import *
from .gwutils import *

logger = get_logger()


def filter_tds_observations(df, return_removals=False, **kwargs):
    """Filter out salinity observations which are not suitable for analysis.

    Args:
        df (pandas DataFrame): observations
        return_removals (bool): return the removals which end up being applied.

    Returns:
        :class:`pandas.DataFrame` or tuple of two dataframes if
        *return_removals* is True.

    Other keyword arguments are passed to
    :func:`wrap_technote.load_qc_removals`.

    Removes rows where:

    1. anomalous_ind == "Y" AND
    2. measured_during == "D"


    """
    df = df[~df.collected_date.isnull()]
    df = df[~df.tds.isnull()]

    removals = [
        {
            "reason": "SA Geodata records with anomalous_ind != 'N'",
            "idx": df.anomalous_ind != "N",
        },
        {
            "reason": "SA Geodata records with measured_during in 'D', 'R', 'U'",
            "idx": df.measured_during.isin(["D"]),
        },
    ]
    removals += load_qc_removals(df, parameter="TDS", dt_col="collected_date", **kwargs)

    rdfs = []
    comb_idx = np.array([False for x in range(len(df))])
    for removal in removals:
        idx = removal["idx"].values
        rdf = pd.DataFrame(df[idx])
        rdf["reason"] = removal["reason"]
        rdfs.append(rdf)
        comb_idx = np.logical_or(comb_idx, idx)

    df = df[~comb_idx]

    if return_removals:
        return df, pd.concat(rdfs)
    else:
        return df


def reduce_to_annual_tds(df, reduction_func="mean"):
    """Reduce salinity data to an annual value.

    Args:
        df (pd.DataFrame): salinity data with columns
            "well_id", "collected_date" (datetimes), "tds"
        reduction_func (str, lambda): aggregation function
            for pandas.GroupBy.agg e.g. "mean", "median"

    Return:
        pandas.DataFrame: dataframe with columns "collected_year",
        "well_id", "easting", "northing", "latitude", "longitude", "tds"

    You can get the necessary data for this by for example from
    a salinity resource key `resource`:

    .. code-block:: python

        >>> df = resource.read_data("validated_data", "valid_data")

    """
    if len(df) == 0:
        return pd.DataFrame(
            columns=[
                "collected_year",
                "well_id",
                "easting",
                "northing",
                "latitude",
                "longitude",
                "tds",
            ]
        )
    else:
        tdsann = (
            df.groupby(
                [
                    "well_id",
                    "easting",
                    "northing",
                    "longitude",
                    "latitude",
                    df.collected_date.dt.year,
                ]
            )
            .tds.agg(reduction_func)
            .reset_index()
            .rename(columns={"collected_date": "collected_year"})
        )
        tdsann["decade"] = tdsann.collected_year.map(
            generate_yearly_periods(spacing=10)
        )
        tdsann["period_5yr"] = tdsann.collected_year.map(
            generate_yearly_periods(spacing=5)
        )

        return tdsann


def calculate_annual_tds_stats(df):
    """Return annual statistics by year.

    Args:
        df (pd.DataFrame): tds data - one row per well per year
            e.g. see :func:`reduce_to_annual_tds`

    Returns:
        :class:`pandas.DataFrame`: dataframe with year as index
        and columns "n_wells",
        "tds_mean", "tds_median", and "tds_stdev"

    """
    if len(df):
        grouped = df.groupby("collected_year")
        annstats = pd.concat(
            [
                grouped.well_id.count(),
                grouped.tds.mean(),
                grouped.tds.median(),
                grouped.tds.std(),
            ],
            axis=1,
        )
        annstats.columns = ["n_wells", "tds_mean", "tds_median", "tds_stdev"]
        return annstats
    else:
        return pd.DataFrame(columns=["n_wells", "tds_mean", "tds_median", "tds_stdev"])


def get_annual_mean_salinity_data(tdsann, well_id):
    """Return annual mean salinity data points.

    Args:
        tdsann (pd.DataFrame): columns "well_id", "collected_year" (int) and "tds" (float)
        well_id (str): value to group by

    Returns:
        pd.DataFrame: a dataframe with columns "well_id", "collected_date", and "tds",
        with the date set to June 30th of each year's value, containing only
        that well's data.

    Note that *tdsann* can be generated from an ordinary table `tds` of salinity data
    using code such as:

    .. code-block:: python

        >>> tdsann = (
        ...         tds.groupby([tds.well_id, tds.collected_date.dt.year])
        ...         .tds.mean()
        ...         .reset_index()
        ...         .rename(columns={"collected_date": "collected_year"})
        ...     )

    """
    idx = lambda x: x.well_id == well_id
    df = tdsann[idx].sort_values("collected_year")
    df["collected_date"] = [pd.Timestamp(y, 6, 30) for y in df.collected_year]
    return df


def linear_salinity_trend(
    df, tds_col="tds", dt_col="collected_date", regression_method="least-squares"
):
    """Calculate a linear salinity trend.

    Args:
        df (pandas.DataFrame): data to regress against.
        tds_col (str): column in `df` that contains salinity data in mg/L
        dt_col (str): column in `df` that contains pd.Timestamp datetimes.
        regression_method (str): regression_method (str): either "least-squares"
            or "L2" for ordinary least squares or "least-absolute-deviation" or
            "L1" for deviation

    Returns:
        :class:`pandas.DataFrame`: pandas dataframe with columns:

        - "observed" (coming from ``df[tds_col]``)
        - "ndays" (calculated from ``df[dt_col]``)
        - "timestamp" (coming from ``df[dt_col]``)
        - "predicted" (trend line value)
        - "start_value" (first observed value from period)
        - "end_value" (last observed value from period)
        - "slope_yr_ndays" (slope of the trend line in units of mg/L/day)
        - "y_int_ndays" (trend line intercept at day=0, almost totally meaningless)
        - "slope_yr" (trend line slope in units of mg/L/y).

    This function uses :func:`wrap_technote.linear_trend` to do the regression.

    """
    ndays = df[dt_col].apply(lambda dt: tn.date_to_decimal(dt)).values
    dfx = pd.DataFrame(
        {"observed": df[tds_col], "ndays": ndays, "timestamp": df[dt_col]}, index=None
    )
    tline = linear_trend(
        dfx, param_col="observed", dt_col="ndays", regression_method=regression_method
    ).to_dict()
    predicted = ndays * tline["slope_yr_ndays"] + tline["y_int_ndays"]
    dfx["start_value"] = df[tds_col].iloc[0]
    dfx["end_value"] = df[tds_col].iloc[-1]
    dfx["predicted"] = predicted
    for k, v in tline.items():
        dfx[k] = v
    return dfx


def calculate_historical_salinity_trends(
    df, trend_length_years=10, years="all", regression_method="least-squares"
):
    """Calculate salinity trends for each year possible.

    Args:
        df (pd.DataFrame): should have columns *collected_date* (datetime), *tds* (float)
        trend_length_years (int): number of years the trend should be calculated over.
        years (str or iterable): either "all", "final", or an iterable of integers.
            Trends will calculated as of each year, so for example if *df* has data
            from 1990 to 2020, if *years* is `"all"`, a trend line and status will
            be calculated as at 1991, 1992, and so on until 2021.

    Returns:
        tuple: with three items:

        - years (ndarray): the years for which trends have been calculated
        - dfs (list, each item a dict of DataFrames): one under the key "df" shows the
          original data with columns "well_id", "collected_year", "tds", "collected_date",
          "mean". Another under "trend_df" shows the trend line data against observed
          data. It has columns "observed", "ndays", "timestamp", "start_value",
          "end_value", "predicted", "slope_yr_ndays", "y_int_ndays", and "slope_yr".
          One set of dataframes is returned for each year in `years`, i.e. the length
          of `dfs` is the length of `years`.
        - results (pd.DataFrame): shows a summary for each trend period calculated.
          Columns are: "well_id", "year", "start_year", "current_tds", "current_pct_diff",
          "mean", "n_years_data", "slope_mgl_yr", "slope_pct_change_yr",

    If, for a given trend period (i.e. `year - (trend_length_years - 1)`), the number
    of datapoints is 2 or greater, then the trend period at that year will be included
    in the results (below). If not, it will be silently excluded. As a result, note that
    the returned `years` ndarray may not be contiguous, i.e. it may have missing years.

    """

    if years == "all":
        year0 = df.collected_date.dt.year.min() + 1
        year1 = df.collected_date.dt.year.max()
        years = [y for y in range(year0, year1 + 1, 1)]
    elif years == "final":
        years = [df.collected_date.dt.year.max()]
    logger.debug(f"YEARS: {years}")
    dfs = []
    table_results = []
    years_ran = []
    well_id = df.well_id.unique()[0]
    for year in years:
        logger.debug(f"calculating trend for {year}")
        if len(df[df.collected_date.dt.year == year]) == 0:
            logger.debug(f"  skipping, no data in {year}")
            continue
        dfy = df[df.collected_date.dt.year <= year].sort_values("collected_date")
        dfy = dfy.dropna(subset=["tds"])
        start_year = year - (trend_length_years - 1)
        tdfy = dfy[dfy.collected_date.dt.year >= start_year]
        logger.debug(
            f"well_id={well_id} trend @ year={year} - start_year={start_year} - len(tdfy)={len(tdfy)}"
        )
        if len(tdfy) == 0:
            logger.debug(
                f"  skipping, only one data point between {start_year} and {year}"
            )
            continue
        tdf = linear_salinity_trend(tdfy, regression_method=regression_method)

        # QUESTION!!!!!!!!! is the "mean" the 10 year mean, or the whole lot of data?
        # Probably needs to be much more than 10 years.

        mean = dfy.tds.mean()
        current_tds = dfy.tds.iloc[-1]
        slope_mgl_yr = tdf.slope_yr.iloc[0]
        dfy["mean"] = mean
        pct_diff = ((current_tds - mean) / mean) * 100
        diff_word = "above" if pct_diff > 0 else "below"
        label_text = f"(<= {year}): {abs(pct_diff):.0f}% {diff_word} average"
        slope_pct_change_yr = (slope_mgl_yr / tdf.iloc[-1].predicted) * 100
        dfs_result = {
            "df": dfy,
            "trend_df": tdf,
        }
        table_result = {
            "well_id": well_id,
            "year": year,
            "start_year": start_year,
            "n_years_data": len(tdfy),
            "current_tds": current_tds,
            "mean": mean,
            "current_pct_diff": pct_diff,
            "slope_mgl_yr": slope_mgl_yr,
            "slope_pct_change_yr": slope_pct_change_yr,
            "slope_pct_change": slope_pct_change_yr * trend_length_years,
            "label": label_text,
            "trend_length_years": trend_length_years,
        }
        logger.debug(f"Results: {table_result}")
        years_ran.append(year)
        dfs.append(dfs_result)
        table_results.append(table_result)
    return np.array(years_ran), dfs, pd.DataFrame(table_results)


def generate_salinity_bins(
    range_min,
    range_max,
    step,
    extrema=1e10,
    label_fmt="{bin_left}% to {bin_right}% {word}",
    end_label_fmt="More than {bin_left}% {word}",
    word_positive="increase",
    word_negative="decrease",
):
    """Generate bins/classes for salinity indicator values.

    .. todo:: Document this function

    Args:
        range_min (float)
        range_max (float)
        step (int)
        extrema (float)
        label_fmt (str)
        end_label (str)
        word_positive (str)
        word_negative (str)

    Returns:
        dict:

    """
    # bins = np.arange(range_min, range_max + step, step)
    bins = np.linspace(
        range_min, range_max, int(np.ceil((range_max - range_min) / step) + 1)
    )
    bins = np.concatenate([np.array([-1 * extrema]), bins, np.array([extrema])])
    bin_centres = []
    bin_labels = []
    bin_classes = []
    for i, value in enumerate(bins[:-1]):
        if value < 0:
            multiplier = -1
            word = word_negative
        else:
            multiplier = 1
            word = word_positive
        value_upper = bins[i + 1]
        bounds = sorted([abs(value), abs(value_upper)])
        label = label_fmt.format(
            word=word,
            bin_left="{:.0f}".format(bounds[0]),
            bin_right="{:.0f}".format(bounds[1]),
        )
        if i in (0, len(bins) - 2):
            label = end_label_fmt.format(
                word=word, bin_left="{:.0f}".format(min(np.abs(bounds)))
            )
        bin_class = f"{bounds[0] * multiplier:+.1f}_to_{bounds[1]  * multiplier:+.1f}"
        bin_classes.append(bin_class)
        bin_labels.append(label)
        bin_centres.append(np.mean(np.asarray(bounds) * multiplier))

    label_func = lambda x: pd.cut([x], bins, labels=bin_labels)[0]
    class_func = lambda x: pd.cut([x], bins, labels=bin_classes)[0]

    return {
        "bins": bins,
        "bins_left": bins[:-1],
        "bins_right": bins[1:],
        "bin_centres": bin_centres,
        "labels": bin_labels,
        "classes": bin_classes,
        "min": range_min,
        "max": range_max,
        "extrema": extrema,
        "step": step,
        "label_func": label_func,
        "class_func": class_func,
    }


def calculate_salinity_indicator_results(
    tdsann,
    dfn,
    pct_diff=None,
    trend_pct=None,
    years="final",
    regression_method="least-absolute-deviation",
    dropna=True,
    **kwargs,
):
    """Calculate 'pct_diff'/'curr_tds_pct_diff_indicator' and 'trend_pct'/'tds_trend_pct_change_indicator' values
    from annual salinity data.

    Args:
        tdsann (pandas.DataFrame): table of annual salinity data. It should have columns "tds" (floats),
            "collected_year" (int) and "well_id" (string or number) and will be passed as the first
            argument to :func:`wrap_technote.get_annual_mean_salinity_data`
        dfn (pandas.Series): recordO

    Returns: dict with keys "df" (pd.DataFrame), "data" (dict), "pct_diff" (dict) and
        "trend_pct" (dict)

    """
    data = {}
    for well_id in tdsann.well_id.unique():
        logger.debug(f"Calculating salinity indicators for {well_id}")
        df = get_annual_mean_salinity_data(tdsann, well_id)
        years, dfs, results = calculate_historical_salinity_trends(
            df, years="final", regression_method="least-absolute-deviation", **kwargs
        )
        if len(results):
            data[well_id] = {
                "years": years,
                "dfs": dfs,
                "results": results,
            }

    if pct_diff is None:
        pct_diff = generate_salinity_bins(
            range_min=float(dfn.pct_diff_range_min),
            range_max=float(dfn.pct_diff_range_max),
            step=float(dfn.pct_diff_step),
            word_positive="above",
            word_negative="below",
            label_fmt="{bin_left}% to {bin_right}% {word} mean",
            end_label_fmt="More than {bin_left}% {word} mean",
        )
    if trend_pct is None:
        trend_pct = generate_salinity_bins(
            range_min=float(dfn.trend_pct_range_min),
            range_max=float(dfn.trend_pct_range_max),
            step=float(dfn.trend_pct_step),
        )

    all_results = []

    for well_id, welldata in data.items():
        r = welldata["results"].iloc[-1]
        well_result = {
            "well_id": well_id,
            "mean_tds": welldata["dfs"][-1]["df"].iloc[-1]["mean"],
            "curr_tds": welldata["dfs"][-1]["df"].iloc[-1].tds,
            "curr_tds_pct_diff": r.current_pct_diff,
            "curr_tds_pct_diff_indicator": pct_diff["label_func"](r.current_pct_diff),
            "slope_pct_change_yr": r.slope_pct_change_yr,
            "slope_pct_change_trend_pd": r.slope_pct_change_yr * dfn.trend_length_years,
            "tds_trend_pct_change_indicator": trend_pct["label_func"](
                r.slope_pct_change_yr * dfn.trend_length_years
            ),
        }
        all_results.append(well_result)

    alldf = pd.DataFrame(all_results)
    if len(alldf) == 0:
        alldf = pd.DataFrame(
            columns=[
                "well_id",
                "mean_tds",
                "curr_tds",
                "curr_tds_pct_diff",
                "curr_tds_pct_diff_indicator",
                "slope_pct_change_yr",
                "slope_pct_change_trend_pd",
                "tds_trend_pct_change_indicator",
                "include_curr_pct_diff",
                "include_trend_pct",
                "validation_comment",
                "last_run_by",
                "last_run_date",
            ]
        )
    if dropna:
        alldf = alldf.dropna(
            subset=["curr_tds_pct_diff_indicator", "tds_trend_pct_change_indicator"],
            how="all",
        )
    alldf["include_curr_pct_diff"] = True
    alldf["include_trend_pct"] = True

    (
        curr_pct_diffs,
        tds_trend_pct_changes,
    ) = calculate_salinity_indicator_summary_results(alldf, pct_diff, trend_pct)

    return {
        "df": alldf,
        "data": data,
        "pct_diff": pct_diff,
        "trend_pct": trend_pct,
        "curr_pct_diffs": curr_pct_diffs,
        "tds_trend_pct_changes": tds_trend_pct_changes,
    }


def calculate_salinity_indicator_summary_results(alldf, pct_diff, trend_pct):
    """Calculate summary tables for *curr_pct_diffs* and *tds_trend_pct_changes*.

    Args:
        alldf (pd.DataFrame):
        pct_diff (bins)
        trend_pct (bins):

    Returns: tuple *curr_pct_diffs* and *tds_trend_pct_changes* (summary tables).

    """
    incl_idx = alldf.include_curr_pct_diff == True
    curr_pct_diffs = alldf[incl_idx].curr_tds_pct_diff_indicator.value_counts()
    curr_pct_diffs = curr_pct_diffs.reindex(pct_diff["labels"])
    curr_pct_diffs = curr_pct_diffs[::-1]
    curr_pct_diffs.index.name = "curr_tds_pct_diff_indicator"
    curr_pct_diffs.name = "n_wells"
    curr_pct_diffs = curr_pct_diffs.reset_index()

    pct_wells = curr_pct_diffs.n_wells / curr_pct_diffs.n_wells.sum() * 100
    pct_wells[np.isnan(pct_wells)] = 0

    logger.debug(f"pct_wells = {pct_wells}")
    curr_pct_diffs["pct_wells"] = round_to_100_percent(pct_wells)

    incl_idx2 = alldf.include_trend_pct == True
    tds_trend_pct_changes = alldf[
        incl_idx2
    ].tds_trend_pct_change_indicator.value_counts()
    tds_trend_pct_changes = tds_trend_pct_changes.reindex(trend_pct["labels"])
    tds_trend_pct_changes = tds_trend_pct_changes[::-1]
    tds_trend_pct_changes.index.name = "tds_trend_pct_change_indicator"
    tds_trend_pct_changes.name = "n_wells"
    tds_trend_pct_changes = tds_trend_pct_changes.reset_index()

    pct_wells = (
        tds_trend_pct_changes.n_wells / tds_trend_pct_changes.n_wells.sum() * 100
    )
    tds_trend_pct_changes["pct_wells"] = round_to_100_percent(pct_wells)

    curr_pct_diffs = curr_pct_diffs.fillna(0)
    tds_trend_pct_changes = tds_trend_pct_changes.fillna(0)

    return curr_pct_diffs, tds_trend_pct_changes


def calculate_historical_pct_diff_values(tdsann, pct_diff):
    """Calculate historical salinity percent difference from mean values.

    Args:
        tdsann (pd.DataFrame): annual salinities - must have "well_id", "collected_year"
            and "tds" columns
        pct_diff (dict): definition of percentage salinity difference bins

    Results: modifies *tdsann* in-place with new columns

    """
    for well_id in tdsann.well_id.unique():
        idx = tdsann.well_id == well_id
        mean_tds = tdsann[idx].tds.mean()
        tdsann.loc[idx, "pct_diff"] = ((tdsann[idx].tds - mean_tds) / mean_tds) * 100
        tdsann.loc[idx, "pct_diff_label"] = [
            "above" if v > 0 else "below" for v in tdsann[idx].pct_diff
        ]
        tdsann.loc[idx, "tds_indicator"] = [
            pct_diff["label_func"](v) for v in tdsann[idx].pct_diff
        ]

    return tdsann


def collate_salinity_summary_data(resource, db=None):
    """Collate salinity data outputs for a resource.

    Args:
        resource (Resource object)
        db (SAGeodataConnection object): optional, will
            be created if omitted.

    Returns:
        dict: details below

    The keys of the returned dictionary are:

    - current_tds_year
    - current_wells
    - current_wells_ex_trends
    - trend_wells
    - excluded_wells
    - curr_pct_diff_wells
    - tds_trend_pct_wells
    - resource
    - wells
    - wells_html
    - data_val
    - tds_changes
    - anntds_summ
    - anntds
    - tdstrends_mgl_summ_1
    - tdstrends_mgl_summ_2
    - tdstrends
    - tdstrends_5yr_summ_1
    - tdstrends_5yr_summ_2
    - curr_pct_diff
    - curr_pct_diff_summ
    - curr_pct_diff_summ_1
    - trend_pct
    - trend_pct_summ
    - trend_pct_summ_1
    - indicators_all

    """
    if db is None:
        db = gd.sageodata()

    current_tds_year = resource.trend_dfn.end_year

    s4 = resource.read_data("validated_data", sheet_name=None)
    s5 = resource.read_data("salinity_trends", sheet_name=None)
    s6 = resource.read_data("salinity_long_term_change", sheet_name=None)
    s7 = resource.read_data("salinity_indicators", sheet_name=None)

    well_ids = sorted(
        set(
            list(s4["valid data"].well_id.unique())
            + list(s4["invalid data"].well_id.unique())
        )
    )

    anntds = s4["current_mean_tds"]
    tdstrends = s5["final_trends"]
    current_wells = list(s4["valid data"].well_id.unique())
    trend_wells = list(s5["final trends"].well_id.unique())
    current_wells_ex_trends = set(current_wells) - set(trend_wells)
    excluded_wells = set(well_ids) - set(current_wells + trend_wells)
    curr_pct_diff_wells = list(s7["curr_pct_diff"].well_id.unique())
    tds_trend_pct_wells = list(s7["trend_pct"].well_id.unique())

    wells_found = db.find_wells(str(well_ids))
    if len(wells_found) > 0:
        wells = db.drillhole_details(wells_found).sort_values("well_id")
        wells["charts_link"] = wells.apply(
            lambda x: f"<a href='#charts-{x.well_id}'>{x.well_id}</a>", axis="columns"
        )
    else:
        wells = pd.DataFrame(columns=["well_id"])

    templates = tn.load_html_templates()

    data_val = resource.filter_table_by_well_ids(
        wells.well_id.values, table="Data_validation"
    )
    data_val_cols = [
        "well_id",
        "database",
        "start_period",
        "end_period",
        "action",
        "comment",
        "username",
    ]
    if len(data_val) > 0:
        data_val = data_val[data_val_cols]
    else:
        data_val = pd.DataFrame(columns=data_val_cols)

    anntds_summ = anntds[["tds"]].describe().round(2).T
    anntds = anntds.sort_values("tds")[["well_id", "unit_hyphen", "dh_name", "tds"]]

    remap_cols = {"sal_change": "5yr_change_mgL", "sal_pct_change": "5yr_change_in_pct"}
    cols_a = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    null_row_a = {col: pd.NA for col in cols_a}
    cols_b = [
        ("5yr_change_mgL", "count"),
        ("5yr_change_mgL", "mean"),
        ("5yr_change_mgL", "std"),
        ("5yr_change_mgL", "min"),
        ("5yr_change_mgL", "25%"),
        ("5yr_change_mgL", "50%"),
        ("5yr_change_mgL", "75%"),
        ("5yr_change_mgL", "max"),
        ("5yr_change_in_pct", "count"),
        ("5yr_change_in_pct", "mean"),
        ("5yr_change_in_pct", "std"),
        ("5yr_change_in_pct", "min"),
        ("5yr_change_in_pct", "25%"),
        ("5yr_change_in_pct", "50%"),
        ("5yr_change_in_pct", "75%"),
        ("5yr_change_in_pct", "max"),
    ]
    if len(tdstrends):
        tdstrends_mgl_summ_1 = (
            tdstrends.groupby(["status_change"])[["slope_yr"]].describe().round(2)
        )
        tdstrends_mgl_summ_2 = tdstrends[["slope_yr"]].describe().round(2).T
        tdstrends_5yr_summ_1 = (
            tdstrends.rename(columns=remap_cols)
            .groupby(["status_change"])[["5yr_change_mgL", "5yr_change_in_pct"]]
            .describe()
            .round(2)
        )
        tdstrends_5yr_summ_2 = (
            tdstrends[["sal_change", "sal_pct_change"]]
            .rename(columns=remap_cols)
            .describe()
            .round(2)
            .T
        )
        tdstrends = tdstrends.sort_values(["status_change", "sal_pct_change"])
        tdstrends = tdstrends[
            [
                "well_id",
                "status_change",
                "slope_yr",
                "sal_change",
                "sal_pct_change",
                "n_trend_year_obs",
            ]
        ].rename(columns=remap_cols)
    else:
        tdstrends_mgl_summ_1 = pd.DataFrame(columns=cols_a)
        tdstrends_mgl_summ_2 = pd.DataFrame(columns=cols_a)
        tdstrends_5yr_summ_1 = pd.DataFrame(columns=cols_b)
        tdstrends_5yr_summ_2 = pd.DataFrame(columns=cols_a)
    tdschange = s6["TDS changes"]

    curr_pct_diff_summ = s7["curr_pct_diff_summary"]
    trend_pct_summ = s7["tds_trend_pct_changes_summary"]
    curr_pct_diff = s7["curr_pct_diff"]
    if len(curr_pct_diff):
        curr_pct_diff_summ_1 = (
            curr_pct_diff["curr_tds_pct_diff"].describe().to_frame().T
        )
    else:
        curr_pct_diff_summ_1 = pd.DataFrame([null_row_a], index=["curr_tds_pct_diff"])

    trend_pct = s7["trend_pct"]
    if len(trend_pct):
        trend_pct_summ_1 = (
            trend_pct[["slope_pct_change_yr", "slope_pct_change_trend_pd"]].describe().T
        )
    else:
        trend_pct_summ_1 = pd.DataFrame(
            [null_row_a, null_row_a],
            index=["slope_pct_change_yr", "slope_pct_change_trend_pd"],
        )
    indicators_all = s7["all_results"]
    indicators_all[
        "validation_comment"
    ] = indicators_all.validation_comment.str.replace("\n", "<br />")

    return {
        "current_tds_year": current_tds_year,
        "current_wells": sorted(current_wells),
        "current_wells_ex_trends": sorted(current_wells_ex_trends),
        "trend_wells": sorted(trend_wells),
        "excluded_wells": sorted(excluded_wells),
        "curr_pct_diff_wells": sorted(curr_pct_diff_wells),
        "tds_trend_pct_wells": sorted(tds_trend_pct_wells),
        "resource": resource,
        "wells": wells.to_dict(orient="records"),
        "wells_html": wells.to_html(escape=False),
        "data_val": data_val,
        "tds_changes": s6["TDS changes"].to_html(escape=False),
        "anntds_summ": anntds_summ,
        "anntds": anntds,
        "tdstrends_mgl_summ_1": tdstrends_mgl_summ_1,
        "tdstrends_mgl_summ_2": tdstrends_mgl_summ_2,
        "tdstrends": tdstrends,
        "tdstrends_5yr_summ_1": tdstrends_5yr_summ_1,
        "tdstrends_5yr_summ_2": tdstrends_5yr_summ_2,
        "curr_pct_diff_summ": curr_pct_diff_summ,
        "curr_pct_diff": curr_pct_diff,
        "curr_pct_diff_summ_1": curr_pct_diff_summ_1,
        "trend_pct_summ": trend_pct_summ,
        "trend_pct": trend_pct,
        "trend_pct_summ_1": trend_pct_summ_1,
        "indicators_all": indicators_all,
    }


def construct_salinity_template_sentences(
    resource, data, highlight_method="papayawhip"
):
    """Construct template sentences for water level sections.

    Args:
        resource (wrap_technote.Resource): resource to summaries
        data (dict): collated salinity results - see
            :func:`wrap_technote.collate_salinity_summary_data`
        highlight_method (str): "papayawhip" by default -
            see :func:`wrap_technote.utils.highlight_fields` for
            details

    Returns:
        list: list of sentences

    """
    tds = data["anntds_summ"].iloc[0]
    cat1 = data["trend_pct_summ"].fillna(0)
    cat = cat1.groupby(cat1.tds_trend_pct_change_indicator.str.contains("increase"))[
        ["n_wells", "pct_wells"]
    ].sum()
    cat.index.name = "category"
    cat = cat.reset_index()
    cat.loc[cat.category == False, "category"] = "decreasing"
    cat.loc[cat.category == True, "category"] = "increasing"
    maj = cat.sort_values("n_wells", ascending=False).iloc[0]

    a_vs_an = lambda w: "an" if w[0].lower() in "aeiouh" else "a"
    tr_dirn = lambda v: "an increase" if v > 0 else "a decrease"

    trend_length_years_word = decimal_words[
        resource.dfn_salinity_indicators.trend_length_years
    ]
    trend_length_years_word_upper = (
        trend_length_years_word[0].upper() + trend_length_years_word[1:]
    )

    sentence_1 = (
        f"In <|{data['current_tds_year']}|>, sampling results from "
        f"<|{tds['count']:.0f}|> wells in the "
        f"<|{resource.report_resources_mapping.tech_note_sentence_value}|> "
        f"ranged between "
        f"<|{tds['min']:.0f}|> mg/L and <|{tds['max']:.0f}|> mg/L "
        f"with a median of <|{tds['50%']:.0f}|> mg/L (Figure XYZ)."
    )

    sentence_2 = (
        f"In the <|{trend_length_years_word}|> years to "
        f"<|{resource.dfn_salinity_indicators.trend_end_year}|>, "
        f"<|{maj['n_wells']:.0f}|> of <|{cat.n_wells.sum():.0f}|> wells "
        f"(<|{maj['pct_wells']:.0f}|>%) show <|{a_vs_an(maj.category)}|> "
        f"<|{maj.category}|> trend in salinity (Section XYZ; Figure XYZ)."
    )

    cat2 = data["trend_pct_summ_1"].loc["slope_pct_change_yr"].fillna(0)

    sentence_3 = (
        f"<|{trend_length_years_word_upper}|>-year trends show that "
        f"rates of change in salinity vary from a "
        f"<|{tr_dirn(cat2['min'])}|> of <|{abs(cat2['min']):.1f}|>% per year to "
        f"<|{tr_dirn(cat2['max'])}|> of <|{abs(cat2['max']):.1f}|>% per year, with a median rate of "
        f"<|{abs(cat2['50%']):.1f}|>% <|{tr_dirn(cat2['50%']).split()[1]}|> per year."
    )

    sentences = [sentence_1, sentence_2, sentence_3]
    sentences = tn.highlight_fields(sentences, highlight_method=highlight_method)
    return sentences
