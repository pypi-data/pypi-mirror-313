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
from .charts_utils import *
from .charts_wl import *

logger = get_logger()


def filter_wl_observations(df, return_removals=False, **kwargs):
    """Filter out water level observations which are not suitable for monitoring
    trend analysis.

    Args:
        df (pandas.DataFrame): water level observations
        return_removals (bool): if True, also return the records which were
            removed (and why)

    Returns:
        either a :class:`pandas.DataFrame` with the filtered water levels,
        or a tuple of two dataframes, where the second is the records which were
        removed.

    See :func:`load_qc_removals` for more keyword arguments.

    Which records does it drop?

    1. Drops rows where "Swl" is null
    2. Drops rows where "anomalous_ind" is not "N"
    3. Drops rows where "pumping_ind" is not "N"
    4. Drops rows where "measured_during" is either "D", "R", or "U"
    5. Drops rows where "dry_ind" is not "N"
    6. Drops rows where "comments" contains "[Missed peak recovery]"


    """
    if not "database" in df:
        df["database"] = "SA Geodata"

    df = df[~df.obs_date.isnull()]

    removals = [
        {
            "reason": "SA Geodata records with null SWL measurements",
            "idx": (df.database == "SA Geodata") & pd.isnull(df.swl),
        },
        {
            "reason": "SA Geodata records with '[Missed peak recovery]' in the comments field",
            "idx": df.comments.str.contains(
                "[Missed peak recovery]", regex=False, na=False
            ),
        },
        {
            "reason": "SA Geodata records with anomalous_ind != 'N'",
            "idx": (df.database == "SA Geodata") & (df.anomalous_ind != "N"),
        },
        {
            "reason": "SA Geodata records with pumping_ind != 'N'",
            "idx": (df.database == "SA Geodata") & (df.pumping_ind != "N"),
        },
        {
            "reason": "SA Geodata records with measured_during in 'D', 'R', 'U'",
            "idx": (df.database == "SA Geodata")
            & (df.measured_during.isin(["D", "R", "U"])),
        },
        {
            "reason": "SA Geodata records with dry_ind != 'N'",
            "idx": (df.database == "SA Geodata") & (df.dry_ind != "N"),
        },
        {
            "reason": "AQTS grade <= 0",
            "idx": (df.database == "Aquarius") & (df.grade <= 0),
        },
    ]

    removals += load_qc_removals(df, parameter="WL", **kwargs)

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


def analyse_wl_by_seasons(df, seasons, well_id_col="dh_no", dt_col="obs_date"):
    """Reduce a water level dataset to one or more values per seasonal period,
    according to the definition of seasons in *seasons*.

    Args:
        df (:class:`pandas.DataFrame`): data table of water level observations
        well_id_col (``str``, optional): column of *df* which uniquely identifies
            an individual well - not needed if *df* only has data from one well.
        dt_col (``str``, optional): column of *df* with datetimes

    Returns:
        :class:`pandas.DataFrame`: dataframe with the same columns as *df* and the additional
        columns "season" and "year+season". The returned DataFrame can be used as
        the *anndf* argument to, for example, :func:`wrap_technote.plot_wl_seasonality`.

    Normally this would reduce df such that it has no more than one value per season.
    This is the case where the seasonal definition uses a reduction function such
    as 'max' or 'min'. However, when the reduction function is 'all', it
    will potentially retain more than one value per season. This is to accommodate
    regions such as Far North.

    """
    df2 = df.copy()
    df2.loc[:, "season"] = df2[dt_col].dt.dayofyear.map(seasons.dayofyear_to_season)
    df2.loc[:, "season_year"] = df2[dt_col].apply(seasons.label_year)
    df2.loc[:, "year+season"] = df2[dt_col].apply(seasons.label_year_and_season)
    df2.loc[:, "seasons_dfn"] = seasons.to_str()
    logger.debug(
        f"well_id: {df2[well_id_col].unique()[0]} seasons_dfn: id={id(seasons)} {seasons.to_str()}"
    )
    if well_id_col in df2.columns:
        groupby_cols = [well_id_col, "year+season", "season"]
    else:
        groupby_cols = ["year+season", "season"]
    if seasons.reduces_to_one_value_per_season:
        return (
            df2.groupby(groupby_cols)
            .apply(seasons.apply_season_func)
            .reset_index(drop=True)
        )
    else:
        return df2


