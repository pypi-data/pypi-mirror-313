import sys
from datetime import datetime
import logging
import os

import click
import matplotlib.pyplot as plt
import pandas as pd

import dew_gwdata as gd  # Access to SA Geodata database
import wrap_technote as tn  # GW data analysis functions
import ausweather

from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


logger = tn.get_logger()

from ..charts_utils import apply_technote_chart_style

apply_technote_chart_style()


@click.command()
@click.option("-p", "--reporting-period", default=tn.CURRENT_RPERIOD)
@click.option("-v", "--verbose", count=True)
@click.option("--overwrite/--no-overwrite", default=True, help="True by default")
@click.option("--download/--no-download", default=False, help="False by default")
@click.option("--figures/--no-figures", default=True, help="True by default")
@click.option("--static/--no-static", default=True, help="True by default")
@click.option("--id-glob", default="*", help="match only one or two station IDs")
@click.option("--name-glob", default="*", help="match only one or two station names")
@click.option(
    "--internal-only/--no-internal-only", default=False, help="False by default"
)
@click.argument("report_key")
def rainfall(
    report_key,
    reporting_period,
    verbose,
    static,
    overwrite,
    download,
    figures,
    id_glob,
    name_glob,
    internal_only,
):
    return rainfall_run(
        report_key=report_key,
        reporting_period=reporting_period,
        verbose=verbose,
        static=static,
        overwrite=overwrite,
        download=download,
        figures=figures,
        id_glob=id_glob,
        name_glob=name_glob,
        internal_only=internal_only,
    )


