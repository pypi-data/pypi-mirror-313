import sys
from datetime import datetime
import logging
import os
import textwrap
import shutil
import pprint

import click
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

import dew_gwdata as gd  # Access to SA Geodata database
import wrap_technote as tn  # GW data analysis functions


from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


logger = tn.get_logger()


@click.command()
@click.option("-p", "--reporting-period", default=tn.CURRENT_RPERIOD)
@click.option("-v", "--verbose", count=True)
@click.option("-s1", "--step1", is_flag=True)
@click.option("-s2", "--step2", is_flag=True)
@click.option("-s3", "--step3", is_flag=True)
@click.option("-s", "--static", is_flag=True)
@click.option("-r", "--report", default="")
@click.option("--figures/--no-figures", is_flag=True, default=True)
@click.argument("resource", required=False)
def waterlevels(
    resource, reporting_period, verbose, step1, step2, step3, static, report, figures
):
    return waterlevels_run(
        resource,
        reporting_period,
        verbose,
        step1,
        step2,
        step3,
        static,
        report,
        figures,
    )


def waterlevels_run(
    resource,
    reporting_period,
    verbose=0,
    step1=True,
    step2=True,
    step3=True,
    static=True,
    report="",
    figures=True,
):
    """Run the water level data analysis for a WRAP resource.

    Args:
        resource (wrap_tn.Resource): the resource to analyse
        reporting_period (wrap_tn.ReportingPeriod): the reporting period
            to analyse the resource for
        verbose (int): pre-configure loguru logging messages, use
            1 for INFO to console, and 2 for INFO to console & DEBUG to
            a file in the current directory wraptn_waterlevels.log.
            Set to anything else to use whatever loguru is configured for
            via tn.get_logger().configure()
        step1 (bool): execute step 1 of the analysis (see
            :func:`wrap_technote.scripts.step1_data_validation` below)
        step2 (bool): execute step 1 of the analysis (see XXX below)
        step3 (bool): execute step 1 of the analysis (see XXX below)
        static (bool): run the code to create the static site resources
            (see XXX below)
        report (str): ?
        figures (bool): create figures, yes or no. You would only select
            False in order to speed up the execution time of this function.

    """
    handlers = []
    if verbose == 1:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
    if verbose == 2:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
        handlers.append({"sink": "wraptn_waterlevels.log", "level": "DEBUG"})
    config = {
        "handlers": handlers,
    }
    logger.configure(**config)

    logger.info(f"Using dew_gwdata {gd.__version__}")
    logger.info(f"Using wrap_technote {tn.__version__}")

    plt.rcParams["figure.dpi"] = 100

    db = gd.sageodata()

    if not resource:
        if report:
            logger.info(f"Finding resources for report: {report}")
            report = tn.Report(report, reporting_period)
            df = report.read_table("Report_Resources_mapping")
            resource_keys = [r for r in df[df.param == "WL"].resource_key.unique() if r]
            logger.info(f"Found resources: {resource_keys}")
    else:
        resource_keys = [resource]

    for resource in resource_keys:
        logger.info(
            f"Loading resource {resource} for reporting_period {reporting_period}"
        )
        resource = tn.Resource(resource, reporting_period)

        r = {}
        if step1:
            step1_data_validation(resource, db, plot_figures=figures)
        if step2:
            step2_defining_recovered_wls(resource, db, plot_figures=figures)
        if step3:
            step3_waterlevel_trends(resource, db, plot_figures=figures)

        if static:
            create_static_waterlevels_page(resource, db)


