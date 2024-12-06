import sys
import logging
from pprint import pprint
import re
import os
import subprocess
import sys
from pathlib import Path

import click
import pandas as pd

logging.getLogger("matplotlib").setLevel(logging.CRITICAL)
logging.getLogger("fiona").setLevel(logging.CRITICAL)
logging.getLogger("PIL").setLevel(logging.CRITICAL)

import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib import colors as mcolors
from matplotlib import ticker as mticker
from matplotlib import patches as mpatches
import geopandas as gpd
import numpy as np
import pyproj

import dew_gwdata as gd
import ausweather
import wrap_technote as tn


logger = tn.get_logger()


@click.command()
@click.option("-p", "--reporting-period", default=tn.CURRENT_RPERIOD)
@click.option("-v", "--verbose", count=True)
@click.option("-k", "--resource-key", default=None)
@click.option("-r", "--report-key", default=None)
@click.option("--local/--no-local", default=True)
@click.option("--nbs/--no-nbs", default=True)
@click.option("--chart-glob", default=".*")
def summaries(
    reporting_period, report_key, verbose, resource_key, local, nbs, chart_glob
):
    return summaries_run(
        reporting_period, report_key, verbose, resource_key, local, nbs, chart_glob
    )


def summaries_run(
    reporting_period,
    report_key,
    verbose=0,
    resource_key=None,
    local=True,
    nbs=True,
    chart_glob=".*",
):
    handlers = []
    if verbose == 1:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
    if verbose == 2:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
        handlers.append({"sink": "wraptn_summaries.log", "level": "DEBUG"})
    config = {
        "handlers": handlers,
    }
    logger.configure(**config)

    logger.info(f"Using dew_gwdata {gd.__version__}")
    logger.info(f"Using wrap_technote {tn.__version__}")
    logger.info(f"Using ausweather {ausweather.__version__}")

    logger.info(f"Using reporting_period; {reporting_period}")

    logger.debug(f"chart_glob = {chart_glob}")

    plt.rcParams["figure.dpi"] = 150

    if resource_key is not None:
        if not resource_key == "none":
            report = tn.Report(report_key, reporting_period)
            logger.info(
                f"resource_key {resource_key} was specified; making summaries for that resource only."
            )
            make_summaries_for_resource(report, resource_key, chart_glob=chart_glob)

    if resource_key is None:
        logger.info(
            f"resource_key was not specified; making summaries for all resources in {report_key} report"
        )
        make_summaries_for_report(
            report_key, reporting_period, nbs=nbs, chart_glob=chart_glob
        )

    if resource_key is None or resource_key == "none":
        logger.info(f"Creating static HTML page for {report_key} report")
        create_static_summaries_page(report_key, reporting_period, local=local)


def create_static_summaries_page(report_key, reporting_period, local=False):
    logger.info(
        f"Creating static HTML page for {reporting_period}  {report_key} report"
    )
    report = tn.Report(report_key, reporting_period)
    templates = tn.load_html_templates()
    template = templates.get_template("static/gw_summary.html")

    resource_key_paths = {}
    resources = {}
    for section_name, section in report.report_settings.resources.items():
        logger.info(f"Working on section: {section_name}")
        for param, resource_keys in section.items():
            for resource_key in resource_keys:
                logger.info(
                    f"section={section_name} param={param} resource_key={resource_key}"
                )
                r = tn.Resource(resource_key, reporting_period)
                maptable = r.read_table("Report_Resources_mapping")
                logger.info(f"Adding link to {resource_key} static page...")
                if local:
                    path = maptable[maptable.param == param].path.iloc[0]
                    parts = Path(path).parts[2:]
                    p = Path("..")
                    for part in parts:
                        p = p / part
                else:
                    p = r.data_path
                if param == "WL":
                    resource_key_paths[resource_key] = (
                        p / "technote_static" / "waterlevels.html"
                    )
                elif param == "TDS":
                    resource_key_paths[resource_key] = (
                        p / "technote_static" / "salinities.html"
                    )
                resources[resource_key] = tn.load_resource(
                    resource_key, reporting_period
                )

    logger.info(f"Creating static page for {report_key}")
    if local:
        page_path = "."
    else:
        page_path = report.gw_summaries_path

    resource_sentences = {}
    for resource_key, resource in resources.items():
        if resource_key.endswith("WL"):
            retdata = tn.collate_waterlevel_summary_data(resource)
            sentences = tn.construct_waterlevel_template_sentences(resource, retdata)
            resource_sentences[resource_key] = sentences

        elif resource_key.endswith("TDS"):
            retdata = tn.collate_salinity_summary_data(resource)
            sentences = tn.construct_salinity_template_sentences(resource, retdata)
            resource_sentences[resource_key] = sentences

    with open(str(report.gw_summaries_path / "gw_summary.html"), mode="w") as html:
        html.write(
            template.render(
                {
                    "report": report,
                    "page_path": page_path,
                    "resource_key_paths": resource_key_paths,
                    "resource_sentences": resource_sentences,
                    "resources": resources,
                }
            )
        )