def rainfall_run(
    report_key,
    reporting_period,
    verbose=0,
    static=True,
    overwrite=True,
    download=False,
    figures=True,
    id_glob="*",
    name_glob="*",
    internal_only=False,
):
    handlers = []
    if verbose == 1:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
    if verbose == 2:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
        handlers.append({"sink": "wraptn_rainfall.log", "level": "DEBUG"})
    config = {
        "handlers": handlers,
    }
    logger.configure(**config)

    logger.info(f"Using dew_gwdata {gd.__version__}")
    logger.info(f"Using wrap_technote {tn.__version__}")
    logger.info(f"Using ausweather {ausweather.__version__}")

    plt.rcParams["figure.dpi"] = 120

    logger.info(f"Loading report {report_key} for reporting_period {reporting_period}")
    logger.info(f"download={download} overwrite={overwrite} figures={figures}")

    report = tn.load_report(report_key, reporting_period)

    report.rainfall_path.mkdir(exist_ok=True, parents=True)

    # Download and store data.
    # logger.info(f"{report.path}")

    if download:
        logger.info("Downloading")
        for station_id in report.read_table("Report_Rainfall_stations").station_id:
            rrow = report.rainfall_dfn(station_id)
            if rrow.station_type == "BoM":
                logger.info(f"Downloading {station_id} from {rrow.data_start}")
                rf = tn.RainfallStationData.from_bom_via_silo(
                    station_id, data_start=rrow.data_start
                )

            elif rrow.station_type in ("Hydstra", "Aquarius"):
                rf = tn.RainfallStationData.from_aquarius(
                    station_id, data_start=rrow.data_start
                )

            rf.save_to_excel(report, overwrite=overwrite)
            rf.save_to_database(report)

            # data = ausweather.fetch_bom_station_from_silo(
            #     station_id, "groundwater@sa.gov.au", rrow.data_start
            # )
            # stub = f'{data["station_no"]}_{data["station_name"]}'
            # data["df"].loc[:, "wu_year"] = [
            #     tn.date_to_wateruseyear(d) for d in data["df"].Date
            # ]
            # data["wateruse_year"] = (
            #     data["df"].groupby("wu_year").Rain.sum().reset_index()
            # )

            # excel_filename = (
            #     report.rainfall_path / f"silo_data_{report.report_key}_{stub}.xlsx"
            # )
            # if overwrite:
            #     with pd.ExcelWriter(excel_filename) as writer:
            #         data["df"].to_excel(writer, "daily", index=False)
            #         data["annual"].reset_index().to_excel(
            #             writer, "annual (calendar)", index=False
            #         )
            #         data["srn"].reset_index().to_excel(
            #             writer, "annual provenance", index=False
            #         )
            #         data["wateruse_year"].reset_index().to_excel(
            #             writer, "annual (water-use year)", index=False
            #         )

    logger.info(f"Finding stations matching id_glob={id_glob} name_glob={name_glob}")
    stations = report.find_rainfall_stations(id_glob=id_glob, name_glob=name_glob)
    logger.info(f"Found {len(stations)} stations")
    dfs = {}
    dfns = {}
    for station in stations:
        logger.info(f"Loading data for {station['id']} {station['name']}")
        dfs[station["id"]] = report.get_all_rainfall_data(station)
        dfns[station["id"]] = report.rainfall_dfn(station["id"])

    # Make charts and spreadsheet.
    if figures:
        for station in stations:
            sid = station["id"]
            name = station["name"]

            logger.info(f"Making graphs for {sid} {name}")
            dfn = dfns[station["id"]]
            ann_calendar_df = dfs[sid]["annual (calendar)"]
            ann_srn_df = dfs[sid]["annual provenance"]
            ann_financial_df = dfs[sid]["annual (water-use year)"]
            daily_df = dfs[sid]["daily"]
            mp_df = daily_df[
                (daily_df["Date"] >= dfn.mean_period_start)
                & (daily_df["Date"] <= dfn.mean_period_finish)
            ]
            means = mp_df.groupby("wu_year").Rain.sum().describe()
            p_df = daily_df[
                (daily_df["Date"] >= dfn.rf_period_start)
                & (daily_df["Date"] <= dfn.rf_period_finish)
            ]
            rf_period_years = p_df.Date.dt.year.unique()
            if len(rf_period_years) == 1:
                year_type = "calendar"
            else:
                year_type = "split"
            logger.info(f"Selecting year_type = '{year_type}'")

            # for rf in report.rainfall_files():
            #     sid = rf["sid"]
            #     name = rf["name"]
            #     logger.info(f"{sid} {name}")
            #     rdfn = report.rainfall_dfn(sid)

            # Excel does not understand datetimes <= 1900. You will need to include the commented-out line
            # in that case.
            #     df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')

            if not internal_only:
                # ----------------- SILO chart -------------------------
                logger.info(
                    f"Making chart :: ausweather.plot_silo_station :: for {sid} {name}"
                )
                pchart = ausweather.plot_silo_station(
                    ann_calendar_df.set_index("Date").Rain,
                    ann_calendar_df.Rain.mean(),
                    ann_srn_df.set_index("Date"),
                    title=f"{sid} {name}",
                )
                pchart_fn = report.rainfall_path / f"plot_station_{sid}_{name}.png"
                pchart["fig"].tight_layout()
                pchart["fig"].savefig(pchart_fn, dpi=150)

                # ---------------- Annual totals chart ----------------------
                # Mean period data

                # Annual water-use year chart
                # if year_type == "split":
                logger.info(
                    f"Making chart :: wrap_technote.plot_rainfall_wuy_annual :: for {sid} {name}"
                )
                filename = f"annual_rainfall_wuy_{sid}_{name}_{mp_df.iloc[0].wu_year}_{mp_df.iloc[-1].wu_year}.png"
                wuy_ann_chart = tn.plot_rainfall_wuy_annual(
                    mp_df, trend_line=True, wuy_col=False
                )
                wuy_ann_chart["ax"].figure.tight_layout()
                wuy_ann_chart["ax"].figure.savefig(
                    str(report.rainfall_path / filename), dpi=150
                )

                wuy_trend_line_df = pd.DataFrame(
                    [
                        {
                            "start": dfn.mean_period_start,
                            "finish": dfn.mean_period_finish,
                            "slope (mm/y)": wuy_ann_chart["slope"],
                            "intercept": wuy_ann_chart["intercept"],
                        }
                    ]
                )

                # if year_type == "calendar":
                # Annual calendar year chart
                logger.info(
                    f"Making chart :: wrap_technote.plot_rainfall_calendar_annual :: for {sid} {name}"
                )
                filename = f"annual_rainfall_calendar_{sid}_{name}_{mp_df.iloc[0].Date.year}_{mp_df.iloc[-1].Date.year}.png"
                calendar_ann_chart = tn.plot_rainfall_calendar_annual(
                    mp_df, trend_line=True, year_col=False
                )
                calendar_ann_chart["ax"].figure.tight_layout()
                calendar_ann_chart["ax"].figure.savefig(
                    str(report.rainfall_path / filename), dpi=150
                )

                calendar_trend_line_df = pd.DataFrame(
                    [
                        {
                            "start": dfn.mean_period_start,
                            "finish": dfn.mean_period_finish,
                            "slope (mm/y)": calendar_ann_chart["slope"],
                            "intercept": calendar_ann_chart["intercept"],
                        }
                    ]
                )

                # -------------------- Monthly totals (and means) chart -----------------------

                # Monthly means (mean_monthly) and monthly totals for last 18 months (period_monthly).
                if year_type == "split":
                    mlabel = (
                        tn.date_to_wateruseyear(dfn.mean_period_start)
                        + " to "
                        + tn.date_to_wateruseyear(dfn.mean_period_finish)
                    )
                    mp_label = f"{mp_df.iloc[0].wu_year}_{mp_df.iloc[-1].wu_year}"
                    plabel = f"{dfn.rf_period_start.year}-{str(dfn.rf_period_finish.year)[-2:]}"
                elif year_type == "calendar":
                    mlabel = (
                        f"{dfn.mean_period_start.year} to {dfn.mean_period_finish.year}"
                    )
                    mp_label = mlabel.replace(" to ", "_")
                    plabel = str(dfn.rf_period_start.year)

                xl_left = str(dfn.rf_period_start.year)
                xl_right = str(dfn.rf_period_finish.year)

                mean_monthly = mp_df.groupby(
                    [mp_df.Date.dt.year, mp_df.Date.dt.month]
                ).Rain.sum()
                mean_monthly = (
                    mean_monthly.reset_index(level=0, drop=True)
                    .reset_index()
                    .groupby("Date")
                    .mean()
                    .Rain
                )
                # mean_monthly = (
                #     mp_df.groupby([mp_df.Date.dt.year, mp_df.Date.dt.month])
                #     .Rain.sum()
                #     .mean(level=1)
                # )
                period_monthly = p_df.groupby(
                    [daily_df.Date.dt.year, daily_df.Date.dt.month]
                ).Rain.sum()

                # Monthly chart
                logger.info(
                    f"Making chart :: wrap_technote.plot_rainfall_monthly_means :: for {sid} {name} year_type={year_type}"
                )
                ax = tn.plot_rainfall_monthly_means(
                    mean_monthly,
                    period_monthly,
                    mlabel,
                    plabel,
                    xl_left,
                    xl_right,
                    year_type=year_type,
                )
                monthly_filename = (
                    f"monthly_rainfall_{sid}_{name}_"
                    + mp_label
                    + f"_period_{plabel}.png"
                )
                ax.figure.tight_layout()
                ax.figure.savefig(str(report.rainfall_path / monthly_filename), dpi=150)

            plt.style.use("default")
            # --------- Internal analysis -------
            internal_path = report.rainfall_path / "analysis_figures"
            internal_path.mkdir(parents=True, exist_ok=True)

            ax = tn.plot_annual_rainfall_internal(
                station,
                report,
                df=ann_calendar_df,
                chart_start=1990,
                sheet_name="calendar",
            )
            fn = f"annual_rainfall_internal_calendar_{sid}_{name}.png"
            ax.figure.tight_layout()
            ax.figure.savefig(report.rainfall_path / "analysis_figures" / fn, dpi=100)

            ax = tn.plot_annual_rainfall_internal(
                station,
                report,
                df=ann_financial_df,
                chart_start=1990,
                sheet_name="financial",
            )
            fn = f"annual_rainfall_internal_financial_{sid}_{name}.png"
            ax.figure.tight_layout()
            ax.figure.savefig(report.rainfall_path / "analysis_figures" / fn, dpi=100)

            current_year = dfn.rf_period_finish.year
            for chart_year in [current_year - i for i in range(4)]:
                chart_year = str(chart_year)
                ax = tn.plot_monthly_rainfall_internal(
                    station,
                    report,
                    show_year=chart_year,
                    dailydf=daily_df,
                )
                fn = f"monthly_rainfall_internal_{chart_year}_{sid}_{name}.png"
                ax.figure.tight_layout()
                ax.figure.savefig(
                    report.rainfall_path / "analysis_figures" / fn, dpi=100
                )

            ax = tn.plot_seasonal_rainfall_residuals_internal(
                station, report, daily_df=daily_df, chart_start=1990, value_type="mm"
            )
            fn = f"seasonal_rainfall_residuals_internal_mm_{sid}_{name}.png"
            ax.figure.tight_layout()
            ax.figure.savefig(report.rainfall_path / "analysis_figures" / fn, dpi=100)

            ax = tn.plot_seasonal_rainfall_residuals_internal(
                station, report, daily_df=daily_df, chart_start=1990, value_type="%"
            )
            fn = f"seasonal_rainfall_residuals_internal_pct_{sid}_{name}.png"
            ax.figure.tight_layout()
            ax.figure.savefig(report.rainfall_path / "analysis_figures" / fn, dpi=100)

            ax = tn.plot_seasonal_rainfall_totals_internal(
                station, report, daily_df=daily_df, chart_start=1990
            )
            fn = f"seasonal_rainfall_totals_internal_{sid}_{name}.png"
            ax.figure.tight_layout()
            ax.figure.savefig(report.rainfall_path / "analysis_figures" / fn, dpi=100)

            # ------------------------ Write data to spreadsheet -----------------------------

            if not internal_only:
                with pd.ExcelWriter(
                    str(
                        report.rainfall_path
                        / f"report_rainfall_{report.report_key}_{sid}_{name}_{mp_label}.xlsx"
                    )
                ) as writer:
                    wuy_ann_chart["rf_wuy"].to_excel(
                        writer, "water-use year", index=True
                    )
                    calendar_ann_chart["rf_year"].to_excel(
                        writer, "calendar", index=True
                    )
                    means.to_excel(writer, "means", index=True)
                    wuy_trend_line_df.to_excel(
                        writer, "trend line (water-use years)", index=True
                    )
                    calendar_trend_line_df.to_excel(
                        writer, "trend line (calendar years)", index=True
                    )
                    if year_type == "split":
                        wuy_trend_line_df.to_excel(writer, "trend line", index=True)
                    elif year_type == "calendar":
                        calendar_trend_line_df.to_excel(
                            writer, "trend line", index=True
                        )
                    if len(mean_monthly):
                        mean_monthly.to_excel(writer, f"monthly means", index=True)
                    if len(period_monthly):
                        period_monthly.to_excel(
                            writer, f"{plabel} monthly totals", index=True
                        )

    if static:
        create_static_rainfall_page(report)


def create_static_rainfall_page(report):
    templates = tn.load_html_templates()
    template = templates.get_template("static/rainfall.html")

    with open(str(report.rainfall_path / "rainfall.html"), mode="w") as html:
        data = report.calculated_rainfall_files()
        station_data = {k: v for k, v in data.items() if not k == "pivoted"}
        html.write(
            template.render(
                {"report": report, "data": station_data, "wide_data": data["pivoted"]}
            )
        )