def apply_calculate_seasonal_water_levels(resource):
    """Returns a function suitable for "apply"ing to a DataFrame.

    Args:
        resource (tn.Resource)

    Returns:
        function: a function that accepts a dataframe of water levels
        for a single well.

    The function can then be applied to a dataframe to produce a
    new dataframe containing seasonal water levels (using the function
    :func:`wrap_technote.analyse_wl_by_seasons`).

    """

    def apply_calculate_seasonal_water_levels__generated(frame):
        well_id = frame.well_id.unique()[0]
        season = resource.get_season(well_id)
        return analyse_wl_by_seasons(frame, season)

    return apply_calculate_seasonal_water_levels__generated


def get_total_wl_changes(wldata, windows):
    """
    df = resource.read_data("recovery_wl_data", "annual recovered WL")

    .. todo:: Document this function.

    """

    window_year_col = "season_year"

    dfs = []
    for window in windows:
        name = window[0]
        start_syears = list(window[1])
        start_syears += [f"{y}-{str(y + 1)[-2:]}" for y in start_syears]
        start_syears += [str(w) for w in window[1]]
        end_syears = list(window[2])
        end_syears += [f"{y}-{str(y + 1)[-2:]}" for y in end_syears]
        end_syears += [str(w) for w in window[2]]
        agg_arg = window[3]

        def get_start_end_year_rswls(f):
            start_rswl = f[f[window_year_col].isin(start_syears)].rswl.agg(agg_arg)
            end_rswl = f[f[window_year_col].isin(end_syears)].rswl.agg(agg_arg)
            return pd.Series({"start_window": start_rswl, "end_window": end_rswl})

        x = wldata.groupby("well_id").apply(get_start_end_year_rswls)
        x["change"] = x["end_window"] - x["start_window"]
        x.loc[x.change > 0, "change_direction"] = "increase"
        x.loc[x.change == 0, "change_direction"] = "no change"
        x.loc[x.change < 0, "change_direction"] = "decrease"
        x_cols = list(x.columns)
        x["window"] = name
        x["start_dfn"] = str(start_syears)
        x["end_dfn"] = str(end_syears)
        x = x[["window"] + x_cols + ["start_dfn", "end_dfn"]]
        dfs.append(x)

    return pd.concat(dfs).dropna(subset=["change"], how="any")


def get_total_wl_change_windows(current_year, offset_years=(30, 20, 10)):
    """

    .. todo:: Document this function.

    """
    windows = []
    for offset in offset_years:
        label = f"{offset} years"
        start_years = tuple(
            [
                current_year - offset,
                current_year - offset + 1,
                current_year - offset + 2,
            ]
        )
        end_year = tuple([current_year])
        func = "mean"
        windows.append((label, start_years, end_year, func))
    return windows