def step1_data_validation(resource, db, plot_figures=True):
    aq = gd.DEWAquarius()

    resource_key = resource.resource_key
    logger.info(f"Finding wells for {resource_key}...")
    wells = resource.find_wells()
    include_replacements = resource.well_selection_query.include_replacements

    logger.info(f"{len(wells)} wells with data from at least the reporting period")
    logger.debug(f" wells found: {wells.well_id.tolist()}")

    logger.info(f"Including replaced drillholes? {include_replacements}")

    logger.info("Retrieving manual water level data...")
    # wls = gd.fetch_wl_data(wells, include_replacements=include_replacements)
    sag_wl = db.water_levels(wells)
    sag_wl['database'] = 'SA Geodata'
    sag_wl.loc[sag_wl.anomalous_ind == 'Y', "grade"] = 15
    sag_wl.loc[sag_wl.anomalous_ind == 'N', "grade"] = 30

    logger.info("Identifying wells with logger data...")
    swimsmd = gd.SWIMSMetadata()
    dsets = swimsmd.get_datasets()
    aq_unit_hyphens = dsets[dsets['LocationId'].isin(wells.unit_hyphen.unique())].LocationId.unique()

    logger.info(f"Downloading logger data for {len(aq_unit_hyphens)} wells...")
    all_wl_dfs = [sag_wl]
    for unit_hyphen in aq_unit_hyphens:
        row = wells[wells.unit_hyphen == unit_hyphen].iloc[0]
        logger.info(f" obtaining logger data at 1 day frequency for {unit_hyphen} / {row.obs_no}")
        aq_wl_dfs = aq.fetch_timeseries_data(
            row.unit_hyphen,
            param="rswl",
            freq="1d",
            max_gap_days=550,
            keep_grades=(0, 1, 5, 20, 30),
        )
        aq_wl = gd.join_logger_data_intervals(aq_wl_dfs)
        aq_wl = aq_wl.rename(columns={
            "timestamp": "obs_date",
        })
        keep_cols = ["well_id", "obs_no", "dh_no", "unit_long", "unit_hyphen", "dh_name", "aquifer"]
        for col in keep_cols:
            aq_wl[col] = row[col]
        aq_wl["database"] = "Aquarius"
        aq_wl["anomalous_ind"] = "N"
        aq_wl.loc[(aq_wl.grade <= 0) | (aq_wl.grade == 15), "anomalous_ind"] = "Y"
        if len(aq_wl):
            aq_wl["obs_date"] = aq_wl.obs_date.dt.tz_localize(None)
        keep_cols += ['database', 'obs_date', 'rswl', 'anomalous_ind', "grade"]
        aq_wl = aq_wl[keep_cols]
        all_wl_dfs.append(aq_wl)
    wls = pd.concat(all_wl_dfs)
        
    wls = wls.dropna(subset=["dtw", "swl", "rswl"], how="all")
    logger.debug(f"number of water level observations: {len(wls)}")

    logger.info("Filtering water level observations...")
    wls, removals = tn.filter_wl_observations(wls, return_removals=True, qc=resource)
    logger.debug(
        f"number of water level observations: retained = {len(wls)}; removed = {len(removals)}"
    )

    logger.info("Removing wells with fewer than 5 measurements...")
    wls = wls.groupby("well_id").filter(lambda x: len(x) >= 5)
    # removals = removals[removals.well_id.isin(wls.well_id.unique())]

    logger.info("Creating water level data validation graphs...")
    wls["well_title"] = wls.groupby("well_id").apply(
        lambda f: (f"{f.unit_hyphen.iloc[0]} {f.obs_no.iloc[0]} {f.dh_name.iloc[0]}")
    )
    removals["well_title"] = removals.groupby("well_id").apply(
        lambda f: (f"{f.unit_hyphen.iloc[0]} {f.obs_no.iloc[0]} {f.dh_name.iloc[0]}")
    )

    if resource_key.startswith("Far_North"):
        show_comments = False
    else:
        show_comments = True

    if plot_figures:
        for fn in resource.static_path.glob("plot_wl_data_validation_*.png"):
            logger.debug(f"removing old figure: {fn}")
            os.remove(fn)
        axes = tn.plot_wl_data_validation(
            wls,
            removals,
            well_title_col="well_title",
            show_comments=show_comments,
            adjust_comments=False,
            path=resource.static_path,
            savefig_and_close=True,
            dpi=100,
        )

    output_data = {"valid_data": wls, "invalid_data": removals}
    resource.write_data_sheets("validated_data", output_data)
    return output_data