def make_summaries_for_report(report_key, reporting_period, nbs=True, chart_glob=".*"):
    logger.info(f"Making summaries for report: {report_key}")
    report = tn.Report(report_key, reporting_period)

    if nbs:
        path = report.gw_summaries_path.parent
        if path.glob("*.ipynb"):
            with tn.cd(path):
                subprocess.call(
                    [
                        "jupyter",
                        "nbconvert",
                        "--ExecutePreprocessor.kernel_name=python3",
                        "--execute",
                        "--to",
                        "html",
                        "*.ipynb",
                    ]
                )

    logger.info("Loading aggregate resources data.")
    wl_agg_ranks = report.get_aggregate_resources_data(
        "WL", "recovery_wl_data", "current ranked WLs"
    )
    wl_agg_trends = report.get_aggregate_resources_data(
        "WL", "recovery_wl_trends", "final trends"
    )
    tds_agg_trends = report.get_aggregate_resources_data(
        "TDS", "salinity_trends", "final trends"
    )

    for agg_key, df in wl_agg_ranks.items():
        for path in [report.gw_summaries_path]:
            fn = f"{agg_key} - recovery_wl_data__current_ranked_wls.csv"
            fn_path = path / fn
            df.to_csv(fn_path, index=False)

    for agg_key, df in wl_agg_trends.items():
        for path in [report.gw_summaries_path]:
            fn = f"{agg_key} - recovery_wl_trends__final_trends.csv"
            fn_path = path / fn
            df.to_csv(fn_path, index=False)

    for agg_key, df in tds_agg_trends.items():
        for path in [report.gw_summaries_path]:
            fn = f"{agg_key} - salinity_trends__final_trends.csv"
            fn_path = path / fn
            df.to_csv(fn_path, index=False)

    chart_glob_re = re.compile(chart_glob)

    if chart_glob_re.match("aggregate_current_WL_rankings"):
        logger.info("Plotting _aggregate_current_WL_rankings")
        filename = f"{report.report_key}_aggregate_current_WL_rankings.png"
        bcmap = tn.BoMClassesColormap()
        ax = tn.plot_internal_classes_for_aggregate_resources(
            wl_agg_ranks, bcmap.class_names, bcmap.colours_rgba(), col="rswl_bom_class"
        )
        ax.set_title(
            f"{report.report_key} Aggregate current WL rankings", fontsize="medium"
        )
        ax.figure.tight_layout()
        for path in [report.gw_summaries_path]:
            fn = str(path / filename)
            ax.figure.savefig(fn, dpi=150)
            tn.trim_whitespace_from_image(fn, append=False)

    if chart_glob_re.match("aggregate_5yr_WL_trends_triclass"):
        logger.info("Plotting _aggregate_5yr_WL_trends_triclass")
        filename = f"{report.report_key}_aggregate_5yr_WL_trends_triclass.png"
        bcmap = tn.BoMClassesColormap()
        ax = tn.plot_internal_classes_for_aggregate_resources(
            wl_agg_trends,
            tn.wl_status_changes,
            tn.wl_status_change_colours,
            col="status_change",
        )
        ax.set_title(f"{report.report_key} Aggregate 5-yr WL trends", fontsize="medium")
        ax.figure.tight_layout()
        for path in [report.gw_summaries_path]:
            fn = str(path / filename)
            ax.figure.savefig(fn, dpi=150)
            tn.trim_whitespace_from_image(fn, append=False)

    if chart_glob_re.match("aggregate_5yr_TDS_trends_triclass"):
        logger.info("Plotting _aggregate_5yr_TDS_trends_triclass")
        filename = f"{report.report_key}_aggregate_5yr_TDS_trends_triclass.png"
        ax = tn.plot_internal_classes_for_aggregate_resources(
            tds_agg_trends,
            tn.tds_status_changes,
            tn.tds_status_change_colours,
            col="status_change",
        )
        ax.set_title(
            f"{report.report_key} Aggregate 5-yr TDS trends", fontsize="medium"
        )
        ax.figure.tight_layout()
        for path in [report.gw_summaries_path]:
            fn = str(path / filename)
            ax.figure.savefig(fn, dpi=150)
            tn.trim_whitespace_from_image(fn, append=False)

    for section_name, section in report.report_settings.resources.items():
        logger.info(f"Working on report section: {section_name}")
        for param, resource_keys in section.items():
            logger.info(f"Iterating over {len(resource_keys)} {param} resource_keys:")
            for resource_key in resource_keys:
                logger.info(f"Loading settings for {resource_key}")
                try:
                    settings = report.resource_settings(resource_key)
                except ModuleNotFoundError:
                    logger.info("No settings found, moving to the next resource.")
                    continue
                else:
                    make_summaries_for_resource(
                        report, resource_key, chart_glob=chart_glob
                    )