def collate_waterlevel_summary_data(resource, db=None):
    """Collate water level data outputs for a resource.

    Args:
        resource (Resource object)
        db (SAGeodataConnection object): optional, will
            be created if omitted.

    Returns:
        dict: details below

    The keys of the returned dictionary are:

    - unlisted_wells
    - curr_rank_wells
    - curr_rank_excluded_wells
    - final_trend_wells
    - excluded_trend_wells
    - resource: wrap_technote.Resource object
    - wells: list of dicts
    - wells_html: HTML representation
    - data_val
    - curr_ranks
    - curr_ranks_summ
    - curr_ranks_summ_grpd
    - majority_grpd_curr_ranks
    - curr_ranks_qc
    - final_trends
    - wltrends_summ_by_triclass
    - wltrends_summ_all
    - total_wl_changes
    - total_wl_changes_summ_1
    - total_wl_changes_summ_2

    """
    if db is None:
        db = gd.sageodata()

    s1 = resource.read_data("validated_data", sheet_name=None)
    s2 = resource.read_data("recovery_wl_data", sheet_name=None)

    ranks = s2["annual_recovered WL"]
    curr_ranks = s2["current ranked WLs"]
    curr_ranks_excluded = s2["current ranks excl"]
    curr_ranks_qc = s2["data quality"]

    s3 = resource.read_data("recovery_wl_trends", sheet_name=None)
    final_trends = s3["final trends"]
    excluded_trends = s3["excluded trends"]

    total_wl_changes = s2["total_wl_changes"]
    curr_rank_wells = sorted(set(curr_ranks.well_id.unique()))
    curr_rank_excluded_wells = sorted(set(curr_ranks_excluded.well_id.unique()))
    final_trend_wells = sorted(set(final_trends.well_id.unique()))
    excluded_trend_wells = sorted(set(excluded_trends.well_id.unique()))

    all_listed_wells = set(
        sorted(
            set(
                list(curr_rank_wells)
                + list(final_trend_wells)
                + list(curr_rank_excluded_wells)
                + list(excluded_trend_wells)
            )
        )
    )
    all_wells = set(
        list(s1["valid data"].well_id.unique())
        + list(s1["invalid data"].well_id.unique())
    )
    unlisted_wells = all_wells - set(all_listed_wells)

    wells = db.drillhole_details(db.find_wells(str(all_wells))).sort_values("well_id")
    wells["charts_link"] = wells.apply(
        lambda x: f"<a href='#charts-{x.well_id}'>{x.well_id}</a>", axis="columns"
    )

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
    data_val = data_val[[c for c in data_val_cols if c in data_val.columns]]
    final_trends_cols = [
        c
        for c in [
            "well_id",
            "unit_hyphen",
            "aquifer",
            "slope_yr",
            "status_change",
            "status",
            "status_combined",
            "n_trend_obs",
        ]
        if c in final_trends.columns
    ]

    bcmap = BoMClassesColormap

    # Summary and details table for Current WL ranks
    curr_ranks["class_index"] = curr_ranks["rswl_bom_class"].map(
        {c: bcmap.class_names.index(c) for c in bcmap.class_names}
    )
    curr_ranks = curr_ranks
    curr_ranks_ct = curr_ranks["rswl_bom_class"].value_counts().fillna(0)
    curr_ranks_summ = curr_ranks_ct.to_frame(name="n_wells").fillna(0)
    curr_ranks_summ["pct_wells"] = (curr_ranks_ct / curr_ranks_ct.sum() * 100).round(2)
    curr_ranks_summ = curr_ranks_summ.reindex(bcmap.class_names).fillna(0)

    crs = curr_ranks_summ
    curr_ranks_summ_grpd = {
        "'Below average' or lower": crs.loc[
            ["Below average", "Very much below average", "Lowest on record"]
        ].sum(axis=0),
        "Average": crs.loc["Average"],
        "'Above average' or higher": crs.loc[
            ["Above average", "Very much above average", "Highest on record"]
        ].sum(axis=0),
    }
    curr_ranks_summ_grpd = pd.DataFrame(curr_ranks_summ_grpd).fillna(0).T

    crf_cols = [
        "rswl_bom_class",
        "well_id",
        "unit_hyphen",
        "aquifer",
        "class_index",
        "rswl",
        "obs_date",
    ]
    logger.debug(f"curr_ranks.columns = {curr_ranks.columns.values}")
    curr_ranks = curr_ranks[crf_cols]
    logger.debug(f"curr_ranks.columns = {curr_ranks.columns.values}")
    curr_ranks = curr_ranks.sort_values(["class_index"])

    wltrends_summ_by_triclass = (
        final_trends.groupby(["status_change"])
        .slope_yr.describe()
        .round(2)
        .rename(columns={"count": "n_wells"})
    )
    if wltrends_summ_by_triclass.n_wells.sum() > 0:
        wltrends_summ_by_triclass.insert(
            1,
            "pct_wells",
            (
                wltrends_summ_by_triclass.n_wells
                / wltrends_summ_by_triclass.n_wells.sum()
                * 100
            ).round(2),
        )
    wltrends_summ_all = final_trends[["slope_yr"]].describe().round(2).T
    final_trends = final_trends.sort_values(["slope_yr"])

    if len(total_wl_changes):
        total_wl_changes_summ_1 = (
            total_wl_changes.groupby(["window"]).change.describe().round(2)
        )
        total_wl_changes_summ_2 = (
            total_wl_changes.groupby(["window", "change_direction"])
            .change.describe()
            .round(2)
        )
    else:
        total_wl_changes_summ_1 = pd.DataFrame()
        total_wl_changes_summ_2 = pd.DataFrame()

    total_wl_changes = total_wl_changes.sort_values(
        ["window", "change_direction", "change"]
    ).set_index(["window", "change_direction"])

    retdata = {
        "unlisted_wells": sorted(unlisted_wells),
        "curr_rank_wells": sorted(curr_rank_wells),
        "curr_rank_excluded_wells": sorted(curr_rank_excluded_wells),
        "final_trend_wells": sorted(final_trend_wells),
        "excluded_trend_wells": sorted(excluded_trend_wells),
        "resource": resource,
        "wells": wells.to_dict(orient="records"),
        "wells_html": wells.to_html(escape=False),
        "data_val": data_val,
        "curr_ranks": curr_ranks[crf_cols],
        "curr_ranks_summ": curr_ranks_summ,
        "curr_ranks_summ_grpd": curr_ranks_summ_grpd,
        "majority_grpd_curr_ranks": curr_ranks_summ_grpd.sort_values("n_wells").iloc[
            -1
        ],
        "curr_ranks_qc": curr_ranks_qc,
        "final_trends": final_trends[final_trends_cols],
        "wltrends_summ_by_triclass": wltrends_summ_by_triclass,
        "wltrends_summ_all": wltrends_summ_all,
        "total_wl_changes": total_wl_changes,
        "total_wl_changes_summ_1": total_wl_changes_summ_1,
        "total_wl_changes_summ_2": total_wl_changes_summ_2,
    }

    return retdata