def step2_defining_recovered_wls(resource, db, plot_figures=True):
    resource_key = resource.resource_key
    wls = resource.read_data("validated_data", sheet_name="valid data")

    wells = db.drillhole_details(wls.dh_no.unique())

    def analyse_wls_by_season(frame):
        well_id = frame.well_id.unique()[0]
        season = resource.get_season(well_id)
        return tn.analyse_wl_by_seasons(frame, season)

    logger.info("Calculating annual recovered water levels...")
    wlann = wls.groupby("well_id").apply(analyse_wls_by_season).reset_index(drop=True)

    # Create a subset of rows with only the recovery water levels.
    wlrec = wlann.loc[wlann.season == "recovery", :]
    logger.info(
        f"Filtering to only those with season == 'recovery' (retained records include wells {wlrec.well_id.unique()})"
    )

    # Remove any recovered levels which are beyond end_recovery_season
    end_y = int(str(resource.trend_dfn.end_recovery_season)[:4])
    wlrec = wlrec[wlrec.season_year.astype(str).str[:4].astype(int) <= end_y]
    logger.debug(
        f"Removed records >= end_recovery season ({resource.trend_dfn.end_recovery_season} -> {end_y}) by looking at column 'season_year'. Max date of remaining data = {wlrec.obs_date.max()}"
    )

    logger.info("Calculating the quality of record for each well...")
    qc, cmp_df = resource.get_wl_ranking_qc_results(wlrec)
    qc_results = pd.merge(
        qc, cmp_df["all_conditions"], left_index=True, right_index=True
    )
    for idx, well_qc_result in qc_results.iterrows():
        logger.info(
            f"\nQC results for {idx}\n" + pprint.pformat(well_qc_result.to_dict())
        )

    vals = resource.read_table("Data_validation")
    incl = vals.query("action == 'Include well in water level rankings'")
    for ix, row in incl.iterrows():
        for well_id in row.well_id.split(","):
            well_id = well_id.strip()
            if well_id in qc_results.index:
                x = qc_results.loc[well_id, "all_conditions"]
                qc_results.loc[well_id, "all_conditions"] = True
                comment = (
                    f"Included True by {row.username}: {row.comment} (overriding {x})"
                )
                qc_results.loc[well_id, "comment"] = comment
                logger.info(f"Data validation. {well_id} include=True {comment}")

    logger.debug(f"wlrec length={len(wlrec)}. Wells: {wlrec.well_id.unique()}")
    wlrec_ranked = wlrec.groupby("well_id", as_index=True).apply(
        lambda df: tn.rank_and_classify(
            df, param_name="rswl", param_col="rswl", dt_col="year+season"
        )
    )
    logger.debug(
        f"wlrec_ranked length={len(wlrec_ranked)}. Columns: {wlrec_ranked.columns}. Index values: \n{wlrec_ranked.index}"
    )
    wlrec_ranked = wlrec_ranked.reset_index(drop=True, level=1)
    wlrec_ranked = wlrec_ranked.drop(["rswl"], axis=1)
    logger.debug(
        f"wlrec_ranked  v2 length={len(wlrec_ranked)}. Columns: {wlrec_ranked.columns}. Index values: \n{wlrec_ranked.index}"
    )

    logger.info("Ranking and classifying recovered water levels for each well...")
    wlranks = pd.merge(
        wlrec.reset_index(),
        wlrec_ranked.reset_index(),
        on=("well_id", "year+season"),
    )
    logger.debug(f"wlranks wells: {wlranks.well_id.unique()}")

    end_year = int(resource.trend_dfn.end_year)
    next_year = end_year + 1
    next_year2 = str(int(next_year))[2:]
    end_year2 = f"{end_year}-{next_year2}"
    curr_year_recovery_seasons = [f"{end_year}-recovery", f"{end_year2}-recovery"]
    logger.info(f"Current year recovery seasons: {curr_year_recovery_seasons}")
    wlranks_curr = wlranks[wlranks["year+season"].isin(curr_year_recovery_seasons)]
    data_quality = (
        qc_results.reset_index()
    )  # pd.merge(qc, cmp_df, left_index=True, right_index=True).reset_index()
    logger.debug(f"data_quality wells: {data_quality.well_id.unique()}")

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

    logger.debug(f"wlranks_included: {wlranks_included.well_id.unique()}")
    logger.debug(f"wlranks_excluded: {wlranks_excluded.well_id.unique()}")
    logger.debug(f"wlranks_curr_included: {wlranks_curr_included.well_id.unique()}")
    logger.debug(f"wlranks_curr_excluded: {wlranks_curr_excluded.well_id.unique()}")

    logger.info("Calculate total water level changes.")
    windows = tn.get_total_wl_change_windows(current_year=end_year)
    total_wl_changes = tn.get_total_wl_changes(wlranks, windows=windows).reset_index()

    if plot_figures:
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

    data_quality = data_quality.reset_index()

    output_data = {
        "annual_recovered_wl": wlrec,
        "ranked_wls": wlranks_included,
        "current_ranked_wls": wlranks_curr_included,
        "ranks_excl": wlranks_excluded,
        "current_ranks_excl": wlranks_curr_excluded,
        "total_wl_changes": total_wl_changes,
        "data_quality": data_quality,
    }
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

    return output_data


