import sys
from datetime import datetime
import logging
import os
import textwrap
import shutil

import click
import numpy as np
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
@click.option("-s4", "--step4", is_flag=True)
@click.option("-s5", "--step5", is_flag=True)
@click.option("-s6", "--step6", is_flag=True)
@click.option("-s7", "--step7", is_flag=True)
@click.option("-s", "--static", is_flag=True)
@click.option("-r", "--report", default="")
@click.option("--figures/--no-figures", is_flag=True, default=True)
@click.argument("resource", required=False)
def salinities(
    resource,
    reporting_period,
    verbose,
    step4,
    step5,
    step6,
    step7,
    static,
    report,
    figures,
):
    logger.warning(f"wraptn.__version__ == {tn.__version__}")
    return salinities_run(
        resource,
        reporting_period,
        verbose,
        step4,
        step5,
        step6,
        step7,
        static,
        report,
        figures,
    )


def salinities_run(
    resource,
    reporting_period,
    verbose=0,
    step4=True,
    step5=True,
    step6=True,
    step7=True,
    static=True,
    report="",
    figures=True,
):
    handlers = []
    if verbose == 1:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
    if verbose == 2:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
        handlers.append({"sink": "wraptn_salinities.log", "level": "DEBUG"})
    config = {
        "handlers": handlers,
    }
    logger.configure(**config)

    logger.info(f"Using dew_gwdata {gd.__version__}")
    logger.info(f"Using wrap_technote {tn.__version__}")

    plt.rcParams["figure.dpi"] = 105

    db = gd.sageodata()

    if not resource:
        if report:
            logger.info(f"Finding resources for report: {report}")
            report = tn.Report(report, reporting_period)
            df = report.read_table("Report_Resources_mapping")
            resource_keys = [
                r for r in df[df.param == "TDS"].resource_key.unique() if r
            ]
            logger.info(f"Found resources: {resource_keys}")
    else:
        resource_keys = [resource]

    for resource in resource_keys:
        logger.info(
            f"Loading resource {resource} for reporting_period {reporting_period}"
        )
        resource = tn.Resource(resource, reporting_period)

        r = {}
        if step4:
            step4_data_validation(resource, db, plot_figures=figures)
        if step5:
            step5_salinity_trends(resource, db, plot_figures=figures)
        if step6:
            step6_salinity_change(resource, db, plot_figures=figures)
        if step7:
            step7_salinity_indicators(resource, db, plot_figures=figures)

        if static:
            create_static_salinity_page(resource, db)


def step4_data_validation(resource, db, plot_figures=True):
    current_tds_year = resource.trend_dfn.end_year

    resource_key = resource.resource_key
    logger.info(f"Finding wells for {resource_key}...")
    wells = resource.find_wells()
    logger.debug(f"Found wells: {wells}")

    logger.info("Retrieving salinity data...")
    sals0 = db.salinities(wells)
    sals0["database"] = "SA Geodata"

    logger.info("Remove all wells with < 3 observations...")
    sals0 = sals0.groupby("well_id").filter(lambda x: len(x) >= 3)

    logger.info("Filter out or refresh invalidated data...")
    sals, removals = tn.filter_tds_observations(
        sals0, return_removals=True, qc=resource
    )

    logger.info(f"removing any wells with no current data (in {current_tds_year}")
    keep = []
    removing = [removals]
    for well_id, well_sals in sals.groupby("well_id"):
        if current_tds_year in well_sals.collected_date.dt.year.unique():
            keep.append(well_sals)
        else:
            remove = pd.DataFrame(well_sals)
            remove["reason"] = f"No data from current year ({current_tds_year})"
            removing.append(remove)
    removals = pd.concat(removing)
    sals = pd.concat(keep)

    if plot_figures:
        for fn in resource.static_path.glob("plot_tds_data_validation*.png"):
            logger.debug(f"removing old figure: {fn}")
            os.remove(fn)
        logger.info("Plot salinity data validation charts...")
        axes = tn.plot_tds_data_validation(
            sals,
            removals,
            show_comments=True,
            adjust_comments=False,
            savefig_and_close=True,
            path=resource.static_path,
        )

    logger.info(
        f"Selecting valid current year salinities with collected_date.dt.year == {current_tds_year}"
    )
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
    curr_sal_multiples = sals[sals.collected_date.dt.year == current_tds_year]
    curr_sal = (
        curr_sal_multiples.groupby(["well_id"], as_index=False).tds.mean().reset_index()
    )
    curr_sal = pd.merge(
        curr_sal_multiples[cols].drop_duplicates(),
        curr_sal,
        on="well_id",
        how="inner",
    )

    logger.debug(f"curr_sal ('current_mean_tds') {len(curr_sal)} records")

    output_data = {
        "valid_data": sals,
        "invalid_data": removals,
        "current_mean_tds": curr_sal,
    }
    resource.write_data_sheets("validated_data", output_data)

    for path in [resource.data_path]:
        spath = path / "spatial_outputs"
        spath.mkdir(exist_ok=True)
        tn.df_to_shp(curr_sal, spath / f"current_mean_tds_{resource.resource_key}.shp")

    return output_data