def construct_waterlevel_template_sentences(
    resource, data, highlight_method="papayawhip"
):
    """Construct template sentences for water level sections.

    Args:
        resource (wrap_technote.Resource): resource to summaries
        data (dict): collated water level results - see
            :func:`wrap_technote.collate_waterlevel_summary_data`
        highlight_method (str): "papayawhip" by default -
            see :func:`wrap_technote.utils.highlight_fields` for
            details

    Returns:
        list: list of sentences

    """
    maj = data["majority_grpd_curr_ranks"]
    total_wells = len(data["curr_ranks"])

    sentence_1 = (
        f"In <|{resource.trend_dfn.end_recovery_season:.0f}|>, "
        f"winter recovered water levels in "
        f"<|{maj.n_wells:.0f}|> out of <|{total_wells:.0f}|> (<|{maj.pct_wells:.0f}|>%) "
        "of monitoring wells in the "
        f"<|{resource.report_resources_mapping.tech_note_sentence_value}|> "
        f"are classified as <|{maj.name}|> (Section XYZ)."
    )

    tchanges = data["total_wl_changes_summ_1"]
    word = lambda x: "decline" if x < 0 else "rise"

    sentences_2 = []
    for year_range, row in tchanges.sort_index(ascending=False).iterrows():
        n_years = int(year_range.split()[0])
        if n_years in decimal_words.index.values:
            year_range_word = decimal_words[n_years]
        else:
            year_range_word = n_years
        sentences_2.append(
            (
                f"Over the past <|{year_range_word}|> years, "
                f"variations in water level in <|{row['count']:.0f}|> well<|{'s' if row['count'] > 1 else ''}|> "
                f"range from a <|{word(row['min'])}|> of <|{abs(row['min']):.2f}|> m "
                f"to a <|{word(row['max'])}|> of <|{abs(row['max']):.2f}|> m "
                f"(median is a <|{word(row['50%'])}|> of <|{abs(row['50%']):.1f}|> m)."
            )
        )

    trends = data["wltrends_summ_by_triclass"]
    majtr = get_majority_categories(trends)
    trend_years = resource.trend_dfn.end_year - resource.trend_dfn.start_year + 1
    words = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    num2word = {i + 2: words[i] for i in range(len(words))}
    years_word = num2word[trend_years]
    years_word = years_word[0].upper() + years_word[1:]

    if word(majtr["min"]) == word(majtr["max"]):
        sentence_3 = (
            f"<|{years_word}|>-year trends show <|{majtr.name}|> water levels "
            f"in the majority of wells (<|{majtr.pct_wells:.0f}|>%), "
            f"with rates of <|{word(majtr['min'])}|> ranging between "
            f"<|{abs(majtr['min']):.2f}|>-<|{abs(majtr['max']):.2f}|> m/y "
            f"(median is a <|{word(majtr['50%'])}|> of <|{abs(majtr['50%']):.2f}|> m/y)."
        )
    else:
        sentence_3 = (
            f"<|{years_word}|>-year trends show <|{majtr.name}|> water levels "
            f"in the majority of wells (<|{majtr.pct_wells:.0f}|>%), "
            f"with rates ranging from a "
            f"<|{word(majtr['min'])}|> of <|{abs(majtr['min']):.2f}|> m/y to a "
            f"<|{word(majtr['max'])}|> of <|{abs(majtr['max']):.2f}|> m/y "
            f"(median <|{word(majtr['50%'])}|> of <|{abs(majtr['50%']):.2f}|> m/y)."
        )

    sentences = [sentence_1] + sentences_2 + [sentence_3]

    sentences = highlight_fields(sentences, highlight_method=highlight_method)

    return sentences