def make_summaries_for_resource(report, resource_key, chart_glob=".*"):
    if resource_key.endswith("WL"):
        return make_wl_summaries(report, resource_key, chart_glob=chart_glob)
    elif resource_key.endswith("TDS"):
        return make_tds_summaries(report, resource_key, chart_glob=chart_glob)


def make_wl_summaries(report, resource_key, chart_glob=".*"):
    logger.info(
        f"Making WL summaries for report='{report.report_key}' resource='{resource_key}'"
    )
    resource = tn.Resource(
        resource_key, tn.paths_reporting_period[report.reporting_period.path]
    )
    s = report.resource_settings(resource_key)
    ranks_data = resource.read_data("recovery_wl_data", sheet_name=None)
    logger.info(f"recovery_wl_data sheet names: {ranks_data.keys()}")
    wlranks = ranks_data["ranked WLs"]
    all_wlranks = pd.concat([wlranks, ranks_data["ranks excl"]])
    ranks_qc = ranks_data["data quality"]
    logger.info(f"{len(wlranks.well_id.unique())} wells with historical ranked WLs")
    wlranks = pd.concat([wlranks, s.dry_rows])

    curr_ranks = ranks_data["current ranked WLs"]
    logger.info(f"{len(curr_ranks)} with current year WL rank")

    logger.debug(f"Compiling chart_glob = {chart_glob}")
    chart_glob_re = re.compile(chart_glob)

    if len(curr_ranks):
        if chart_glob_re.match("rankings"):
            ax = tn.plot_wl_ranking_classes(curr_ranks)
            ax.figure.tight_layout()
            filename = f"{resource_key}_rankings.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

            ax = tn.plot_wl_ranking_map(
                curr_ranks,
                s.ranking_map_elements,
                s.ranking_map_annotations,
                leg_frame=s.leg_frame,
                leg_loc=s.leg_loc,
                markersize=s.wl_ranking_marker_size,
            )
            x0, x1 = ax.get_xlim()
            y0, y1 = ax.get_ylim()
            ax.set_xlim(
                x0 + s.ranking_map_xaxis_shift[0], x1 + s.ranking_map_xaxis_shift[1]
            )
            ax.set_ylim(
                y0 + s.ranking_map_yaxis_shift[0], y1 + s.ranking_map_yaxis_shift[1]
            )
            ax.set_xlim(*s.ranking_map_limits["x"])
            ax.set_ylim(*s.ranking_map_limits["y"])
            ax.figure.tight_layout()
            filename = f"{resource_key}_rankings_map.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

        if chart_glob_re.match("wl_rankings_internal"):
            logger.info("Charting: tn.plot_wl_rankings_internal")
            fig = tn.plot_wl_rankings_internal(curr_ranks, title=resource.resource_key)
            filename = f"{resource.resource_key}_wl_rankings_internal.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                fig.savefig(fn, dpi=120)
                tn.trim_whitespace_from_image(fn, append=False)

        if chart_glob_re.match("wl_historical_rankings"):
            logger.info("Charting:tn.plot_wl_historical_rankings")
            fig = tn.plot_wl_historical_rankings(
                all_wlranks, ranks_qc, title=resource.resource_key
            )
            filename = f"{resource.resource_key}_wl_historical_rankings.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                fig.savefig(fn, dpi=120)
                tn.trim_whitespace_from_image(fn, append=False)

    logger.info("Load trend data")
    wl_trend_data = resource.read_data("recovery_wl_trends", sheet_name=None)
    wl_trend_df = wl_trend_data["final trends"]
    wl_annual_threshold = resource.trend_dfn.ann_rate_threshold

    if len(wl_trend_df):
        if chart_glob_re.match("trend_triclass"):
            ax = tn.plot_wl_trend_triclass_bars(wl_trend_df)
            if s.trend_triclass_xticks:
                ax.set_xticks(s.trend_triclass_xticks)
            ax.figure.tight_layout()
            filename = f"{resource_key}_trend_triclass.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

            ax = tn.plot_wl_trend_triclass_map(
                wl_trend_df,
                s.trend_map_elements,
                s.trend_map_annotations,
                leg_frame=s.leg_frame,
                leg_loc=s.leg_loc,
                markersize=s.wl_trend_marker_size,
            )
            x0, x1 = ax.get_xlim()
            y0, y1 = ax.get_ylim()
            ax.set_xlim(
                x0 + s.trend_map_xaxis_shift[0], x1 + s.trend_map_xaxis_shift[1]
            )
            ax.set_ylim(
                y0 + s.trend_map_yaxis_shift[0], y1 + s.trend_map_yaxis_shift[1]
            )
            ax.set_xlim(*s.trend_map_limits["x"])
            ax.set_ylim(*s.trend_map_limits["y"])
            ax.figure.tight_layout()

        if chart_glob_re.match("wl_trends_internal"):
            logger.info("Charting: tn.plot_wl_trends_internal")
            fig = tn.plot_wl_trends_internal(wl_trend_df, title=resource.resource_key)
            filename = f"{resource.resource_key}_wl_trends_internal.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                fig.savefig(fn, dpi=120)
                tn.trim_whitespace_from_image(fn, append=False)

        if chart_glob_re.match("trend_triclass_map"):
            filename = f"{resource_key}_trend_triclass_map.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)


