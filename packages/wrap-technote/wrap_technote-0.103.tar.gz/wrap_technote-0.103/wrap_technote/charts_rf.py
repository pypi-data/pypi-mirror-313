import colorsys
from datetime import date, datetime, timedelta
import io
import re
import os
import logging
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import lines as mlines
from matplotlib import gridspec
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib import colors as mcolors
import numpy as np
import pandas as pd
from adjustText import adjust_text
from scipy import stats
from PIL import Image, ImageChops
import pyproj

from .gwutils import *
from .utils import *
from .rainfall import *
from .charts_utils import *

logger = get_logger()


def plot_rainfall_wuy_annual(
    rf, ax=None, trend_line=False, rf_col="Rain", dt_col="Date", wuy_col=False
):
    """Plot annual rainfall.

    Args:
        rf (pandas DataFrame): daily rainfall data
        trend_line (bool): calculate and plot a trend line
        rf_col (str): column containing rainfall in mm
        dt_col (str): column containing datetimes
        wuy_col (str or False): column containing the water-use year. If it is
            False then the column will be calculated and added as "wu_year"

    Note, water-use year is the same as financial year.

    Returns:
        dict with keys "ax", "rf_wuy" (a pandas Series), "slope" (mm/y) and
        "intercept".

    """

    width = 0.8
    if ax is None:
        fig = plt.figure(figsize=(7.2, 3.4))
        ax = fig.add_subplot(111)

    if not wuy_col in rf:
        rf.loc[:, "wu_year"] = [date_to_wateruseyear(d) for d in rf[dt_col]]
    rf_wuy = rf.groupby("wu_year")[rf_col].sum()
    rf_wuy_x = np.arange(len(rf_wuy))
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        rf_wuy_x, rf_wuy.values
    )

    ax.bar(
        rf_wuy_x,
        rf_wuy.values,
        width=width,
        facecolor=rainfall_colours["rainfall"],
        label="Annual rainfall",
    )

    trend_x = np.asarray([rf_wuy_x[0], rf_wuy_x[-1]])
    trend_y = [slope * tx + intercept for tx in trend_x]
    if trend_line:
        ax.plot(trend_x, trend_y, color="darkblue", label="Trend in rainfall")

    ax.plot(
        [rf_wuy_x[0] - width / 2, rf_wuy_x[-1] + width / 2],
        [rf_wuy.mean(), rf_wuy.mean()],
        color=rainfall_colours["mean"],
        ls="--",
        lw=1,
        label=f"Mean annual rainfall ({rf_wuy.mean():.0f} mm)",
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ticks_per_label = 2
    xticks = np.arange(0, len(rf_wuy_x), ticks_per_label)
    while xticks[-1] != rf_wuy_x[-1]:
        xticks += 1
    ax.set_xticks(xticks)

    _ = ax.set_xticklabels(
        rf_wuy.index[xticks], rotation=90, ha="center", fontsize="medium"
    )
    y0, y1 = ax.get_ylim()
    y1_new = y1 + (y1 - y0) / 5
    ax.set_ylim(y0, y1_new)
    ax.set_ylabel("Annual rainfall (mm)", fontsize="medium")
    ax.legend(loc="best", fontsize="small", frameon=False, ncol=2)

    chart = {"ax": ax, "rf_wuy": rf_wuy, "slope": slope, "intercept": intercept}
    return chart


def plot_rainfall_calendar_annual(
    rf, ax=None, trend_line=False, rf_col="Rain", dt_col="Date", year_col=False
):
    """Plot annual rainfall.

    Args:
        rf (pandas DataFrame): daily rainfall data
        trend_line (bool): calculate and plot a trend line
        rf_col (str): column containing rainfall in mm
        dt_col (str): column containing datetimes
        year_col (str or False): column containing the year as an
            integer. If it is
            False then the column will be calculated and added as "year"

    Returns:
        dict with keys "ax", "rf_year" (a pandas Series), "slope" (mm/y) and
        "intercept".

    """

    width = 0.8
    if ax is None:
        fig = plt.figure(figsize=(7.2, 3.4))
        ax = fig.add_subplot(111)

    if not year_col in rf:
        rf.loc[:, "year"] = rf[dt_col].dt.year
    rf_year = rf.groupby("year")[rf_col].sum()
    rf_year_x = np.arange(len(rf_year))
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        rf_year_x, rf_year.values
    )

    ax.bar(
        rf_year_x,
        rf_year.values,
        width=width,
        facecolor=rainfall_colours["rainfall"],
        label="Annual rainfall",
    )

    trend_x = np.asarray([rf_year_x[0], rf_year_x[-1]])
    trend_y = [slope * tx + intercept for tx in trend_x]
    if trend_line:
        ax.plot(trend_x, trend_y, color="darkblue", label="Trend in rainfall")

    ax.plot(
        [rf_year_x[0] - width / 2, rf_year_x[-1] + width / 2],
        [rf_year.mean(), rf_year.mean()],
        color=rainfall_colours["mean"],
        ls="--",
        lw=1,
        label=f"Mean annual rainfall ({rf_year.mean():.0f} mm)",
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ticks_per_label = 2
    xticks = np.arange(0, len(rf_year_x), ticks_per_label)
    while xticks[-1] != rf_year_x[-1]:
        xticks += 1
    ax.set_xticks(xticks)

    _ = ax.set_xticklabels(
        rf_year.index[xticks], rotation=90, ha="center", fontsize="medium"
    )
    y0, y1 = ax.get_ylim()
    y1_new = y1 + (y1 - y0) / 5
    ax.set_ylim(y0, y1_new)
    ax.set_ylabel("Annual rainfall (mm)", fontsize="medium")
    ax.legend(loc="best", fontsize="small", frameon=False, ncol=2)

    chart = {"ax": ax, "rf_year": rf_year, "slope": slope, "intercept": intercept}
    return chart


def plot_rainfall_monthly_means(
    mm,
    pm,
    mlabel,
    plabel,
    xlabel_left,
    xlabel_right,
    ax=None,
    xtl_kws=None,
    year_type="split",
    yl_fontsize="medium",
    leg_fontsize="small",
    xl2_fontsize="medium",
    bar_width=0.38,
    y_bump=0.1,
    ly=0.02,
):
    """Plot monthly totals vs monthly means.

    Args:
        mm (pandas Series): index is month number, value is
            monthly mean rainfall for that month
        pm (pandas Series): multilevel index: year, month number: the
            values are the monthly totals for that month.
        mlabel (str): label for the mean period e.g. "1977-78 to 2018-19"
        plabel (str): label for period e.g. "2018-19"
        year_type (str): either "split" (water use year) or "calendar"
        # # xlabel_left (str): label for left side of x-axis e.g. "2018"
        # # xlabel_right (str): label for right side of x-axis e.g. "2019"
        # xtl_fontsize (str): xticklabel fontsize
        y_bump (float): figure fraction to shift x-axis up by

    Returns: ax

    """

    width = bar_width
    month_numbers = pm.index.get_level_values(1)
    month_names = [date(2000, mn, 1).strftime("%b") for mn in month_numbers]
    rf_period_mm = [mm.loc[mn] for mn in month_numbers]
    rf_period_m = [x for x in pm]

    if ax is None:
        fig = plt.figure(figsize=(7.2, 3.0))
        ax = fig.add_subplot(111)
    rf_period_x = np.arange(len(month_numbers)) - width / 2
    rf_period_mm_x = np.arange(len(month_numbers)) + width / 2
    ax.bar(
        rf_period_x,
        rf_period_m,
        width=width,
        facecolor=rainfall_colours["rainfall"],
        label=f"{plabel} rainfall",
    )
    ax.bar(
        rf_period_mm_x,
        rf_period_mm,
        width=width,
        facecolor=rainfall_colours["mean"],
        label=f"Mean rainfall\n({mlabel})",
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks(range(len(month_numbers)))
    if xtl_kws is None:
        xtl_kws = dict(rotation=0, ha="center", fontsize="medium")
    _ = ax.set_xticklabels(month_names, **xtl_kws)
    ax.set_ylabel("Monthly rainfall (mm)", fontsize=yl_fontsize)
    ax.legend(loc="upper right", fontsize=leg_fontsize, frameon=False, ncol=2)
    y0, y1 = ax.get_ylim()
    y1_new = y1 + (y1 - y0) / 6
    ax.set_ylim(y0, y1_new)
    if year_type == "split":
        pos = ax.get_position()
        ax.set_position([pos.x0, pos.y0 + y_bump, pos.width, pos.height - y_bump])

        # ly = 0.02
        l1_x = (pos.x0, pos.x0 + 0.31)
        l2_x = [pos.x0 + 0.34, pos.x0 + pos.width + 0.04]
        ax.text(
            l1_x[0] + (l1_x[1] - l1_x[0]) / 2,
            ly,
            xlabel_left,
            transform=ax.figure.transFigure,
            fontsize=xl2_fontsize,
            va="center",
            ha="center",
            bbox=dict(facecolor="white", edgecolor="none"),
        )
        ax.text(
            l2_x[0] + (l2_x[1] - l2_x[0]) / 2,
            ly,
            xlabel_right,
            transform=ax.figure.transFigure,
            fontsize=xl2_fontsize,
            va="center",
            ha="center",
            bbox=dict(facecolor="white", edgecolor="none"),
        )

        line1 = mlines.Line2D(
            l1_x, [ly, ly], color="k", lw=0.5, transform=ax.figure.transFigure
        )
        line2 = mlines.Line2D(
            l2_x, [ly, ly], color="k", lw=0.5, transform=ax.figure.transFigure
        )
        for line in (line1, line2):
            line.set_clip_on(False)
            ax.add_line(line)
    return ax


def plot_monthly_rainfall_internal(
    station,
    report,
    show_year=None,
    dailydf=None,
    chart_start=2000,
    stat_start=None,
    stat_end=None,
):
    """Plot monthly average rainfall against a given year (either calendar or
    financial) and show the amount of change in labels on the chart.

    Args:
        station (dict): station to analyse. Must have keys "dfn" (pd.Series),
            and "station" (str). See :meth:`wrap_technote.Report.find_rainfall_station`.
        report (:class:`wrap_technote.Report`): report definition
            which defines the mean rainfall period and access to data.
        show_year (str or None): the year which should be shown in comparison to the
            mean period. By default this will be the most recent year in the data,
            so if you run the code in Jan or Feb it may be mostly blank ;-)
            If you specify a calendar year e.g. "2020" then the chart will
            extend from January on the left to December on the right.
            If you specify a financial year e.g. "2019-20" then the chart will
            extend from July on the left to June on the right.
        dailydf (pd.DataFrame): the data to plot. If not specified, daily
            data for *station* will be retrieved via *report*.
        chart_start (str/int): start year for the chart display only, can be
            either e.g. "2000" or 2000, or financial year e.g. "1998-99".
        stat_start, stat_end (str/int): as for *chart_start*, defines the
            mean period. If not supplied, it will be taken from
            :meth:`wrap_technote.Report.rainfall_dfn`.

    Example code::

        >>> import wrap_technote as tn
        >>> report = tn.load_report("Eyre Pen", "2020-21")
        >>> station = report.find_rainfall_station(id='18069')
        >>> tn.plot_monthly_rainfall_internal(station, report, show_year="2020")

    .. figure:: figures/monthly_rainfall_internal_2020_18069_ELLISTON.png

    You may need a higher DPI to see the smaller labels (`plt.rcParams['figure.dpi'] = 100`).

    Returns: matplotlib Axes object.

    """

    ddf = dailydf
    if stat_start is None:
        stat_start = station["dfn"].mean_period_start
    if stat_end is None:
        stat_end = station["dfn"].mean_period_finish - pd.Timedelta(days=365)

    if ddf is None:
        ddf = report.get_rainfall_data(station, "daily")

    ddf["year"] = ddf["Date"].dt.year

    if show_year is None:
        show_year = str(ddf.year.max())

    if "-" in show_year:
        year_col = "wu_year"
        dt_col = "wu_year"
    else:
        year_col = "year"
        dt_col = "year"

    monthly = reduce_daily_to_monthly(ddf, year_col=year_col)

    stat_start = stat_start.year
    stat_end = stat_end.year
    title = f"{report.report_key} - monthly - mean from {stat_start} - {station['station']} ({station['dfn'].station_name})"

    chart_idx = lambda x: x[dt_col].astype(str).str[:4].astype(int) >= chart_start
    stat_idx = lambda x: (x[dt_col].astype(str).str[:4].astype(int) >= stat_start) & (
        x[dt_col].astype(str).str[:4].astype(int) < (stat_end + 1)
    )
    stat_0 = sorted(ddf.loc[stat_idx, dt_col].values)[0]
    stat_1 = sorted(ddf.loc[stat_idx, dt_col].values)[-1]

    select_idx = lambda x: (x[year_col].astype(str) == show_year)

    stat_months = monthly[stat_idx].groupby("month").mean()
    select_months = monthly[select_idx].groupby("month").mean()
    # print(stat_months)

    fig = plt.figure(figsize=(8.8, 4.5))
    ax = fig.add_subplot(111)
    if dt_col == "wu_year":
        leg_loc = "upper center"
        ax_idx = np.array([7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6])
        year_for_month = (
            lambda m: int(show_year[:4]) if m >= 7 else int(show_year[:4]) + 1
        )
    elif dt_col == "year":
        leg_loc = "upper left"
        ax_idx = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        year_for_month = lambda m: int(show_year)

    ax_months = [
        pd.Timestamp(year=year_for_month(m), month=m, day=1).strftime("%b\n%Y")
        for m in ax_idx
    ]
    # fill any missing data
    select_months = select_months.reindex(index=ax_idx)

    x_idx = np.arange(0, len(ax_idx))
    width = 0.42
    ax.bar(
        x_idx - width / 2,
        select_months.loc[ax_idx]["Rain"],
        width=width,
        fc="tab:blue",
        label=f"{show_year}",
        alpha=0.5,
    )
    ax.bar(
        x_idx + width / 2,
        stat_months.loc[ax_idx]["Rain"],
        width=width,
        fc="tab:green",
        label=f"Mean {stat_0} to {stat_1}",
        alpha=0.5,
    )
    ax.plot(
        x_idx - width / 6,
        select_months.loc[ax_idx]["Rain"],
        marker="o",
        c="tab:blue",
        label="",
    )
    ax.plot(
        x_idx + width / 6,
        stat_months.loc[ax_idx]["Rain"],
        marker="o",
        ls=":",
        c="tab:green",
        label="",
    )
    ax.axhline(0, color="k", lw=0.5)
    _ = ax.set_xticks(x_idx)
    ax.set_xticklabels(ax_months)

    ax.legend(loc="best", frameon=False, fontsize="small")
    y1 = ax.get_ylim()[1]
    yspan = y1 - ax.get_ylim()[0]
    box_space_height = yspan / 7
    box_step = box_space_height / 5
    box_height = box_space_height - box_step
    y0 = 0 - box_space_height

    for m_idx, m in enumerate(ax_idx):
        sel = select_months.loc[m].Rain
        stat = stat_months.loc[m].Rain
        diff = sel - stat
        diff_pct = diff / stat * 100
        cmp_pct = sel / stat * 100
        if diff > 0:
            box_y = 0
        else:
            box_y = 0 - box_step
        label = (
            f"{sel:.0f} ({stat:.0f})\n{diff:+.0f} ({diff_pct:+.0f}%)\n({cmp_pct:.0f}%)"
        )
        ax.text(
            m_idx,
            box_y - (box_height / 10),
            label,
            va="top",
            ha="center",
            fontsize="xx-small",
            bbox=dict(boxstyle="square", fc="white", ec="none", alpha=0.8),
        )
    ax.set_ylim(y0, y1)
    ax.set_ylabel("Monthly rainfall (mm)")
    ax.set_title(title)
    return ax


def plot_annual_rainfall_internal(
    station,
    report,
    df=None,
    chart_start=2000,
    stat_start=None,
    stat_end=None,
    sheet_name="annual (water-use year)",
    annotations=True,
    ax=None,
    fig=None,
    report_key="",
    fig_width=None,
):
    """Plot chart for internal analysis of annual rainfall.

    Args:
        station (dict): from :meth:`wrap_technote.Report.get_rainfall_station`.
            must have key "dfn" containing pd.Series with index values
            "mean_period_start" and "mean_period_finish"
        chart_start (int): year in which the chart begins
        stat_start (pd.Timestamp): date from which the mean begins (will be taken from
            *station* if None)
        stat_end (pd.Timestamp): date on which the mean ends (will be taken from
            *station* if None)
        sheet_name (str): method of defining a year, must be either 'financial' or 'calendar'
        annotations (bool): draw the labels
        report_key (str): "" - used only in the title
        ax (matplotlib Axes)
        fig (matplotlib Figure)

    """

    if "water" in sheet_name.lower() and "use" in sheet_name.lower():
        sheet_name = "annual (water-use year)"
    elif "fin" in sheet_name.lower():
        sheet_name = "annual (water-use year)"
    elif "calendar" in sheet_name.lower():
        sheet_name = "annual (calendar)"
    else:
        raise KeyError(
            f"sheet_name {sheet_name} must be either 'financial' or 'calendar'"
        )

    if df is None:
        logger.debug(f"Loading data for {station['name']}")
        df = report.get_rainfall_data(station, sheet_name)

    if sheet_name == "annual (water-use year)":
        dt_col = "wu_year"
        df = df[(df[dt_col].str[:4].astype(int) + 1) <= datetime.today().year]
    elif sheet_name == "annual (calendar)":
        dt_col = "Date"
        df = df[df[dt_col] < datetime.today().year]

    if stat_start is None:
        stat_start = station["dfn"].mean_period_start
    if stat_end is None:
        stat_end = station["dfn"].mean_period_finish

    stat_start = stat_start.year
    if sheet_name == "annual (water-use year)":
        stat_end = (stat_end - pd.Timedelta(days=365)).year
    else:
        stat_end = stat_end.year

    logger.debug(f"stat_start = {stat_start} and stat_end = {stat_end}")

    # title = f"{report.report_key} - {sheet_name} - mean from {stat_start} - {station['station']} ({station['dfn'].station_name})"
    title = f"{station['id']} {station['name']}"

    chart_idx = lambda x: x[dt_col].astype(str).str[:4].astype(int) >= chart_start
    wu_years = list(df[chart_idx][dt_col].unique())

    if fig_width is None:
        fig_width = len(wu_years) * 0.4 + 0.8

    chart_idx = lambda x: x[dt_col].astype(str).str[:4].astype(int) >= chart_start
    stat_idx = lambda x: (x[dt_col].astype(str).str[:4].astype(int) >= stat_start) & (
        x[dt_col].astype(str).str[:4].astype(int) < (stat_end + 1)
    )
    stat_0 = sorted(df.loc[stat_idx, dt_col].values)[0]
    stat_1 = sorted(df.loc[stat_idx, dt_col].values)[-1]
    mean = df[stat_idx].Rain.mean()
    df["rain_change"] = df.Rain.diff()
    df["rain_pct_change"] = df.Rain.pct_change() * 100
    df["mean_change"] = df.Rain - mean
    df["mean_pct_change"] = df.mean_change / mean * 100
    df2 = df[chart_idx]
    df2 = df2.set_index(dt_col).reindex(wu_years).reset_index()
    if fig is None:
        fig = plt.figure(figsize=(fig_width, 5))
    if ax is None:
        ax = fig.add_subplot(111)
    ax.bar(df2.index, df2.Rain)
    ax.set_xticks(df2.index)
    ax.set_xticklabels(df2[dt_col])
    plt.setp(ax.get_xticklabels(), rotation=50, ha="right")
    ax.axhline(mean, color="brown", lw=1)
    mean_labelled = False
    for ix, row in df2.iterrows():
        if row.rain_change > 0:
            boxy = 30
        else:
            boxy = 5
        ax.text(
            ix,
            #             row.Rain + row.Rain / 22,
            boxy,
            (
                f"{row.Rain:.0f}\n"
                + f"{row.rain_change:+.0f}\n"
                + f"{row.rain_pct_change:+.0f}%"
            ),
            va="bottom",
            ha="center",
            fontsize="xx-small",
            bbox=dict(boxstyle="square", fc="white", ec="none", alpha=0.8),
        )

        # Position of top or bottom of the comparison to the mean.
        y = row.Rain + (row.Rain / 20 * (1 if row.mean_change > 0 else -1))
        ax.annotate(
            "",
            (ix, y),
            (ix, mean),
            arrowprops=dict(arrowstyle="-|>", color="brown", lw=0.5),
        )
        # Comparison to the mean - text label.
        ax.text(
            ix,
            y,
            (f"{row.mean_change:+.0f}\n" + f"{row.mean_pct_change:+.0f}%"),
            va=("bottom" if row.mean_change > 0 else "top"),
            ha="center",
            fontsize="xx-small",
            color="brown",
            bbox=dict(boxstyle="square", fc="white", ec="none", alpha=0.8),
        )

    ax.set_title(title + f"\nmean {stat_0} to {stat_1}")
    ax.set_ylim(None, ax.get_ylim()[1] + df2.Rain.max() / 10)
    ax.set_xlim(df2.index[0] - 1.5, None)
    ax.text(
        df2.index[0] - 1.3,
        mean,
        f"{mean:.0f}:",
        ha="left",
        va="center",
        style="italic",
        fontsize="x-small",
        color="brown",
        bbox=dict(boxstyle="square", fc="white", alpha=0.8, ec="none"),
    )
    ax.text(
        1,
        1,
        f"Data ends {df[dt_col].max()}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize="x-small",
    )
    return ax


def plot_seasonal_rainfall_residuals_internal(
    station,
    report,
    daily_df=None,
    chart_start=2000,
    chart_end=None,
    mean_start=None,
    mean_end=None,
    value_type="%",
    fig_width=None,
):
    if daily_df is None:
        ddf = report.get_rainfall_data(station, "daily")
    else:
        ddf = daily_df

    ddf["year"] = ddf.Date.dt.year
    monthly = reduce_daily_to_monthly(ddf, year_col="year")

    if chart_end is None:
        # chart_end = (station["dfn"].rf_period_finish - pd.Timedelta(days=365)).year
        chart_end = station["dfn"].rf_period_finish.year
    if mean_start is None:
        mean_start = station["dfn"].mean_period_start.year
    if mean_end is None:
        # mean_end = (station["dfn"].mean_period_finish - pd.Timedelta(days=365)).year
        mean_end = station["dfn"].rf_period_finish.year

    value_type_title = "pct" if value_type == "%" else value_type

    # title = f"{report.report_key} - seasonal difference {value_type_title} - mean from {mean_start} - {station['station']} ({station['dfn'].station_name})"
    title = f"{station['id']} {station['name']}"

    monthly["season"] = monthly.month.map(months_to_seasons)
    monthly.loc[monthly.season == "summer", "season"] = "0-summer"
    monthly.loc[monthly.season == "autumn", "season"] = "1-autumn"
    monthly.loc[monthly.season == "winter", "season"] = "2-winter"
    monthly.loc[monthly.season == "spring", "season"] = "3-spring"
    monthly["year-season"] = monthly["year"].astype(str) + "-" + monthly["season"]
    monthly = monthly.sort_values(["year", "month"])
    seasons = (
        monthly.groupby(["year-season", "year", "season"]).Rain.sum().reset_index()
    )

    smeans = (
        seasons[(seasons.year >= mean_start) & (seasons.year <= mean_end)]
        .groupby("season")
        .Rain.mean()
    )
    rows = []
    index = []
    for year, s in seasons.groupby("year"):
        year_totals = s.set_index("season").Rain
        year_diffs = year_totals - smeans
        index.append(year)
        rows.append(year_diffs)
    sdiffs = pd.DataFrame(rows, index=index)
    if value_type == "%":
        for col in sdiffs.columns:
            sdiffs[col] = sdiffs[col] / smeans.loc[col] * 100

    annrf = seasons.groupby("year").Rain.sum()
    annrf_mean = annrf[(annrf.index >= mean_start) & (annrf.index <= mean_end)].mean()
    annrf_dev = annrf - annrf_mean
    if value_type == "%":
        annrf_dev = annrf_dev / annrf_mean * 100

    if chart_end is None:
        chart_end = sdiffs.index.max()

    years = chart_end - chart_start + 1
    years_plot = np.array(
        [y for y in np.arange(chart_start, chart_end + 1, 1) if y in sdiffs.index]
    )
    sdiffs_plot = sdiffs[(sdiffs.index >= chart_start) & (sdiffs.index <= chart_end)]

    if fig_width is None:
        fig_width = 0.8 + len(years_plot) * 0.3
    fig = plt.figure(figsize=(fig_width, 5.5))
    ax = fig.add_subplot(111)
    season_names = ["0-summer", "1-autumn", "2-winter", "3-spring"]
    s_width = 0.25
    for i, season in enumerate(season_names):
        x_offset = i * s_width
        ax.bar(
            years_plot + x_offset + (s_width / 2) - (s_width / 3),
            sdiffs_plot[season],
            width=s_width,
            label=season[2:],
            facecolor=season_colours[season],
            edgecolor="k",
            lw=0.4,
        )
    ax.bar(
        years_plot + 0.5,
        annrf_dev.loc[years_plot],
        facecolor=(0, 0, 0, 0.1),
        width=1,
        lw=0.5,
        edgecolor=(0, 0, 0, 0.5),
        label="Annual",
    )
    ax.legend(loc="best", frameon=False, fontsize="small", ncol=4)
    ax.set_xticks(list(years_plot) + [years_plot[-1] + 1])
    plt.setp(ax.get_xticklabels(), rotation=90)
    ax.grid(True, color="gray", lw=0.2)
    y0, y1 = ax.get_ylim()
    dy = y1 - y0
    ax.set_ylim(y0, y1 + (dy / 12))
    ax.set_xlim(years_plot[0], years_plot[-1] + 1)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(10))
    ax.set_ylabel(f"Difference from mean rainfall ({value_type})")
    ax.set_xlabel("Year (tick mark is located on Jan 1)")
    ax.set_title(title)
    return ax


def plot_seasonal_rainfall_totals_internal(
    station, report, daily_df=None, chart_start=2000, chart_end=None, fig_width=None
):
    if daily_df is None:
        ddf = report.get_rainfall_data(station, "daily")
    else:
        ddf = daily_df

    ddf["year"] = ddf.Date.dt.year
    monthly = reduce_daily_to_monthly(ddf, year_col="year")

    if chart_end is None:
        # chart_end = (station["dfn"].rf_period_finish - pd.Timedelta(days=365)).year
        chart_end = station["dfn"].rf_period_finish.year

    # title = f"{report.report_key} - seasonal totals - {station['station']} ({station['dfn'].station_name})"
    title = f"{station['id']} {station['name']}"

    monthly["season"] = monthly.month.map(months_to_seasons)
    monthly.loc[monthly.season == "summer", "season"] = "0-summer"
    monthly.loc[monthly.season == "autumn", "season"] = "1-autumn"
    monthly.loc[monthly.season == "winter", "season"] = "2-winter"
    monthly.loc[monthly.season == "spring", "season"] = "3-spring"
    monthly["year-season"] = monthly["year"].astype(str) + "-" + monthly["season"]
    monthly = monthly.sort_values(["year", "month"])
    seasons = (
        monthly.groupby(["year-season", "year", "season"]).Rain.sum().reset_index()
    )
    ann = seasons.groupby("year").Rain.sum()

    chart_sel = lambda x: x["year"] >= chart_start
    chart_sel_y = lambda x: (x["year"] - 1) >= chart_start
    ann = seasons.groupby("year").Rain.sum().reset_index()
    adf = ann[chart_sel]
    sdf = seasons[chart_sel]
    summer_sel = lambda x: x.season == "0-summer"
    autumn_sel = lambda x: x.season == "1-autumn"
    winter_sel = lambda x: x.season == "2-winter"
    spring_sel = lambda x: x.season == "3-spring"

    if fig_width is None:
        fig_width = 1 + (adf.year.max() - adf.year.min()) * 0.3
    fig = plt.figure(figsize=(fig_width, 5))
    ax2 = fig.add_subplot(111)
    ax = ax2.twinx()
    # ax2.bar(sdf[winter_sel].index, adf.Rain, width=3.7, color='k', alpha=0.2)
    ax2.bar(
        sdf[winter_sel].index - 1 / 6,
        adf.Rain[adf.year.isin(sdf[sdf.season == "2-winter"].year.unique())],
        width=4,
        color="darkblue",
        lw=0.7,
        facecolor="none",
        edgecolor="k",
        label="Annual (calendar)",
    )
    ax.bar(
        sdf.index,
        sdf.Rain.mask(sdf.season != "0-summer", np.nan),
        width=1,
        color="sandybrown",
        label="Summer",
    )
    ax.bar(
        sdf.index,
        sdf.Rain.mask(sdf.season != "1-autumn", np.nan),
        width=1,
        color="khaki",
        label="Autumn",
    )
    ax.bar(
        sdf.index,
        sdf.Rain.mask(sdf.season != "2-winter", np.nan),
        width=1,
        color="deepskyblue",
        label="Winter",
    )
    ax.bar(
        sdf.index,
        sdf.Rain.mask(sdf.season != "3-spring", np.nan),
        width=1,
        color="yellowgreen",
        label="Spring",
    )
    # ax.plot(sdf[winter_sel].index, sdf[summer_sel].Rain, lw=0.7, ls='-', marker='.', color='darkgoldenrod')
    # ax.plot(sdf[winter_sel].index, sdf[autumn_sel].Rain, lw=0.7, ls='-', marker='.', color='olivedrab')
    # ax.plot(sdf[winter_sel].index, sdf[winter_sel].Rain, lw=0.7, ls='-', marker='.', color='blue')
    # ax.plot(sdf[winter_sel].index, sdf[spring_sel].Rain, lw=0.7, ls='-', marker='.', color='purple')
    ax2.legend(loc="upper right", frameon=False, fontsize="small", ncol=1)
    ax.legend(loc="upper left", frameon=False, fontsize="small", ncol=2)
    ax2_y0, ax2_y1 = ax2.get_ylim()
    ax2.set_ylim(ax2_y0, ax2_y1 * 1.1)
    ax_y0, ax_y1 = ax.get_ylim()
    ax.set_ylim(ax_y0, ax_y1 * 1.5)
    years = sdf.loc[sdf.season == "2-winter", "year"]
    xts = ax2.set_xticks(years.index)
    xtls = ax2.set_xticklabels(years)
    xtls = plt.setp(ax2.get_xticklabels(), rotation=90)
    ax2.set_ylabel("Seasonal rainfall (mm)")
    ax.set_ylabel("Annual rainfall (mm)")
    ax.set_xlim(sdf.index[0], sdf.index[-1])
    ax.set_title(title)
    ax.set_xlabel("Year - tick mark is on Jan 1")
    return ax


def plot_rainfall_daily_intensity(daily_df, years, threshold=10):
    daily_df["month"] = daily_df.Date.dt.month
    months, seasons = get_seasonal_rainfall_data(daily_df)
    seasonal_lut = months.set_index(["year", "month"])["season"]
    for year, month in daily_df[["year", "month"]].drop_duplicates().to_numpy():
        daily_df.loc[
            (daily_df.year == year) & (daily_df.month == month), "season"
        ] = seasonal_lut.loc[(year, month)]
    fig = plt.figure(figsize=(7.2, 3.4))
    ax = fig.add_subplot(111)
    days = daily_df[daily_df.year.isin(years)]
    days_low = days[days.Rain <= threshold]
    days_high = days[days.Rain > threshold]
    months = (
        daily_df[daily_df.year.isin(years)]
        .groupby(["year", "month"], as_index=False)
        .Rain.sum()
    )
    months["left_day"] = months.apply(
        (lambda r: pd.Timestamp(year=int(r.year), month=int(r.month), day=1)),
        axis="columns",
    )
    # ax.bar(months.left_day, months.Rain, width=29, align='edge', facecolor)
    ax.bar(
        days_low.Date,
        days_low.Rain,
        width=1,
        facecolor="gray",
        edgecolor="gray",
        linewidth=0.5,
        label="Daily rainfall",
    )
    ax.bar(
        days_high.Date,
        days_high.Rain,
        width=1,
        facecolor="blue",
        edgecolor="blue",
        linewidth=0.5,
        label=f"Days above {threshold} mm",
    )
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=np.arange(1, 13, 1)))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(5, 11), bymonthday=1))
    ax.xaxis.set_minor_formatter(mticker.NullFormatter())
    # ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    # major_xtls = plt.setp(ax.get_xticklabels())
    minor_xtls = plt.setp(ax.get_xticklabels(minor=True), fontsize="small", rotation=90)
    ax.set_xlim(
        pd.Timestamp(str(years[0])), pd.Timestamp(year=years[1], month=12, day=31)
    )
    ax.set_ylabel("Daily rainfall (mm)", fontsize="medium")
    leg = ax.legend(loc="upper left", fontsize="small", frameon=False, ncol=2)
    y0, y1 = ax.get_ylim()
    dy = y1 - y0
    ax.set_ylim(y0, y1 + dy / 3.5)
    for year in years:
        year_xloc = pd.Timestamp(year=year, month=7, day=1)
        count = len(
            days_high[
                (days_high.year == year)
                & (days_high.month >= 5)
                & (days_high.month <= 10)
            ]
        )
        if count == 0:
            label = "No days above 10 mm"
        elif count == 1:
            label = "1 day above 10 mm"
        else:
            label = f"{count:.0f} days above 10 mm"
        ax.text(
            year_xloc,
            y1,
            label + f"\nfrom May to Oct {year}",
            ha="center",
            va="bottom",
            color="darkblue",
            fontsize="small",
        )
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    return ax