class QueryAndValidateWaterLevels(Run):
    """First stage of water level analysis. This downloads water level
    data (both manual and logger), filters it, and creates data validation
    charts.

    Args:
        resource (:class:`wrap_technote.Resource`)
        show_comments (bool): whether to show SA Geodata comments on the
            for the manual water levels, on the data validation charts
        plot_figures (bool): create the data validation figures

    Attributes:
        data (dict): data artifacts created during the stage

    The steps of this stage are:

    1. :meth:`wrap_technote.QueryAndValidateWaterLevels.load_resource_definition`
    2. :meth:`wrap_technote.QueryAndValidateWaterLevels.fetch_wl_data`
    3. :meth:`wrap_technote.QueryAndValidateWaterLevels.drop_null_data`
    4. :meth:`wrap_technote.QueryAndValidateWaterLevels.filter_wl_data`
    5. :meth:`wrap_technote.QueryAndValidateWaterLevels.add_well_titles`
    6. :meth:`wrap_technote.QueryAndValidateWaterLevels.make_wl_validation_charts`
       (only run if plot_figures is True, obviously!)
    7. :meth:`wrap_technote.QueryAndValidateWaterLevels.save_results`

    """

    def __init__(
        self,
        resource,
        show_comments: bool = True,
        plot_figures: bool = True,
    ):
        super().__init__(
            resource=resource, show_comments=show_comments, plot_figures=plot_figures
        )

        for func in [
            self.load_resource_definition,
            self.fetch_wl_data,
            self.drop_null_data,
            self.filter_wl_data,
            self.add_well_titles,
            self.if_then_use("plot_figures", self.make_wl_validation_charts),
            self.save_results,
        ]:
            self.append_step(func)

    def load_resource_definition(self, resource, **kwargs):
        parameter = resource.resource_key.split("_")[-1]
        wells = resource.find_wells()
        return {"wells": wells}

    def fetch_wl_data(self, wells: pd.DataFrame, **kwargs):
        wls = gd.fetch_wl_data(wells, include_replacements=False)
        return {"wls": wls}

    def drop_null_data(self, wls: pd.DataFrame, **kwargs):
        wls = wls.dropna(subset=["dtw", "swl", "rswl"], how="all")
        return {"wls": wls}

    def filter_wl_data(self, wls: pd.DataFrame, resource, **kwargs):
        wls, removals = filter_wl_observations(wls, return_removals=True, qc=resource)
        wls = wls.groupby("well_id").filter(lambda x: len(x) >= 5)
        return {"wls": wls, "removals": removals}

    def add_well_titles(self, wls: pd.DataFrame, removals: pd.DataFrame, **kwargs):
        for df in (wls, removals):
            df["well_title"] = df.unit_hyphen + " " + df.obs_no + " " + df.dh_name
        return {"wls": wls, "removals": removals}

    def make_wl_validation_charts(
        self,
        wls: pd.DataFrame,
        removals: pd.DataFrame,
        resource,
        show_comments: bool,
        **kwargs,
    ):
        axes = plot_wl_data_validation(
            wls,
            removals,
            well_title_col="well_title",
            show_comments=show_comments,
            adjust_comments=False,
            path=resource.static_path,
            savefig_and_close=True,
            dpi=100,
        )

    def save_results(
        self, resource, wls: pd.DataFrame, removals: pd.DataFrame, **kwargs
    ):
        table_prefix = "validated_data"
        output_data = {"valid_data": wls, "invalid_data": removals}
        resource.write_data_sheets(table_prefix, output_data)
        output_data = {table_prefix + "__" + k: v for k, v in output_data.items()}
        return {"output_data": output_data}