def step5_salinity_trends(resource, db, plot_figures=True):
    resource_key = resource.resource_key

    all_data = resource.read_data("validated_data", sheet_name=None)
    tdsdata = all_data["valid data"]
    invalid_tdsdata = all_data["invalid data"]
    # tdsdata = resource.read_data("validated_data", sheet_name="valid data")
    wells = db.drillhole_details(tdsdata.dh_no.unique())

    logger.info(
        "Add decimal number of days to the salinity observation table, to make linear regression easier."
    )

    if "collected_date" in tdsdata:
        tdsdata["ndays"] = tdsdata.collected_date.apply(tn.date_to_decimal)

    logger.info("Remove any wells that don't have data from the trend period.")

    tdsdata = resource.filter_tds_to_wells_with_trend_period_data(tdsdata)

    logger.info("Create a data frame that only has data from the trend period in it")

    trenddf = (
        tdsdata.groupby("well_id", as_index=False)
        .apply(lambda wdf: resource.filter_tds_to_trend_period(wdf))
        .reset_index(drop=True)
    )
    if len(trenddf) == 0:
        cols = list(tdsdata.columns.values)
        cols += [
            "slope_yr",
            "sal_change",
            "sal_pct_change",
            "status_change",
            "status",
            "status_combined",
        ]
        trenddf = pd.DataFrame(
            columns=cols,
        )

    logger.info("Calculate annual mean salinity within the trend period.")

    if len(trenddf):
        ann_mean_df = (
            trenddf.groupby(
                ["well_id", trenddf.collected_date.dt.year], as_index=False
            )[["ndays", "collected_date", "tds"]]
            .mean()
            .reset_index()
            .rename(columns={"collected_date": "collected_year"})
            .set_index("well_id")
        )
    else:
        ann_mean_df = pd.DataFrame(
            columns=list(tdsdata.columns.values)
            + ["collected_year", "ndays", "tds_max_date", "tds_max"]
        ).set_index("well_id")

    if len(ann_mean_df):
        ann_mean_df["collected_date"] = ann_mean_df.ndays.apply(tn.decimal_to_date)
        extrema_map = (
            trenddf[["well_id", "tds_max", "tds_max_date"]]
            .set_index("well_id")
            .drop_duplicates()
        )
        ann_mean_df["tds_max_date"] = ann_mean_df.index.map(extrema_map.tds_max_date)
        ann_mean_df["tds_max"] = ann_mean_df.index.map(extrema_map.tds_max)
    else:
        extrema_map = pd.DataFrame(
            columns=["well_id", "tds_max", "tds_max_date"]
        ).set_index("well_id")

    ann_mean_df = ann_mean_df.reset_index()

    logger.info(
        "Flat out remove all wells with only one data point, because we can't calculate a trend at all."
    )

    num_data = ann_mean_df.groupby("well_id").collected_year.count()

    wells_n1 = num_data[num_data == 1].index.values
    tdsdata = tdsdata[lambda x: ~x.well_id.isin(wells_n1)]
    ann_mean_df = ann_mean_df[~ann_mean_df.well_id.isin(wells_n1)]
    well_ids = ann_mean_df.well_id.unique()

    logger.info(
        "Calculate how many observations fall within the trend period and exclude any if needed."
    )

    vals = resource.read_table("Data_validation")
    excl = vals.query("action == 'Exclude well trend'")
    incl = vals.query("action == 'Include well trend'")
    trendqc = (
        ann_mean_df.groupby("well_id").tds.count().to_frame(name="n_trend_year_obs")
    )
    trendqc["include"] = True
    trendqc["exclusion_reason"] = ""

    for well_id in num_data[num_data < resource.trend_dfn.min_data_pts].index:
        trendqc.loc[well_id, "include"] = False
        trendqc.loc[
            well_id, "exclusion_reason"
        ] = f"Only {num_data.loc[well_id]} years with data points in trend period"

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
                    x = f" (overriding {x}"
                trendqc.loc[well_id, "exclusion_reason"] = (
                    f"{row.username}: {row.comment}" + x
                )

    logger.info("Calculate the trend line by linear regression.")

    welltrends = ann_mean_df.groupby("well_id").apply(
        lambda wdf: resource.apply_trend(wdf)
    )
    if "well_id" in welltrends.columns:
        # This well_id comes from the Trend definition table and should be removed in
        # favour of the index, which contains the actual well ID.
        welltrends = (
            welltrends.drop("well_id", axis="columns")
            .reset_index()
            .set_index("well_id")
        )

    if plot_figures:
        for fn in resource.static_path.glob("plot_salinity_trend*.png"):
            logger.debug(f"removing old figure: {fn}")
            os.remove(fn)
        logger.info("Plot all chart lines.")

        fig = plt.figure(figsize=(7, 3))
        for well_id in sorted(well_ids):
            valid = tdsdata.query(f'well_id == "{well_id}"')
            invalid = invalid_tdsdata.query(f'well_id == "{well_id}"')
            trend_sals = ann_mean_df.query(f'well_id == "{well_id}"')

            ax = fig.add_subplot(111)

            ax = tn.plot_salinity_trend(
                valid,
                trend_sals,
                trend_lines=welltrends,
                excluded_sals=invalid,
                override_year_span="all",
                ax=ax,
            )
            tt = ax._title_text.get_text()
            if trendqc.loc[well_id].include == False:
                exclusion_label = "\n".join(
                    textwrap.wrap(str(trendqc.loc[well_id].exclusion_reason), 50)
                )
                tt += f"\nExcluded: {exclusion_label}"
            else:
                tt += f" - included"
            ax._title_text.set_text(tt)
            fig.tight_layout()
            fn = str(resource.static_path / f"plot_salinity_trend_{well_id}.png")
            fig.savefig(fn, dpi=130)
            tn.trim_whitespace_from_image(fn, append=False)
            fig.clf()

    logger.info("Calculate trend results")

    trend_results = pd.merge(welltrends, trendqc, left_index=True, right_index=True)
    trend_results = trend_results[
        [x for x in trend_results.columns if not x.startswith("Unnamed")]
    ]

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
        tdsdata[cols].drop_duplicates(),
        trend_results,
        on="well_id",
        how="inner",
    )

    if len(trend_results):
        trend_results.loc[
            trend_results["status_change"] == "Decreasing", "gsr_status_colour"
        ] = "Blue"
        trend_results.loc[
            trend_results["status_change"] == "Stable", "gsr_status_colour"
        ] = "Green"
        trend_results.loc[
            trend_results["status_change"] == "Increasing", "gsr_status_colour"
        ] = "Yellow"
        trend_results.loc[
            (trend_results["status_change"] == "Decreasing")
            & (trend_results["status_threshold"].str.startswith("Above")),
            "gsr_status_colour",
        ] = "Purple"
        trend_results.loc[
            (trend_results["status_change"] == "Stable")
            & (trend_results["status_threshold"].str.startswith("Above")),
            "gsr_status_colour",
        ] = "Grey"
        trend_results.loc[
            (trend_results["status_change"] == "Increasing")
            & (trend_results["status_threshold"].str.startswith("Above")),
            "gsr_status_colour",
        ] = "Black"

    logger.info("Write results to spreadsheet...")

    for col in ["status", "status_change", "status_combined", "include"]:
        if not col in trend_results:
            trend_results[col] = ""

    final_trends = trend_results[trend_results.include == True]
    excluded_trends = trend_results[trend_results.include == False]

    output_data = {
        "data_in_trend_period": trenddf,
        "mean_annual_tds_in_trend_pd": ann_mean_df,
        "final_trends": final_trends,
        "excluded_trends": excluded_trends,
        "data_quality": trendqc,
    }
    resource.write_data_sheets("salinity_trends", output_data)

    for path in [resource.data_path]:
        spath = path / "spatial_outputs"
        spath.mkdir(exist_ok=True)
        tn.df_to_shp(
            final_trends, spath / f"salinity_trends_{resource.resource_key}.shp"
        )

    return output_data