def make_tds_summaries(report, resource_key, chart_glob=".*"):
    logger.info(
        f"Making TDS summaries for report='{report.report_key}' resource='{resource_key}'"
    )
    resource = tn.Resource(
        resource_key, tn.paths_reporting_period[report.reporting_period.path]
    )
    current_tds_year = resource.trend_dfn.end_year
    dfn = resource.read_table("Definitions_salinity_indicators").iloc[0]

    s = report.resource_settings(resource_key)
    valid_sal_sheet = resource.read_data("validated_data", sheet_name=None)
    valid_sal = valid_sal_sheet["valid data"]
    curr_sal = valid_sal_sheet["current_mean_tds"]

    chart_glob_re = re.compile(chart_glob)

    if len(curr_sal):
        if chart_glob_re.match("current"):
            tdsbins = tn.calculate_tds_bins(
                curr_sal,
                tds_bin_width=s.tds_bin_width,
                min_tds_colour=s.min_tds_colour,
                max_tds_colour=s.max_tds_colour,
                cmap=s.tds_cmap,
                min_tds_bin=s.min_tds_bin,
                max_tds_bin=s.max_tds_bin,
            )
            ax = tn.plot_tds_current_bars(
                tdsbins,
            )
            ax.figure.tight_layout()
            filename = f"{resource_key}_current.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

            ax = tn.plot_tds_current_map(
                tdsbins,
                curr_sal,
                s.current_map_elements,
                s.current_map_annotations,
                cmap=s.tds_cmap,
                leg_frame=s.leg_frame,
                leg_loc=s.leg_loc,
                markersize=s.tds_current_marker_size,
            )
            x0, x1 = ax.get_xlim()
            y0, y1 = ax.get_ylim()
            ax.set_xlim(
                x0 + s.current_map_xaxis_shift[0], x1 + s.current_map_xaxis_shift[1]
            )
            ax.set_ylim(
                y0 + s.current_map_yaxis_shift[0], y1 + s.current_map_yaxis_shift[1]
            )
            ax.set_xlim(*s.current_map_limits["x"])
            ax.set_ylim(*s.current_map_limits["y"])
            ax.figure.tight_layout()
            filename = f"{resource_key}_current_map.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

        if chart_glob_re.match("tds_current_internal"):
            logger.info("Charting: tn.plot_tds_current_internal")
            ax = tn.plot_tds_current_internal(curr_sal, title=resource.resource_key)
            filename = f"{resource.resource_key}_tds_current_internal.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.tight_layout()
                ax.figure.savefig(fn, dpi=120)
                tn.trim_whitespace_from_image(fn, append=False)

    # Long-term salinity indicators
    sal_inds = resource.read_data("salinity_indicators", "all_results")
    sal_inds = pd.merge(
        sal_inds,
        valid_sal[["well_id", "longitude", "latitude"]].drop_duplicates(),
        on="well_id",
    )
    curr_pct_diff = sal_inds[sal_inds.include_curr_pct_diff == True]
    trend_pcts = sal_inds[sal_inds.include_trend_pct == True]
    curr_pct_diffs = resource.read_data("salinity_indicators", "curr_pct_diff_summary")
    trend_pct_changes = resource.read_data(
        "salinity_indicators", "tds_trend_pct_changes_summary"
    )

    if len(curr_pct_diff):
        if chart_glob_re.match("curr_pct_diff"):
            logger.info("Charting: tn.plot_tds_curr_pct_diff_bars")
            pct_diff = tn.generate_salinity_bins(
                range_min=float(dfn.pct_diff_range_min),
                range_max=float(dfn.pct_diff_range_max),
                step=float(dfn.pct_diff_step),
                word_positive="above",
                word_negative="below",
                label_fmt="{bin_left}% to {bin_right}% {word} mean",
                end_label_fmt="More than {bin_left}% {word} mean",
            )
            ax = tn.plot_tds_curr_pct_diff_bars(curr_pct_diffs, pct_diff)
            ax.figure.tight_layout()
            filename = f"{resource_key}_curr_pct_diff_bars.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

            logger.info("Charting: tn.plot_tds_curr_pct_diff_map")
            ax = tn.plot_tds_curr_pct_diff_map(
                curr_pct_diff,
                pct_diff,
                s.tds_curr_pct_diff_map_elements,
                s.tds_curr_pct_diff_map_annotations,
                leg_frame=s.leg_frame,
                leg_loc=s.leg_loc,
                markersize=s.tds_curr_pct_diff_marker_size,
            )
            x0, x1 = ax.get_xlim()
            y0, y1 = ax.get_ylim()
            ax.set_xlim(
                x0 + s.tds_curr_pct_diff_map_xaxis_shift[0],
                x1 + s.tds_curr_pct_diff_map_xaxis_shift[1],
            )
            ax.set_ylim(
                y0 + s.tds_curr_pct_diff_map_yaxis_shift[0],
                y1 + s.tds_curr_pct_diff_map_yaxis_shift[1],
            )
            ax.set_xlim(*s.tds_curr_pct_diff_map_limits["x"])
            ax.set_ylim(*s.tds_curr_pct_diff_map_limits["y"])
            ax.figure.tight_layout()
            filename = f"{resource_key}_curr_pct_diff_map.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

    if len(trend_pcts):
        if chart_glob_re.match("trend_pct"):
            trend_pct = tn.generate_salinity_bins(
                range_min=float(dfn.trend_pct_range_min),
                range_max=float(dfn.trend_pct_range_max),
                step=float(dfn.trend_pct_step),
            )

            logger.info("Charting: tn.plot_tds_trend_pct_change_bars")
            ax = tn.plot_tds_trend_pct_change_bars(trend_pct_changes, trend_pct)
            ax.figure.tight_layout()
            filename = f"{resource_key}_tds_trend_pct_change_bars.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

            logger.info("Charting: tn.plot_tds_trend_pct_change_map")
            ax = tn.plot_tds_trend_pct_change_map(
                trend_pcts,
                trend_pct,
                s.tds_trend_pct_change_map_elements,
                s.tds_trend_pct_change_map_annotations,
                leg_frame=s.leg_frame,
                leg_loc=s.leg_loc,
                markersize=s.tds_trend_pct_change_marker_size,
            )
            x0, x1 = ax.get_xlim()
            y0, y1 = ax.get_ylim()
            ax.set_xlim(
                x0 + s.tds_trend_pct_change_map_xaxis_shift[0],
                x1 + s.tds_trend_pct_change_map_xaxis_shift[1],
            )
            ax.set_ylim(
                y0 + s.tds_trend_pct_change_map_yaxis_shift[0],
                y1 + s.tds_trend_pct_change_map_yaxis_shift[1],
            )
            ax.set_xlim(*s.tds_trend_pct_change_map_limits["x"])
            ax.set_ylim(*s.tds_trend_pct_change_map_limits["y"])
            ax.figure.tight_layout()
            filename = f"{resource_key}_tds_trend_pct_change_map.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

    for path in [report.gw_summaries_path]:
        spath = path / "spatial_outputs"
        spath.mkdir(exist_ok=True)

        curr_pct_diff_gdf = gpd.GeoDataFrame(
            curr_pct_diff,
            geometry=gpd.points_from_xy(
                curr_pct_diff.longitude, curr_pct_diff.latitude
            ),
            crs="EPSG:7844",
        )
        if len(curr_pct_diff_gdf):
            tn.df_to_shp(
                curr_pct_diff_gdf,
                spath / f"salinity_curr_pct_diff_{resource.resource_key}.shp",
            )

        trend_pcts_gdf = gpd.GeoDataFrame(
            trend_pcts,
            geometry=gpd.points_from_xy(trend_pcts.longitude, trend_pcts.latitude),
            crs="EPSG:7844",
        )
        if len(trend_pcts_gdf):
            tn.df_to_shp(
                trend_pcts_gdf,
                spath / f"salinity_longterm_trend_pcts_{resource.resource_key}.shp",
            )

    sal_trend_sheet = resource.read_data("salinity_trends", sheet_name=None)
    sal_trends = sal_trend_sheet["final trends"]

    for path in [report.gw_summaries_path]:
        spath = path / "spatial_outputs"
        spath.mkdir(exist_ok=True)

        curr_gdf = gpd.GeoDataFrame(
            curr_sal,
            geometry=gpd.points_from_xy(curr_sal.longitude, curr_sal.latitude),
            crs="EPSG:7844",
        )
        if len(curr_gdf):
            tn.df_to_shp(
                curr_gdf, spath / f"salinity_current_mean_{resource.resource_key}.shp"
            )

        trend_gdf = gpd.GeoDataFrame(
            sal_trends,
            geometry=gpd.points_from_xy(sal_trends.longitude, sal_trends.latitude),
            crs="EPSG:7844",
        )
        if len(trend_gdf):
            tn.df_to_shp(
                trend_gdf,
                spath / f"salinity_triclass_trends_{resource.resource_key}.shp",
            )

    if len(sal_trends):
        if chart_glob_re.match("trend_triclass"):
            ax = tn.plot_tds_trend_triclass_bars(sal_trends)
            if s.trend_triclass_xticks:
                ax.set_xticks(s.trend_triclass_xticks)
            ax.figure.tight_layout()
            filename = f"{resource_key}_trend_triclass.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

            ax = tn.plot_tds_trend_triclass_map(
                sal_trends,
                s.trend_map_elements,
                s.trend_map_annotations,
                leg_frame=s.leg_frame,
                leg_loc=s.leg_loc,
                markersize=s.tds_trend_marker_size,
            )
            x0, x1 = ax.get_xlim()
            y0, y1 = ax.get_ylim()
            ax.set_xlim(
                x0 + s.trend_map_xaxis_shift[0], x1 + s.trend_map_xaxis_shift[1]
            )
            ax.set_ylim(
                y0 + s.trend_map_yaxis_shift[0], y1 + s.trend_map_yaxis_shift[1]
            )
            ax.set_xlim(*s.trend_map_limits["x"])
            ax.set_ylim(*s.trend_map_limits["y"])
            ax.figure.tight_layout()
            filename = f"{resource_key}_trend_triclass_map.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                ax.figure.savefig(fn, dpi=250)
                tn.trim_whitespace_from_image(fn, append=False)

        if chart_glob_re.match("tds_trends_mgL_internal"):
            logger.info("Charting: tn.plot_tds_trends_internal mg/L")
            fig = tn.plot_tds_trends_internal(
                sal_trends, title=resource.resource_key, param="mg"
            )
            filename = f"{resource.resource_key}_tds_trends_mgL_internal.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                fig.savefig(fn, dpi=120)
                tn.trim_whitespace_from_image(fn, append=False)

        if chart_glob_re.match("tds_trends_5yr_pct_internal"):
            logger.info("Charting: tn.plot_tds_trends_internal 5yr_pct")
            fig = tn.plot_tds_trends_internal(
                sal_trends, title=resource.resource_key, param="5yr_pct"
            )
            filename = f"{resource.resource_key}_tds_trends_5yr_pct_internal.png"
            for path in [resource.data_path, report.gw_summaries_path]:
                fn = str(path / filename)
                fig.savefig(fn, dpi=120)
                tn.trim_whitespace_from_image(fn, append=False)