def step3_waterlevel_trends(resource, db, plot_figures=True):
    resource_key = resource.resource_key

    wls = resource.read_data("validated_data", sheet_name="valid data")
    if resource.trend_dfn.regress_against.startswith("all"):
        logger.info("Reading all valid data for trend regression.")
        wldata = pd.DataFrame(wls)
        wldata["season_year"] = wldata.obs_date.dt.year
    elif resource.trend_dfn.regress_against.startswith("recovery"):
        logger.info("Reading all recovery seasonal WL data for trend regression.")
        wldata = resource.read_data(
            "recovery_wl_data", sheet_name="annual recovered WL"
        )
    else:
        raise KeyError(
            "Definitions_triclass_trend_thresholds:regress_against must be either 'recovery' or 'all'"
        )
    if "SA Geodata only" in resource.trend_dfn.regress_against:
        wldata = wldata[wldata.database == "SA Geodata"]

    wldata["ndays"] = wldata.obs_date.apply(tn.date_to_decimal)

    logger.info("Filtering data tables to the trend period")
    wldata = wldata.groupby("well_id").filter(resource.test_wls_in_trend_period)

    wells = db.drillhole_details(wldata.dh_no.unique())

    trenddf = (
        wldata.groupby("well_id", as_index=False)
        .apply(lambda wdf: resource.filter_wl_to_trend_period(wdf))
        .reset_index(drop=True)
    )

    logger.info(
        "Calculate how many observations fall within the trend period and exclude any if needed."
    )
    vals = resource.read_table("Data_validation")
    excl = vals[(vals.action == "Exclude well trend") | (vals.action == "Exclude well")]
    incl = vals.query("action == 'Include well trend'")
    trendqc = trenddf.groupby("well_id").rswl.count().to_frame(name="n_trend_obs")
    trendqc["include"] = True
    trendqc["exclusion_reason"] = ""

    for well_id in trendqc[trendqc.n_trend_obs < resource.trend_dfn.min_data_pts].index:
        trendqc.loc[well_id, "include"] = False
        trendqc.loc[
            well_id, "exclusion_reason"
        ] = f"Only {trendqc.loc[well_id].n_trend_obs} data pts in trend period"

    for ix, row in excl.iterrows():
        for well_id in row.well_id.split(","):
            well_id = well_id.strip()
            if well_id in trendqc.index:
                trendqc.loc[well_id, "include"] = False
                trendqc.loc[
                    well_id, "exclusion_reason"
                ] = f"{row.username}: {row.comment}"
    for ix, row in incl.iterrows():
        for well_id in row.well_id.split(","):
            well_id = well_id.strip()
            if well_id in trendqc.index:
                trendqc.loc[well_id, "include"] = True
                x = trendqc.loc[well_id, "exclusion_reason"]
                if x:
                    x = f" (overriding '{x}')"
                trendqc.loc[well_id, "exclusion_reason"] = (
                    f"{row.username}: {row.comment}" + x
                )
    logger.info(str(trendqc))

    logger.info("Calcuate trend line by linear regression...")
    welltrends = trenddf.groupby("well_id").apply(lambda wdf: resource.apply_trend(wdf))

    if plot_figures:
        for fn in resource.static_path.glob("plot_wl_trend_*.png"):
            logger.debug(f"removing old figure: {fn}")
            os.remove(fn)

        trend_line_start = pd.Timestamp(
            f"{int(str(resource.trend_dfn.start_recovery_season)[:4])}-01-01"
        )
        trend_line_end = pd.Timestamp(
            f"{int(str(resource.trend_dfn.end_recovery_season)[:4])}-12-31"
        )

        logger.info("Chart all trend lines...")
        for well_id in sorted(wells.well_id):
            titledf = wldata[wldata.well_id == well_id].iloc[0]
            well_title = f"{titledf.unit_hyphen} {titledf.obs_no} {titledf.dh_name}"
            wldata.loc[wldata.well_id == well_id, "well_title"] = well_title
            logger.info(f"{well_id} ({well_title})...")
            ax = tn.plot_wl_trend(
                wldata.query(f'well_id == "{well_id}"'),
                trenddf.query(f'well_id == "{well_id}"'),
                well_title_col="well_title",
                all_wls=wls.query(f'well_id == "{well_id}"'),
                trend_lines=welltrends,
                trend_line_start=trend_line_start,
                trend_line_end=trend_line_end,
                override_year_span=False,
            )
            tt = ax._title_text.get_text()
            exclusion_label = "\n".join(
                textwrap.wrap(trendqc.loc[well_id].exclusion_reason, 50)
            )
            if not trendqc.loc[well_id].include:
                tt += f"\nExcluded: {exclusion_label}"
            else:
                if exclusion_label:
                    tt += f"\nIncluded: {exclusion_label}"
                else:
                    tt += f" - Included"
            ax._title_text.set_text(tt)
            ax.figure.tight_layout()
            filename = str(resource.static_path / f"plot_wl_trend_{well_id}.png")
            ax.figure.savefig(filename, dpi=100)
            tn.trim_whitespace_from_image(filename, append=False)

    logger.info("Merge trend results into one table...")
    trend_results = pd.merge(
        welltrends,
        trendqc,
        left_on="well_id",
        right_index=True,
    )
    trend_results = trend_results[
        [x for x in trend_results.columns if not x.startswith("Unnamed")]
    ]

    curr_ranks = resource.read_data("recovery_wl_data", "current ranked WLs")

    cols = [
        "well_id",
        "dh_no",
        "unit_long",
        "unit_hyphen",
        "obs_no",
        "dh_name",
        "easting",
        "northing",
        "zone",
        "latitude",
        "longitude",
        "aquifer",
    ]
    trend_results = pd.merge(
        wldata[cols].drop_duplicates(),
        trend_results,
        on="well_id",
        how="inner",
    )

    trend_results["status_combined"] = trend_results["status_change"]
    for well_id in curr_ranks.well_id:
        well_idx = trend_results.well_id == well_id
        if len(well_idx[well_idx == True]) > 0:
            trend_status = trend_results.loc[well_idx, "status_change"].iloc[0]
            rank_status = curr_ranks.loc[
                curr_ranks.well_id == well_id, "rswl_bom_class"
            ].iloc[0]
            trend_results.loc[
                well_idx, "status_combined"
            ] = f"{trend_status} ({rank_status})"
        else:
            trend_results["status_combined"] = trend_results["status_change"]

    trend_results.loc[
        trend_results["status_change"] == "Rising", "gsr_status_colour"
    ] = "Blue"
    trend_results.loc[
        trend_results["status_change"] == "Stable", "gsr_status_colour"
    ] = "Green"
    trend_results.loc[
        trend_results["status_change"] == "Declining", "gsr_status_colour"
    ] = "Yellow"
    trend_results.loc[
        trend_results["status_combined"] == "Rising (Lowest on record)",
        "gsr_status_colour",
    ] = "Purple"
    trend_results.loc[
        trend_results["status_combined"] == "Stable (Lowest on record)",
        "gsr_status_colour",
    ] = "Grey"
    trend_results.loc[
        trend_results["status_combined"] == "Declining (Lowest on record)",
        "gsr_status_colour",
    ] = "Black"

    wldata = wldata.reset_index()
    trenddf = trenddf.reset_index()
    final_trends = trend_results[trend_results.include == True].reset_index()
    excluded_trends = trend_results[trend_results.include == False].reset_index()
    trendqc = trendqc.reset_index()

    output_data = {
        "wl_data": wldata,
        "wls_in_trend_period": trenddf,
        "trend_qc": trendqc,
        "final_trends": final_trends,
        "excluded_trends": excluded_trends,
    }
    resource.write_data_sheets("recovery_wl_trends", output_data)

    for path in [resource.data_path]:
        spath = path / "spatial_outputs"
        spath.mkdir(exist_ok=True)
        tn.df_to_shp(
            final_trends, spath / f"recovered_wl_trends_{resource.resource_key}.shp"
        )

    return output_data


def create_static_waterlevels_page(resource, db):
    templates = tn.load_html_templates()
    template = templates.get_template("static/waterlevels.html")

    retdata = tn.collate_waterlevel_summary_data(resource, db)
    sentences = tn.construct_waterlevel_template_sentences(resource, retdata)
    retdata["sentences"] = sentences

    with open(str(resource.static_path / "waterlevels.html"), mode="w") as html:
        html.write(template.render(retdata))


if __name__ == "__main__":
    run()