def step6_salinity_change(resource, db, plot_figures=True):
    data = resource.read_data("validated_data", sheet_name=None)
    params = resource.read_table("GW_TDS_long_term_changes")

    vdata = data["valid data"]
    if len(vdata):
        vdata["collected_year"] = vdata["collected_date"].dt.year

        wells = db.drillhole_details(data["valid data"].dh_no.unique())
        long_pd_end = pd.Timestamp(f"{int(params.period_end)}-12-31")
        long_pd_start = pd.Timestamp(f"{int(params.long_period_start)}-01-01")

        short_pd_end = pd.Timestamp(f"{int(params.period_end)}-12-31")
        short_pd_start = pd.Timestamp(f"{int(params.short_period_start)}-01-01")

        dt_col = "collected_date"
        long_pd = (vdata[dt_col] >= long_pd_start) & (vdata[dt_col] <= long_pd_end)
        short_pd = (vdata[dt_col] >= short_pd_start) & (vdata[dt_col] <= short_pd_end)

        short_vdata = vdata[short_pd]
        long_vdata = vdata[long_pd]

        short_nyears = short_vdata.groupby("well_id").collected_year.nunique()
        long_nyears = long_vdata.groupby("well_id").collected_year.nunique()

        obs_extent = (
            long_vdata.groupby("well_id")
            .collected_year.agg(["first", "last"])
            .rename(columns={"first": "first_year", "last": "last_year"})
        )

        nobs = pd.merge(
            long_nyears, short_nyears, left_index=True, right_index=True
        ).rename(
            columns={
                "collected_year_x": "long_pd_nyears_w_obs",
                "collected_year_y": "short_pd_nyears_w_obs",
            }
        )

        stats = pd.merge(
            obs_extent, nobs, left_index=True, right_index=True, how="inner"
        )
        stats = stats[stats.first_year < short_pd_start.year].sort_values(
            ["long_pd_nyears_w_obs", "short_pd_nyears_w_obs"], ascending=False
        )

        short_mean_tds = short_vdata.groupby("well_id").tds.mean()
        long_mean_tds = long_vdata.groupby("well_id").tds.mean()
        means = pd.merge(
            long_mean_tds,
            short_mean_tds,
            left_index=True,
            right_index=True,
            how="inner",
        ).rename(columns={"tds_y": "short_pd_tds", "tds_x": "long_pd_tds"})
        means2 = pd.merge(stats, means, left_index=True, right_index=True, how="inner")
        means2["tds_change"] = means2["short_pd_tds"] - means2["long_pd_tds"]
        means2["tds_pct_change"] = means2["tds_change"] / means2["short_pd_tds"] * 100
        means2 = means2.sort_values("tds_pct_change").round(
            {"long_pd_tds": 0, "short_pd_tds": 0, "tds_change": 1, "tds_pct_change": 2}
        )
        cols = [x for x in means2.columns]
        cols.insert(0, "short_period")
        cols.insert(0, "long_period")
        means2["short_period"] = f"{short_pd_start.year} to {short_pd_end.year}"
        means2["long_period"] = f"{long_pd_start.year} to {long_pd_end.year}"
        means2 = means2[cols].sort_values(
            ["long_pd_nyears_w_obs", "short_pd_nyears_w_obs"], ascending=False
        )
    else:
        means2 = pd.DataFrame(
            columns=[
                "well_id",
                "long_period",
                "short_period",
                "first_year",
                "last_year",
                "long_pd_nyears_w_obs",
                "short_pd_nyears_w_obs",
                "long_pd_tds",
                "short_pd_tds",
                "tds_change",
                "tds_pct_change",
            ]
        )
        short_vdata = vdata
        long_vdata = vdata

    means2 = means2.reset_index()

    output_data = {
        "tds_changes": means2,
        "short_period_tds_data": short_vdata,
        "long_period_tds_data": long_vdata,
    }
    resource.write_data_sheets("salinity_long_term_change", output_data)

    return output_data