class CalculateSeasonalWaterLevels(Run):
    """Second stage of water level analysis. This calculates an annual
    'recovered' water level for each well, for each year.

    Args:
        resource (:class:`wrap_technote.Resource`)
        plot_figures (bool): create the data validation figures

    Attributes:
        data (dict): data artifacts created during the stage

    The steps of this stage are:

    1. :meth:`wrap_technote.CalculateSeasonalWaterLevels.load_data`
    2. :meth:`wrap_technote.CalculateSeasonalWaterLevels.calculate_seasonal_water_levels`
    3. :meth:`wrap_technote.CalculateSeasonalWaterLevels.filter_to_recovered_wls_only`
    4. :meth:`wrap_technote.CalculateSeasonalWaterLevels.calculate_quality_of_record`
    5. :meth:`wrap_technote.CalculateSeasonalWaterLevels.apply_data_validations`
    6. :meth:`wrap_technote.CalculateSeasonalWaterLevels.rank_and_classify_recovered_wls`
    7. :meth:`wrap_technote.CalculateSeasonalWaterLevels.clean_up`
    8. :meth:`wrap_technote.CalculateSeasonalWaterLevels.calculate_total_waterlevel_changes`
    9. :meth:`wrap_technote.CalculateSeasonalWaterLevels.make_charts`
    10. :meth:`wrap_technote.CalculateSeasonalWaterLevels.save_data`

    """

    def __init__(
        self,
        resource,
        plot_figures: bool = True,
    ):
        super().__init__(resource=resource, plot_figures=plot_figures)

        for func in [
            self.load_data,
            self.calculate_seasonal_water_levels,
            self.filter_to_recovered_wls_only,
            self.calculate_quality_of_record,
            self.apply_data_validations,
            self.rank_and_classify_recovered_wls,
            self.clean_up,
            self.calculate_total_waterlevel_changes,
            self.if_then_use("plot_figures", self.make_charts),
            self.save_data,
        ]:
            self.append_step(func)

    def load_data(self, resource, **kwargs) -> dict:
        wls = resource.read_data("validated_data__valid_data")
        return {"wls": wls}

    def calculate_seasonal_water_levels(self, wls, resource, **kwargs) -> dict:
        func = apply_calculate_seasonal_water_levels(resource)
        wlann = wls.groupby("well_id").apply(func).reset_index(drop=True)
        return {"wlann": wlann}

    def filter_to_recovered_wls_only(self, wlann, resource, **kwargs):
        # Create a subset of rows with only the recovery water levels.
        wlrec = wlann.loc[wlann.season == "recovery", :]

        # Remove any recovered levels which are beyond end_recovery_season
        end_y = int(str(resource.trend_dfn.end_recovery_season)[:4])
        wlrec = wlrec[wlrec.season_year.astype(str).str[:4].astype(int) <= end_y]
        return {"wlrec": wlrec}

    def calculate_quality_of_record(self, wlrec, resource, **kwargs):
        qc, cmp_df = resource.get_wl_ranking_qc_results(wlrec)
        logger.debug(
            str(
                pd.merge(
                    qc, cmp_df["all_conditions"], left_index=True, right_index=True
                )
            )
        )
        return {"qc": qc, "cmp_df": cmp_df}

    def apply_data_validations(self, resource, cmp_df, qc, **kwargs):
        vals = resource.read_table("Data_validation")
        incl = vals.query("action == 'Include well in water level rankings'")
        for ix, row in incl.iterrows():
            for well_id in row.well_id.split(","):
                well_id = well_id.strip()
                if well_id in cmp_df.index:
                    x = cmp_df.loc[well_id, "all_conditions"]
                    cmp_df.loc[well_id, "all_conditions"] = True
                    cmp_df.loc[
                        well_id, "comment"
                    ] = f"Included True by {row.username}: {row.comment} (overriding {x})"
        data_quality = pd.merge(
            qc, cmp_df, left_index=True, right_index=True
        ).reset_index()
        return {
            "vals": vals,
            "incl": incl,
            "cmp_df": cmp_df,
            "data_quality": data_quality,
        }

    def rank_and_classify_recovered_wls(self, wlrec, resource, **kwargs):
        wlranks = pd.merge(
            wlrec,
            wlrec.groupby("well_id", sort=False).rswl.apply(
                lambda df: tn.rank_and_classify(df, "rswl")
            ),
            left_index=True,
            right_index=True,
        )
        end_year = int(resource.trend_dfn.end_year)
        next_year = end_year + 1
        next_year2 = str(int(next_year))[2:]
        end_year2 = f"{end_year}-{next_year2}"
        curr_year_recovery_seasons = [f"{end_year}-recovery", f"{end_year2}-recovery"]
        logger.info(f"Current year recovery seasons: {curr_year_recovery_seasons}")
        wlranks_curr = wlranks[wlranks["year+season"].isin(curr_year_recovery_seasons)]
        return {"wlranks": wlranks, "wlranks_curr": wlranks_curr, "end_year": end_year}

    def clean_up(self, wlrec, wlranks, data_quality, wlranks_curr, **kwargs):
        wlrec = wlrec.reset_index()
        wlranks = (
            pd.merge(wlranks, data_quality[["well_id", "all_conditions"]], on="well_id")
            .rename(columns={"all_conditions": "meets_qc_filter"})
            .reset_index()
        )
        wlranks_curr = (
            pd.merge(
                wlranks_curr, data_quality[["well_id", "all_conditions"]], on="well_id"
            )
            .rename(columns={"all_conditions": "meets_qc_filter"})
            .reset_index()
        )

        wlranks_included = wlranks[wlranks.meets_qc_filter == True]
        wlranks_excluded = wlranks[wlranks.meets_qc_filter == False]
        wlranks_curr_included = wlranks_curr[wlranks_curr.meets_qc_filter == True]
        wlranks_curr_excluded = wlranks_curr[wlranks_curr.meets_qc_filter == False]
        return {
            "wlrec": wlrec,
            "wlranks": wlranks,
            "wlranks_curr": wlranks_curr,
            "wlranks_included": wlranks_included,
            "wlranks_excluded": wlranks_excluded,
            "wlranks_curr_included": wlranks_curr_included,
            "wlranks_curr_excluded": wlranks_curr_excluded,
        }

    def calculate_total_waterlevel_changes(self, wlranks, end_year, **kwargs):
        windows = get_total_wl_change_windows(current_year=end_year)
        total_wl_changes = get_total_wl_changes(wlranks, windows=windows).reset_index()
        return {"total_wl_changes": total_wl_changes}

    def make_charts(
        self,
        resource,
        wlranks,
        wls,
        cmp_df,
        wlann,
        wlranks_curr,
        data_quality,
        **kwargs,
    ):
        for fn in resource.static_path.glob("plot_wl_bom_classes_*.png"):
            logger.debug(f"removing old figure: {fn}")
            os.remove(fn)
        for fn in resource.static_path.glob("plot_wl_seasonality_*.png"):
            logger.debug(f"removing old figure: {fn}")
            os.remove(fn)

        logger.info(
            "Chart the original (filtered) water levels against the ranked and classified recovered water levels..."
        )
        for well_id, wwlranks in wlranks.groupby(wlranks.well_id):
            logger.info(f"{well_id}...")
            r = tn.plot_wl_bom_classes(
                wwlranks, wls[wls.well_id == well_id], fig=plt.figure(figsize=(10, 4))
            )
            titledf = wls[wls.well_id == well_id].iloc[0]
            well_title = f"{titledf.unit_hyphen} {titledf.obs_no} {titledf.dh_name}"
            r["ax"].set_title(
                f"{well_title}\nmeets all_conditions {cmp_df.loc[well_id].all_conditions}"
            )
            r["ax"].figure.tight_layout()
            filename = str(resource.static_path / f"plot_wl_bom_classes_{well_id}.png")
            logger.debug(f"filename = {filename}")
            r["ax"].figure.savefig(filename, dpi=100)
            tn.trim_whitespace_from_image(filename, append=False)

        logger.info("Chart seasonality for each well...")
        for well_id, wwlann in wlann.groupby("well_id"):
            logger.info(f"Plotting seasonal chart for {well_id}")
            seasons = resource.get_season(well_id)
            r = tn.plot_wl_seasonality(
                wls[wls.well_id == well_id], wwlann, seasons=seasons, dots=True
            )
            titledf = wls[wls.well_id == well_id].iloc[0]
            well_title = f"{titledf.unit_hyphen} {titledf.obs_no} {titledf.dh_name}"
            r["fig"].suptitle(well_title)
            filename = str(resource.static_path / f"plot_wl_seasonality_{well_id}.png")
            r["fig"].savefig(filename, dpi=100)
            tn.trim_whitespace_from_image(filename, append=False)

        logger.info("Charting: plot_wl_rankings_internal")
        fig = tn.plot_wl_rankings_internal(wlranks_curr, title=resource.resource_key)
        filename = f"{resource.resource_key}_wl_rankings_internal.png"
        for path in [resource.data_path]:
            fn = str(path / filename)
            fig.savefig(fn, dpi=120)
            tn.trim_whitespace_from_image(fn, append=False)

        logger.info("Charting: plot_wl_historical_rankings")
        fig = tn.plot_wl_historical_rankings(
            wlranks, data_quality, title=resource.resource_key
        )
        filename = f"{resource.resource_key}_wl_historical_rankings.png"
        for path in [resource.data_path]:
            fn = str(path / filename)
            fig.savefig(fn, dpi=120)
            tn.trim_whitespace_from_image(fn, append=False)

    def save_data(
        self,
        resource,
        data_quality,
        wlrec,
        wlranks_curr,
        wlranks_included,
        wlranks_curr_included,
        wlranks_excluded,
        wlranks_curr_excluded,
        total_wl_changes,
        wlranks,
        wlann,
        **kwargs,
    ):
        data_quality = data_quality.reset_index()

        output_data = {
            "annual_season_wl": wlann,
            "all_ranked_wl": wlranks,
            "annual_recovered_wl": wlrec,
            "ranked_wls": wlranks_included,
            "current_ranked_wls": wlranks_curr_included,
            "ranks_excl": wlranks_excluded,
            "current_ranks_excl": wlranks_curr_excluded,
            "total_wl_changes": total_wl_changes,
            "data_quality": data_quality,
        }
        table_prefix = "recovery_wl_data"
        resource.write_data_sheets("recovery_wl_data", output_data)

        for path in [resource.data_path]:
            spath = path / "spatial_outputs"
            spath.mkdir(exist_ok=True)
            tn.df_to_shp(
                wlranks, spath / f"ranked_recovered_wls_{resource.resource_key}.shp"
            )
            tn.df_to_shp(
                wlranks_curr,
                spath / f"ranked_current_recovered_wls_{resource.resource_key}.shp",
            )

        output_data = {table_prefix + "__" + k: v for k, v in output_data.items()}
        return {"output_data": output_data}


waterlevel_analysis_stages = [
    QueryAndValidateWaterLevels,
    CalculateSeasonalWaterLevels,
]