def step7_salinity_indicators(resource, db, plot_figures=True):
    tds = resource.read_data("validated_data", "valid_data")

    logger.info(f"Reducing validated data to annual mean TDS")
    tdsann = tn.reduce_to_annual_tds(tds, reduction_func="mean")

    logger.info(f"Read Definitions_salinity_indicators")
    dfn = resource.read_table("Definitions_salinity_indicators").iloc[0]
    logger.debug(f"dfn =\n{dfn}")

    logger.info(f"Removing any TDS data > trend_end_year ({dfn.trend_end_year})")
    tdsann = tdsann[tdsann.collected_year <= int(dfn.trend_end_year)]

    logger.info(f"Calculating annual TDS statistics")
    annstats = tn.calculate_annual_tds_stats(tdsann)

    # Plot TDS resoruce monitoring history (mean/stdev salinity vs time for resource)
    logger.info(f"plot_tds_resource_monitoring_history for {resource.resource_key}")
    axes = tn.plot_tds_resource_monitoring_history(annstats)
    for path in [
        resource.data_path,
    ]:
        fn = str(
            path / f"{resource.resource_key}_plot_tds_resource_monitoring_history.png"
        )
        axes[0].figure.savefig(fn, dpi=130)

    # Plot TDS resource variability (mean vs stdev TDS with aspect of n_wells and year)
    logger.info(f"plot_tds_resource_variability for {resource.resource_key}")
    axes = tn.plot_tds_resource_variability(annstats)
    for path in [
        resource.data_path,
    ]:
        fn = str(path / f"{resource.resource_key}_plot_tds_resource_variability.png")
        axes[0].figure.savefig(fn, dpi=130)

    # Generate all salinity results
    logger.info(f"calculate_salinity_indicator_results for {resource.resource_key}")
    r = tn.calculate_salinity_indicator_results(
        tdsann, dfn, trend_length_years=dfn.trend_length_years
    )

    # Apply QC validations.
    r["df"], curr_pct_diff_qc = resource.get_salinity_curr_pct_diff_qc_results(
        r["df"], tdsdf=tdsann
    )
    r["df"], trend_pct_qc = resource.get_salinity_trend_pct_qc_results(
        r["df"], tdsdf=tdsann
    )
    r["df"] = resource.apply_salinity_indicator_validations(r["df"], conn=db)

    # Re-calculate summary tables.
    c, t = tn.calculate_salinity_indicator_summary_results(
        r["df"], r["pct_diff"], r["trend_pct"]
    )
    r["curr_pct_diffs"] = c
    r["tds_trend_pct_changes"] = t
    logger.info(f"Summary curr_pct_diff\n{r['curr_pct_diffs']}")
    logger.info(f"Summary tds_trend_pct_changes\n{r['tds_trend_pct_changes']}")

    # calculate historical pct_diff values
    logger.info(f"calculate_historical_pct_diff_values for {resource.resource_key}")
    tdsann = tn.calculate_historical_pct_diff_values(tdsann, r["pct_diff"])

    if plot_figures:
        for fn in resource.static_path.glob("salinity_status_and_trend_*.png"):
            logger.debug(f"removing old figure: {fn}")
            os.remove(fn)

        # charting individual well status and trend figures
        logger.info(
            f"plot_salinity_status_and_trend_simple_with_indicators for {resource.resource_key}"
        )
        for well_id, wdata in r["data"].items():
            logger.info(f"Plotting salinity status and trend for {well_id}")
            df = wdata["dfs"][-1]["df"]
            trend_df = wdata["dfs"][-1]["trend_df"]
            curr_result = wdata["results"].iloc[-1]
            ax = tn.plot_salinity_status_and_trend_simple_with_indicators(
                df,
                trend_df,
                curr_result,
                r["df"][lambda x: x.well_id == well_id].iloc[0],
                dfn,
            )
            fn = resource.static_path / f"salinity_status_and_trend_{well_id}.png"
            ax.figure.savefig(str(fn), dpi=130)

    if len(tdsann):
        # Plot historical TDS percent differences
        logger.info(f"plot_salinity_historical_pct_diffs for {resource.resource_key}")
        axes = tn.plot_salinity_historical_pct_diffs(
            tdsann,
            r["pct_diff"],
            included_wells=r["df"][
                r["df"].include_curr_pct_diff == True
            ].well_id.unique(),
        )
        for path in [
            resource.data_path,
        ]:
            fn = str(
                path / f"{resource.resource_key}_plot_salinity_historical_pct_diffs.png"
            )
            axes[0].grid(False)
            axes[0].figure.savefig(fn, dpi=130)

    if len(r["curr_pct_diffs"]):
        # plot_salinity_curr_pct_diffs_summary
        logger.info(f"plot_salinity_curr_pct_diffs_summary for {resource.resource_key}")
        ax = tn.plot_salinity_curr_pct_diffs_summary(
            r["curr_pct_diffs"], r["pct_diff"], style="internal", results=r["df"]
        )
        for path in [
            resource.data_path,
        ]:
            fn = str(
                path
                / f"{resource.resource_key}_plot_salinity_curr_pct_diffs_summary.png"
            )
            ax.figure.savefig(fn, dpi=130)

    if len(r["tds_trend_pct_changes"]):
        # plot_salinity_trend_pct_summary
        logger.info(f"plot_salinity_trend_pct_summary for {resource.resource_key}")
        ax = tn.plot_salinity_trend_pct_summary(
            r["tds_trend_pct_changes"],
            r["trend_pct"],
            style="internal",
            results=r["df"],
        )
        for path in [
            resource.data_path,
        ]:
            fn = str(
                path / f"{resource.resource_key}_plot_salinity_trend_pct_summary.png"
            )
            ax.figure.savefig(fn, dpi=130)

    output_data = {
        "annual_mean_tds": tdsann,
        "curr_pct_diff": r["df"][r["df"].include_curr_pct_diff == True],
        "trend_pct": r["df"][r["df"].include_trend_pct == True],
        "excluded_curr_pct_diff": r["df"][r["df"].include_curr_pct_diff == False],
        "excluded_trend_pct": r["df"][r["df"].include_trend_pct == False],
        "all_results": r["df"],
        "curr_pct_diff_summary": r["curr_pct_diffs"],
        "tds_trend_pct_changes_summary": r["tds_trend_pct_changes"],
        "qc_curr_pct_diff": curr_pct_diff_qc.reset_index(),
        "qc_trend_pct_qc": trend_pct_qc.reset_index(),
    }
    resource.write_data_sheets("salinity_indicators", output_data)

    return output_data


def create_static_salinity_page(resource, db):
    logger.info(f"Creating a static page for {resource.resource_key}")

    templates = tn.load_html_templates()

    rp = resource.reporting_period

    retdata = tn.collate_salinity_summary_data(resource, db)
    sentences = tn.construct_salinity_template_sentences(resource, retdata)
    retdata["sentences"] = sentences

    with open(str(resource.static_path / "salinities.html"), mode="w") as html:
        template = templates.get_template("static/salinities.html")
        html.write(template.render(retdata))
