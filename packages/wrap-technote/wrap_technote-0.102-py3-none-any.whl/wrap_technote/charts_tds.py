import colorsys
from datetime import date, datetime, timedelta
import io
import re
import os
import logging
import textwrap
from pathlib import Path
import copy

import matplotlib.pyplot as plt
from matplotlib import lines as mlines
from matplotlib import gridspec
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib import colors as mcolors
from matplotlib import patches as mpatches
import numpy as np
import pandas as pd
from adjustText import adjust_text
from scipy import stats
from PIL import Image, ImageChops
import pyproj

from .gwutils import *
from .utils import *
from .charts_utils import *

logger = get_logger()


def plot_tds_data_validation(
    df,
    removals=None,
    show_comments=True,
    well_id_col="well_id",
    dt_col="collected_date",
    tds_col="tds",
    label_col="reason",
    mew=0.3,
    adjust_comments=False,
    adjust_text_lim=30,
    ignore_comment_regexps=(r"Hydat.*", r".*LIC ?= ?.*"),
    savefig_and_close=False,
    path=".",
    dpi=130,
    fig=None,
    **kws,
):
    """Plot a graph of salinity data for validation purposes.

    Args:
        df (pandas DataFrame): salinity data for one or more wells
        removals (pandas DataFrame): salinity data which has been deemed invalid
            but should be included on the plot (to see what has been removed and
            why), for one or more wells.
        show_comments (bool): show comments on the chart
        well_id_col (str): column label for a unique well identifier
        dt_col (str): column label for the observation date in datetimes
        tds_col (str): column label with salinity data
        label_col (str): column label for *removals* with the reason for the
            data points removal
        mew (float): width of line
        adjust_comments (bool): use the adjustText python library to attempt
            and move the comment labels so that they do not overlap. It is quite
            slow, so be aware of that.
        adjust_text_lim (int): number of iterations for adjustText to run. 2 or 3
            will be fast but likely ineffective for all but the simplest plots.
            100 will be quite slow but a thorough test on almost all plots. 30
            is a good compromise.
        ignore_comment_regexps (sequence of str): each string is a regexp pattern.
            If it matches the comment for a given data point, the comment will not
            be plotted on the chart (only relevant if show_comments is True).
        path (str): path to save figures into.
        savefig_and_close (bool): save fig to png and close
        dpi (int): resolution of saved PNGs if *savefig_and_close=True*.

    Any keyword arguments beginning with ``adjust_text`` will be sent to the
    :func:`adjustText.adjust_text` function, so for example to tell adjustText to
    use autoalign, pass *adjust_text_autoalign=True* to this function.

    Returns: a list of matplotlib Axes.

    """
    if removals is not None:
        all_removal_well_ids = list(removals[well_id_col].unique())
    else:
        all_removal_well_ids = []

    well_ids = sorted(list(set(list(df[well_id_col].unique()) + all_removal_well_ids)))

    df.loc[df.extract_method.isnull(), "extract_method"] = "?"
    df.loc[df.measured_during.isnull(), "measured_during"] = "?"

    comment_props = dict(marker="o", lw=0, mfc="none", mec="purple", mew=0.3, ms=12)

    def add_comments(cdf, cax):
        ctexts = []
        if len(cdf):
            cax.plot(cdf[dt_col], cdf[tds_col], **comment_props)
            for idx, row in cdf.iterrows():
                comment = str(row.comments)
                x = row[dt_col]
                y = row[tds_col]
                by = str(row.collected_by).strip()
                by = "" if by == "None" else by
                if by:
                    comment = f"{by}: {comment}"
                if comment and isinstance(x, datetime) and not np.isnan(y):
                    add_label = True
                    for fail_pattern in ignore_comment_regexps:
                        if re.match(fail_pattern, comment):
                            add_label = False
                    if add_label:
                        text = cax.text(x, y, wrap(comment), color="purple", fontsize=5)
                        ctexts.append(text)
        return ctexts

    axes = []
    if savefig_and_close:
        if not fig:
            fig = plt.figure(figsize=(10, 4))

    for i, well_id in enumerate(well_ids):
        logger.debug(f"Charting {well_id}")
        if savefig_and_close:
            ax = fig.add_subplot(111)
        else:
            fig = plt.figure(figsize=(7, 3))
            ax = fig.add_subplot(111)

        ax.set_title(well_id)

        w_df = df[df[well_id_col] == well_id]

        texts = []

        # Group the salinity data by extract_method and measured_during
        for extract_method, wdf2 in w_df.groupby("extract_method"):
            for mduring, wdf3 in wdf2.groupby("measured_during"):
                # Chart this group of salinity data with
                # the marker shape representing the extract_method; and
                # the fill colour representing the measured_during code
                ax.plot(
                    wdf3[dt_col],
                    wdf3[tds_col],
                    marker=extract_method_markers[extract_method],
                    mfc=meas_during_colours[mduring],
                    mec="black",
                    mew=mew,
                    lw=0,
                    label="",
                )
                if show_comments:
                    texts += add_comments(wdf3[~wdf3.comments.isnull()], ax)

        # Chart a line connecting all the salinity data points.
        (sal_line,) = ax.plot(
            w_df[dt_col],
            w_df[tds_col],
            ls="-",
            lw=0.5,
            color="tab:cyan",
            label="All retained data",
        )

        if removals is not None:
            w_removals = removals[removals[well_id_col] == well_id]
            removal_reasons = list(w_removals.reason.unique())

            # Chart the values which have been excluded (and the reason why).
            for j, (reason, rdf) in enumerate(w_removals.groupby("reason")):
                ax.plot(
                    rdf[dt_col],
                    rdf[tds_col],
                    marker="X",
                    color=removal_reason_colours[removal_reasons.index(reason)],
                    lw=0,
                    label=reason,
                )
            if show_comments:
                texts += add_comments(w_removals[~w_removals.comments.isnull()], ax)

        # Add a legend item for comments
        ax.plot([], [], label="SA Geodata comments", **comment_props)

        # Add a legend item for the differnt extract_method codes.
        for emeth in w_df.extract_method.unique():
            ax.plot(
                [],
                [],
                lw=0,
                marker=extract_method_markers[emeth],
                color="k",
                mew=mew,
                mfc="white",
                label=f"Extract by: {extract_method_lut[emeth]}",
            )

        # Add a legend item for the different measured_during codes.
        for mduring in w_df.measured_during.unique():
            ax.plot(
                [],
                [],
                lw=0,
                marker="8",
                mew=0,
                mfc=meas_during_colours[mduring],
                label=f"Meas. during {measured_during_lut[mduring]}",
            )

        # Show ignore_comment_patterns in the legend.
        if show_comments and ignore_comment_regexps:
            for fail_pattern in ignore_comment_regexps:
                plt.plot(
                    [],
                    [],
                    ls="",
                    label=f'(Comments matching regexp\n"{fail_pattern}" not shown)',
                )

        # Add the legend
        ax.legend(loc="best", fontsize="xx-small", frameon=False, ncol=2)

        # Rearrange the labels if requested
        if adjust_comments:
            logger.debug(
                f"Using adjust_text to shift comment annotations for {well_id}"
            )
            adjust_text_kws = {}
            adjust_text_kws["arrowprops"] = kws.get(
                "adjust_text_arrowprops", dict(arrowstyle="->", color="gray", lw=0.3)
            )
            adjust_text_kws["autoalign"] = kws.get("adjust_text_autoalign", False)
            adjust_text_kws["lim"] = adjust_text_lim
            for key, argval in kws.items():
                if key.startswith("adjust_text"):
                    adjust_text_kws[key.replace("adjust_text_", "")] = argval
            adjust_text(
                texts,
                x=mdates.date2num(sal_line.get_xdata()),
                y=sal_line.get_ydata(),
                **adjust_text_kws,
            )
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel(tds_col)
        ax.set_xlabel(dt_col)

        if savefig_and_close:
            fig.savefig(str(path / f"plot_tds_data_validation_{well_id}.png"), dpi=dpi)
            fig.clf()
        else:
            axes.append(ax)

    df.loc[df.extract_method == "?", "extract_method"] = None
    df.loc[df.measured_during == "?", "measured_during"] = None

    return axes


def plot_salinity_trend(
    sals,
    trend_sals,
    trend_lines=None,
    excluded_sals=None,
    well_id_col="well_id",
    dt_col="collected_date",
    sal_col="tds",
    hist_max_date_col="tds_max_date",
    ax=None,
    ms=5,
    year_span=12,
    override_year_span=False,
):
    well_id = sals[well_id_col].unique()[0]
    logger.debug(f"Charting {well_id}")
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    lw = 0.5
    ax.plot(
        sals[dt_col],
        sals[sal_col],
        color="#222222",
        lw=lw,
        marker="o",
        mfc="orange",
        mec="gray",
        ms=ms - 1,
        mew=0.3,
        alpha=0.5,
        label="All valid salinity data",
    )
    if excluded_sals is not None:
        ax.plot(
            excluded_sals[dt_col],
            excluded_sals[sal_col],
            lw=0,
            marker="o",
            ms=ms,
            mew=0.2,
            mec="grey",
            mfc="grey",
            color="grey",
            alpha=0.2,
            label="Excluded data",
        )
    ax.plot(
        trend_sals[dt_col],
        trend_sals[sal_col],
        marker="o",
        mfc="red",
        mec="k",
        ms=ms,
        mew=0.3,
        lw=0,
        alpha=0.7,
        label="Used for trend calculation",
    )
    hist_idx = sals[dt_col] == trend_sals[hist_max_date_col].iloc[0]
    ax.plot(
        sals[hist_idx][dt_col],
        sals[hist_idx][sal_col],
        marker="o",
        mec="purple",
        mfc="none",
        mew=0.5,
        ms=ms + 5,
        ls="none",
        label="Historical maximum",
    )

    if trend_lines is not None:
        start_year = min(trend_sals[dt_col]).year
        end_year = max(trend_sals[dt_col]).year
        trend_line = trend_lines.loc[well_id]
        trend_line_ts = [
            pd.Timestamp(f"{start_year}-01-01"),
            pd.Timestamp(f"{end_year}-12-31"),
        ]
        trend_line_vals = calculate_trendline_at_dates(trend_line, trend_line_ts)
        ax.plot(trend_line_ts, trend_line_vals, lw=1, color="r", label="Linear trend")
        end_ts = trend_line_ts[1]
        fg, bg = status_to_colours(trend_line.status_change, param="TDS")
        trend_label = (
            f"{well_id}: {trend_line.status_change}"
            f" at {trend_line.slope_yr:.0f} mg/L/y ({trend_line.sal_pct_change:.1f}%)"
        )
    else:
        end_ts = pd.Timestamp(trend_sals[dt_col].max())
        fg = "black"
        bg = "white"

    start_ts = end_ts - timedelta(days=365.25 * year_span)
    if "max" in str(override_year_span):
        hist_max_ts = sals[hist_idx][dt_col].iloc[0] - timedelta(days=120)
        if hist_max_ts < start_ts:
            start_ts = hist_max_ts
    elif override_year_span == "all":
        start_ts = sals[dt_col].min() - timedelta(days=120)

    ax.set_xlim(start_ts, end_ts + timedelta(days=120))
    leg = ax.legend(loc="best", fontsize="x-small", frameon=False)
    ax.set_ylabel(sal_col)
    title_text = ax.set_title(
        trend_label, color=fg, backgroundcolor=bg, fontsize="medium"
    )

    lim_sals = sals[(sals[dt_col] >= start_ts) & (sals[dt_col] <= end_ts)][sal_col]
    yspan = lim_sals.max() - lim_sals.min()
    y0 = lim_sals.min() - yspan * 0.1
    y1 = lim_sals.max() + yspan * 0.1
    ax.set_ylim(y0, y1)
    ax._title_text = title_text
    return ax


def plot_tds_trends_internal(tdstrends, title="", param="mg"):
    """param can be 'mg' or '5_yr_pct'"""
    if param == "mg":
        param_col = "slope_yr"
        yaxis_label = "mg/L/y"
    elif param == "5yr_pct":
        param_col = "sal_pct_change"
        yaxis_label = "% change over 5 yrs"
    assert param in ("mg", "5yr_pct")
    return plot_trends_internal(
        tdstrends,
        title=title,
        class_names=("Decreasing", "Stable", "Increasing"),
        param_yaxis_label=yaxis_label,
        param_col=param_col,
    )


def plot_tds_current_internal(df, title="", ax=None, fig=None):
    anntds = df.copy()
    anntds["tds_interval"] = pd.cut(anntds.tds, np.arange(0, 10000, 200))
    tdsbins = anntds.groupby("tds_interval").dh_no.count().to_frame().reset_index()
    tdsbins["left"] = [interval.left for interval in tdsbins.tds_interval]
    tdsbins["right"] = [interval.right for interval in tdsbins.tds_interval]
    tdsbins["centre"] = tdsbins.left + (tdsbins.right - tdsbins.left) / 2

    if fig is None:
        fig = plt.figure(figsize=(8, 3))
        ax = fig.add_subplot(111)

    highest_tds = 0
    label = "first"
    for ix, row in tdsbins.iterrows():
        if row.dh_no > 0:
            if label == "first":
                label = "Number of wells\n(200 mg/L bins)"
            else:
                label = ""
            ax.bar(
                [row.centre],
                [row.dh_no],
                color="tab:blue",
                alpha=1,
                width=150,
                label=label,
            )
            highest_tds = row.right
    median_tds = anntds.tds.median()
    mean_tds = anntds.tds.mean()
    ax.axvline(
        median_tds, lw=2, color="tab:red", label=f"median ({median_tds:.0f} mg/L)"
    )
    ax.axvline(
        mean_tds,
        lw=2,
        color="purple",
        dashes=(5, 1),
        label=f"mean ({mean_tds:.0f} mg/L)",
    )
    ax.legend(loc="best", fontsize="small", frameon=False)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(15))
    ax.set_xlim(0, highest_tds)
    ax.set_ylabel("Number of wells")
    ax.set_xlabel("Current salinity (mg/L)")
    ax.grid(True, lw=0.5, color="k", alpha=0.5, ls=":")
    ax.grid(True, axis="x", lw=0.5, color="k", alpha=0.5, ls=":")
    ax.set_title(title)
    return ax


def plot_tds_resource_monitoring_history(annstats, axes=None, fig=None):
    if axes is None:
        fig = plt.figure(figsize=(8, 6))
        gs = gridspec.GridSpec(2, 1, height_ratios=(4, 2), hspace=0)
        ax = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1], sharex=ax)
    else:
        ax, ax2 = axes

    lower = annstats.tds_mean - annstats.tds_stdev
    lower2 = (lower - annstats.tds_stdev).dropna()
    upper = annstats.tds_mean + annstats.tds_stdev
    upper2 = (upper + annstats.tds_stdev).dropna()

    logger.debug(f"lower2: {lower2}")
    logger.debug(f"upper2: {upper2}")

    if len(lower):
        ax.fill_between(
            annstats.index,
            lower,
            upper,
            color="tab:blue",
            alpha=0.8,
            lw=0,
            label="±1 s.d.",
        )
        if len(lower2):
            if len(lower) == len(lower2):
                ax.fill_between(
                    annstats.index,
                    lower2,
                    lower,
                    color="lightblue",
                    lw=0,
                    label="±2 s.d.",
                )
        if len(upper2):
            if len(upper) == len(upper2):
                ax.fill_between(
                    annstats.index, upper, upper2, color="lightblue", lw=0, label=""
                )

    ax.plot(annstats.index, annstats.tds_mean, color="darkblue", lw=1, label="Mean TDS")
    ax.plot(
        annstats.index, annstats.tds_median, color="darkgreen", lw=1, label="Median TDS"
    )
    ax2.bar(
        annstats.index,
        annstats.n_wells,
        color="gray",
        lw=1,
        alpha=1,
        label="Number of wells",
    )

    ax.set_ylabel("Salinity (mg/L)")
    ax2.set_ylabel("Number of wells")

    ax.yaxis.set_major_locator(mticker.MaxNLocator(10))
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(5))

    ax.legend(loc="center left", ncol=1, fontsize="small", frameon=True)
    ax2.legend(loc="upper left", ncol=4, fontsize="small", frameon=True)

    if len(annstats):
        ax2.set_ylim(0, annstats.n_wells.max())
        if len(lower2) and len(upper2):
            ax.set_ylim(max([lower2.min(), 0]), upper2.max())

    ax.grid(True, ls="--", lw=0.5)
    ax2.grid(True, ls="--", lw=0.5)

    ax.figure.tight_layout()
    return ax, ax2


def plot_tds_resource_variability(annstats, axes=None):
    if axes is None:
        fig = plt.figure(figsize=(9, 4))
        gs = gridspec.GridSpec(1, 2)
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        axes = (ax1, ax2)
    for i, key in enumerate(("n_wells", "year")):
        if key == "n_wells":
            s = annstats.n_wells
            cmap = plt.cm.magma_r
        elif key == "year":
            s = annstats.index
            cmap = plt.cm.viridis
        ax = axes[i]
        cset = ax.scatter(
            annstats.tds_mean,
            annstats.tds_stdev / annstats.tds_mean * 100,
            c=s,
            marker="o",
            s=80,
            linewidths=0.5,
            edgecolors="k",
            cmap=cmap,
        )
        cbar = plt.colorbar(cset, ax=ax)
        cbar.set_label(key)
        ax.set_ylabel("Standard deviation (% of mean)")
        ax.set_xlabel("Mean TDS (mg/L)")
    axes[0].figure.tight_layout()
    return axes


# def plot_salinity_status_and_trend(df, tdf, results, axes=None):
#     """Plot salinity status and trend results.

#     Args:
#         df (pd.DataFrame): containing data
#         tdf (pd.DataFrame): containing the trend line data
#         results (pd.Series): containing the results of the calculation.

#     The data for this figure comes from the function :func:`get_historical_salinity_trends`,
#     i.e. the last entry in the list of dataframes, and the last row of the
#     "results" dataframe.

#     """
#     if not axes:
#         fig = plt.figure()
#         fig, axes = plt.subplots(2, figsize=(8, 9))
#         # The top figure shows the data; bottom figure shows derived indicators.
#         data_ax = axes[0]
#         sal_ind_ax = axes[1]
#         sal_trend_ax = sal_ind_ax.twinx()
#     else:
#         data_ax, sal_ind_ax, sal_trend_ax = axes

#     results = results.dropna(how="any")

#     (data_line,) = data_ax.plot(
#         df.collected_date,
#         df.tds,
#         lw=1,
#         ls="-",
#         color="k",
#         marker="o",
#         ms=10,
#         mec="k",
#         mfc="none",
#     )
#     (mean_line,) = data_ax.plot(
#         df.collected_date,
#         df["mean"],
#         lw=2,
#         color="tab:blue",
#         dashes=(2, 0.8),
#         label="Mean salinity",
#     )
#     (trend_line,) = data_ax.plot(
#         tdf.timestamp,
#         tdf.predicted,
#         lw=2,
#         color="tab:red",
#         dashes=(10, 2),
#         label="Trend line",
#     )
#     data_label = data_ax.text(
#         0.5,
#         0.96,
#         results.iloc[-1].label,
#         transform=data_ax.transAxes,
#         ha="center",
#         va="top",
#     )
#     data_ax.grid(True, color="grey", lw=0.5, ls=":")
#     tds_range = df.tds.max() - df.tds.min()
#     data_ax.set_ylim(df.tds.min() - tds_range * 0.05, df.tds.max() + tds_range * 0.2)
#     data_ax.legend(frameon=False, fontsize="small")

#     (sal_ind_line,) = sal_ind_ax.plot(
#         pd.to_datetime(results.year.astype(str)),
#         results.current_pct_diff,
#         lw=1,
#         marker="o",
#         ms=10,
#         mfc="none",
#     )
#     (sal_trend_line,) = sal_trend_ax.plot(
#         pd.to_datetime(results.year.astype(str)),
#         results.slope_pct_change_yr * 10,
#         lw=1,
#         marker="d",
#         color="tab:red",
#         ms=10,
#         mfc="none",
#     )
#     sal_ind_ax.axhline(0, lw=2, color="tab:blue", dashes=(10, 2), alpha=0.5)
#     sal_trend_ax.axhline(0, lw=2, color="tab:red", dashes=(3, 0.8), alpha=0.5)
#     sal_ind_ax.grid(True, axis="y", color="tab:blue", lw=0.5, dashes=(10, 2), alpha=0.8)
#     sal_trend_ax.grid(
#         True, axis="y", color="tab:red", lw=0.5, dashes=(3, 0.8), alpha=0.8
#     )
#     sal_ind_ax.grid(True, axis="x", color="grey", lw=0.5, ls=":")

#     sal_ind_ax.set_ylim(results.current_pct_diff.min(), results.current_pct_diff.max())

#     plt.setp(sal_ind_ax.get_yticklabels(), color="tab:blue")
#     plt.setp(sal_trend_ax.get_yticklabels(), color="tab:red")

#     sal_ind_ax.set_ylabel("Salinity difference from mean (%)", color="tab:blue")
#     sal_trend_ax.set_ylabel("Salinity trend (%/decade)", color="tab:red")

#     x0, x1 = pd.Timestamp(str(df.collected_date.dt.year.min() - 1)), pd.Timestamp(
#         str(df.collected_date.dt.year.max() + 1)
#     )
#     data_ax.set_xlim(x0, x1)
#     sal_ind_ax.set_xlim(x0, x1)

#     return data_ax, sal_ind_ax, sal_trend_ax


def tweak_salinity_yaxis_limits(ax, bins):
    data_lims = ax.get_ylim()
    pos_bins = [b for b in bins if b > 0]
    neg_bins = [b for b in bins if b < 0]
    new_min = min([max(neg_bins), min(data_lims)])
    new_max = max([min(pos_bins), max(data_lims)])
    ax.set_yticks(bins)
    ax.set_ylim(new_min, new_max)


def plot_salinity_status_and_trend_simple(df, tdf, results, ax=None):
    """Plot salinity status and trend results.

    Args:
        df (pd.DataFrame): containing data
        tdf (pd.DataFrame): containing the trend line data
        results (pd.Series): containing the results of the calculation.
        ax (Axes): optional Axes object

    Returns: Axes object

    The data for this figure comes from the function :func:`get_historical_salinity_trends`,
    i.e. the last entry in the list of dataframes, and the last row of the
    "results" dataframe. It differs from the other method in that this only plots
    the data and trend, not the historical version of the trend.

    See also :func:`plot_salinity_status_and_trend_simple_with_indicators`

    """
    if not ax:
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)

    results = results.dropna(how="any")

    (data_line,) = ax.plot(
        df.collected_date,
        df.tds,
        lw=1,
        ls="-",
        color="k",
        marker="o",
        ms=10,
        mec="k",
        mfc="none",
    )
    (mean_line,) = ax.plot(
        df.collected_date,
        df["mean"],
        lw=2,
        color="tab:blue",
        dashes=(2, 0.8),
        label="Mean salinity",
    )
    (trend_line,) = ax.plot(
        tdf.timestamp,
        tdf.predicted,
        lw=2,
        color="tab:red",
        dashes=(10, 2),
        label="Trend line",
    )
    ax.grid(True, color="grey", lw=0.5, ls=":")
    tds_range = df.tds.max() - df.tds.min()
    ax.set_ylim(df.tds.min() - tds_range * 0.15, df.tds.max() + tds_range * 0.3)
    ax.legend(loc="lower center", frameon=False, fontsize="small", ncol=2)

    x0, x1 = pd.Timestamp(str(df.collected_date.dt.year.min() - 1)), pd.Timestamp(
        str(df.collected_date.dt.year.max() + 1)
    )
    ax.set_xlim(x0, x1)

    return ax


def plot_salinity_status_and_trend_simple_with_indicators(
    df, trend_df, trend_result, indicator_result, dfn, ax=None
):
    """Plot salinity status and trend results with indicator labels.

    Args:
        df (pd.DataFrame): containing data
        tdf (pd.DataFrame): containing the trend line data
        trend_result (pd.Series): containing the results of the calculation.
        indicator_result (pd.Series): row from dataframe containing the salinity
            indicator results e.g. columns "curr_tds_pct_diff", "curr_tds_pct_diff_indicator",
            "slope_pct_change_trend_pd", and "tds_trend_pct_change_indicator"
        dfn (pd.Series): row from the "Definitions_current_salinity_percent_diff"
            spreadsheet.
        ax (Axes): optional Axes object

    Returns: Axes object

    The data for this figure comes from the function :func:`get_historical_salinity_trends`,
    i.e. the last entry in the list of dataframes, and the last row of the
    "results" dataframe. It differs from the other method in that this only plots
    the data and trend, not the historical version of the trend.

    See also :func:`plot_salinity_status_and_trend_simple_with_indicators`

    """
    r = trend_result
    ax = plot_salinity_status_and_trend_simple(df, trend_df, r, ax=ax)
    ax.set_title(indicator_result.well_id)

    slabel = f"Current diff. to mean: {indicator_result.curr_tds_pct_diff:+.2f}%\n({indicator_result.curr_tds_pct_diff_indicator})"
    tlabel = f"Trend: {indicator_result.slope_pct_change_trend_pd:+.2f}% over {dfn.trend_length_years} yrs\n({indicator_result.tds_trend_pct_change_indicator})"
    ax.text(
        0.25,
        0.95,
        slabel,
        transform=ax.transAxes,
        color="white",
        bbox=dict(facecolor="tab:blue"),
        ha="center",
        va="top",
        fontsize="small",
    )
    ax.text(
        0.75,
        0.95,
        tlabel,
        transform=ax.transAxes,
        color="white",
        bbox=dict(facecolor="tab:red"),
        ha="center",
        va="top",
        fontsize="small",
    )

    ax.figure.tight_layout()
    return ax


def calculate_tds_bins(
    curr_sal=None,
    tds_bin_width=None,
    min_tds_colour=None,
    max_tds_colour=None,
    cmap=None,
    min_tds_bin=0,
    max_tds_bin=50000,
):
    """Generate colour bins for showing TDS data.

    Args:
        curr_sal (dict): dictionary with a key "tds" which stores an array
            of TDS values. If None, a synthetic one is generated which steps
            from the minimum to the maximum TDS specified, plus a high-salinity
            outlier.
        tds_bin_width (float): width of salinity bins.
        min_tds_colour ()

    """

    class Container:
        def summary(self):
            return {
                "cmap_name": self.cmap.name,
                "tds_bin_width": self.tds_bin_width,
                "min_tds_colour": self.min_tds_colour,
                "max_tds_colour": self.max_tds_colour,
                "min_tds_bin": self.min_tds_bin,
                "max_tds_bin": self.max_tds_bin,
            }

        def to_df(self):
            colours = [tuple(np.round(t, 3)) for t in self.bin_colours]
            r1 = np.asarray([t[0] for t in colours])
            g1 = np.asarray([t[1] for t in colours])
            b1 = np.asarray([t[2] for t in colours])
            alpha = np.array([t[3] for t in colours])
            r255 = r1 * 255
            g255 = g1 * 255
            b255 = b1 * 255
            rgb1 = [t[:3] for t in colours]
            rgba255 = [
                (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255), c[3])
                for c in colours
            ]
            edges = [
                (self.bin_left_edges[i], self.bin_right_edges[i])
                for i in range(len(colours))
            ]
            return pd.DataFrame(
                {
                    "edges": edges,
                    "left_edge": self.bin_left_edges,
                    "right_edge": self.bin_right_edges,
                    "label": self.bin_labels,
                    "centre": self.bin_centre_tds,
                    "rgba1": colours,
                    "rgb1": rgb1,
                    "rgba255": rgba255,
                    "rgb255": [c[:3] for c in rgba255],
                    "alpha": alpha,
                    "r1": r1,
                    "g1": g1,
                    "b1": b1,
                    "r255": r255,
                    "g255": g255,
                    "b255": b255,
                }
            )

    if curr_sal is None:
        curr_sal = {"tds": [min_tds_bin, max_tds_bin, max_tds_bin + 100000]}

    c = Container()
    c.tds_bin_width = tds_bin_width
    c.min_tds_colour = min_tds_colour
    c.max_tds_colour = max_tds_colour
    c.min_tds_bin = min_tds_bin
    c.max_tds_bin = max_tds_bin
    c.cmap = cmap

    c.n_above_max = len([t for t in curr_sal["tds"] if t > c.max_tds_bin])

    logger.debug(
        f"tds_bin_width={tds_bin_width} / "
        f"min_tds_colour={min_tds_colour} / "
        f"max_tds_colour={max_tds_colour} / "
        f"max_tds_bin={max_tds_bin}"
    )

    c.all_bins = np.arange(c.min_tds_bin, c.max_tds_bin + 1, c.tds_bin_width)
    c.all_counts, c.all_bin_edges = np.histogram(curr_sal["tds"], bins=c.all_bins)
    c.all_bin_left_edges = c.all_bin_edges[:-1]
    logger.debug(f"all_bins: {[x for x in zip(range(len(c.all_bins)), c.all_bins)]}")
    logger.debug(
        f"all_counts: {[x for x in zip(range(len(c.all_counts)), c.all_counts)]}"
    )
    logger.debug(
        f"all_bin_edges: {[x for x in zip(range(len(c.all_bin_edges)), c.all_bin_edges)]}"
    )
    logger.debug(
        f"all_bin_left_edges: {[x for x in zip(range(len(c.all_bin_left_edges)), c.all_bin_left_edges)]}"
    )

    for i in range(len(c.all_counts)):
        count = c.all_counts[i]
        logger.debug(f"Looking from left (low) for non-zero counts at {i}")
        if count > 0:
            i0 = i
            logger.debug(f"Found {i} -> i0 = {i0}")
            break

    if c.n_above_max == 0:
        for i in range(len(c.all_counts))[::-1]:
            count = c.all_counts[i]
            logger.debug(f"Looking from right (high) for non-zero counts at {i}")
            if count > 0:
                i1 = i
                logger.debug(f"Found {i} -> i1 = {i1}")
                break
    else:
        i1 = len(c.all_counts) - 1
        logger.debug(
            f"n_above_max > 0 ({c.n_above_max}) therefore not trimming high bins (right-hand side) -> i1 = {i1}"
        )
    c.bins = c.all_bins[i0 : i1 + 1]
    c.bin_left_edges = c.all_bin_left_edges[i0 : i1 + 1]
    c.bin_right_edges = c.bin_left_edges + c.tds_bin_width
    c.counts = c.all_counts[i0 : i1 + 1]
    c.bin_centre_tds = [b + tds_bin_width / 2 for b in c.bin_left_edges]
    c.bin_labels = [
        f"{c.bin_left_edges[i]:.0f} to {(c.bin_left_edges[i] + tds_bin_width):.0f}"
        for i in range(len(c.bin_left_edges))
    ]
    logger.debug(f"Trimmed bins: {list(zip(range(len(c.bins)), c.bins))}")
    logger.debug(
        f"Trimmed bin_left_edges: {list(zip(range(len(c.bin_left_edges)), c.bin_left_edges))}"
    )
    logger.debug(f"Trimmed counts: {list(zip(range(len(c.counts)), c.counts))}")
    logger.debug(
        f"Trimmed bin_centre_tds: {list(zip(range(len(c.bin_centre_tds)), c.bin_centre_tds))}"
    )

    c.bin_tds_normed = [
        (c.bin_centre_tds[i] - min_tds_colour) / (max_tds_colour - min_tds_colour)
        for i in range(len(c.bin_centre_tds))
    ]
    c.bin_colours = [cmap(c.bin_tds_normed[i]) for i in range(len(c.bin_tds_normed))]

    if c.n_above_max > 0:
        c.bins = np.append(c.bins, c.max_tds_bin)
        c.bin_colours.append(tuple(list(mcolors.to_rgb("crimson")) + [1]))
        c.bin_labels.append(f"Above {c.max_tds_bin:.0f}")
        c.bin_left_edges = np.append(c.bin_left_edges, c.max_tds_bin)
        c.bin_right_edges = np.append(c.bin_right_edges, max(curr_sal["tds"]))
        c.all_counts = np.append(c.all_counts, c.n_above_max)
        c.all_bin_edges = np.append(c.all_bin_edges, max(curr_sal["tds"]))
        c.counts = np.append(c.counts, c.n_above_max)
        c.bin_centre_tds.append(np.nan)
        c.bin_tds_normed.append(np.nan)

    logger.debug(
        f"Final bin_left_edges: {list(zip(range(len(c.bin_left_edges)), c.bin_left_edges))}"
    )
    logger.debug(f"Final counts: {list(zip(range(len(c.counts)), c.counts))}")
    logger.debug(
        f"Final bin_centre_tds: {list(zip(range(len(c.bin_centre_tds)), c.bin_centre_tds))}"
    )

    return c


def plot_tds_current_bars(tdsbinned, ax=None, **kwargs):
    c = tdsbinned

    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    x_counts = np.arange(len(c.counts))
    label_ypos = np.asarray(c.counts) + (max(c.counts) / 30)
    ax.barh(x_counts, c.counts, color=c.bin_colours, edgecolor="k")
    percentage_counts = [y / sum(c.counts) * 100 for y in c.counts]
    percentage_labels = [
        f"{pct:.0f}" for pct in round_to_100_percent(percentage_counts, 0)
    ]
    for i in range(len(x_counts)):
        if c.counts[i] > 0:
            ax.text(
                label_ypos[i],
                x_counts[i],
                percentage_labels[i] + "%",
                va="center",
                ha="left",
                color="#555555",
            )
    ax.set_yticks(np.arange(len(c.bin_labels)))
    ax.set_yticklabels(c.bin_labels)
    ax.set_ylim(len(c.bin_labels), -1)
    ax.set_ylabel("TDS (mg/L)")
    ax.set_xlabel("Number of wells")
    y0, y1 = ax.get_xlim()
    ax.xaxis.set_major_locator(
        mticker.MaxNLocator(nbins="auto", steps=[1, 2, 5, 10], integer=True)
    )
    ax.set_xlim(0, y1 + np.ceil((max(c.counts) / 30)))
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    return ax


def plot_tds_curr_pct_diff_bars(curr_pct_diffs, pct_diff, cm="auto", ax=None, **kwargs):
    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    if cm == "auto":
        cm = PctDiffColormap(pct_diff)
    bin_labels = curr_pct_diffs.curr_tds_pct_diff_indicator.values
    counts = curr_pct_diffs.n_wells.fillna(0).values
    logger.debug(f"counts = {counts}")
    x_counts = np.arange(len(counts))
    label_ypos = np.asarray(counts) + (max(counts) / 30)
    ax.barh(x_counts, counts, color=cm.bin_colours, edgecolor="k")
    percentage_counts = curr_pct_diffs.pct_wells.fillna(0).values
    percentage_labels = [
        f"{pct:.0f}" for pct in round_to_100_percent(percentage_counts, 0)
    ]
    for i in range(len(x_counts)):
        if counts[i] > 0:
            ax.text(
                label_ypos[i],
                x_counts[i],
                percentage_labels[i] + "%",
                va="center",
                ha="left",
                color="#555555",
            )
    ax.set_yticks(np.arange(len(bin_labels)))
    ax.set_yticklabels(bin_labels)
    ax.set_ylim(len(bin_labels), -1)
    # ax.set_ylabel("TDS (mg/L)")
    ax.set_xlabel("Number of wells")
    y0, y1 = ax.get_xlim()
    ax.xaxis.set_major_locator(
        mticker.MaxNLocator(nbins="auto", steps=[1, 2, 5, 10], integer=True)
    )
    ax.set_xlim(0, y1 + np.ceil((max(counts) / 30)))
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    return ax


def plot_tds_trend_pct_change_bars(
    tds_trend_pct_changes, trend_pct, cm="auto", ax=None, **kwargs
):
    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    if cm == "auto":
        cm = TrendPctColormap(trend_pct)
    bin_labels = tds_trend_pct_changes.tds_trend_pct_change_indicator.values
    counts = tds_trend_pct_changes.n_wells.fillna(0).values
    logger.debug(f"counts = {counts}")
    x_counts = np.arange(len(counts))
    label_ypos = np.asarray(counts) + (max(counts) / 30)
    ax.barh(x_counts, counts, color=cm.bin_colours, edgecolor="k")
    percentage_counts = tds_trend_pct_changes.pct_wells.fillna(0).values
    percentage_labels = [
        f"{pct:.0f}" for pct in round_to_100_percent(percentage_counts, 0)
    ]
    for i in range(len(x_counts)):
        if counts[i] > 0:
            ax.text(
                label_ypos[i],
                x_counts[i],
                percentage_labels[i] + "%",
                va="center",
                ha="left",
                color="#555555",
            )
    ax.set_yticks(np.arange(len(bin_labels)))
    ax.set_yticklabels(bin_labels)
    ax.set_ylim(len(bin_labels), -1)
    # ax.set_ylabel("TDS (mg/L)")
    ax.set_xlabel("Number of wells")
    y0, y1 = ax.get_xlim()
    ax.xaxis.set_major_locator(
        mticker.MaxNLocator(nbins="auto", steps=[1, 2, 5, 10], integer=True)
    )
    ax.set_xlim(0, y1 + np.ceil((max(counts) / 30)))
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    return ax


def plot_tds_current_map(
    tdsbinned,
    curr_sal,
    map_elements,
    map_annotations,
    ax=None,
    leg_frame=True,
    leg_loc="lower right",
    map_crs=8059,
    markersize=45,
    scattermarker="o",
    **kwargs,
):
    c = tdsbinned

    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    for spine in ax.spines.values():
        spine.set_visible(False)

    legend = []
    if len(map_elements):
        if "legend_zorder" in map_elements[0]:
            map_elements = sorted(map_elements, key=lambda x: x["legend_zorder"])
    for me in map_elements:
        me["shapely_object"].plot(ax=ax, **me["plot_kwargs"])
        if me.get("label", None):
            if me["legend_item_type"] == "line":
                legend_patch = ax.plot([], [], **me["legend_kwargs"])[0]
            elif me["legend_item_type"] == "rect":
                legend_patch = mpatches.Rectangle((0, 0), 1, 1, **me["legend_kwargs"])
            legend.append((me["label"], legend_patch))

    # bins_for_cut =  np.append(c.bins, c.bins[-1] + c.tds_bin_width)
    # logger.debug(f"bins_for_cut {bins_for_cut}")
    well_bin_lefts = np.array(
        [
            np.nan if i is np.nan else int(i.left)
            for i in pd.cut(curr_sal.tds, c.bin_left_edges, right=False)
        ]
    )
    well_bin_lefts = []
    for ix, row in curr_sal.iterrows():
        interval = False
        logger.debug(f"testing {row.well_id} {row.tds} against bins...")
        for i in range(len(c.bins)):
            b_left = c.bin_left_edges[i]
            b_right = c.bin_right_edges[i]
            if row.tds > b_left and row.tds <= b_right:
                interval = b_left
                break
        if interval is False:
            interval = np.nan
        well_bin_lefts.append(interval)

    logger.debug(
        "\n".join([str(x) for x in zip(curr_sal.well_id, curr_sal.tds, well_bin_lefts)])
    )

    tr = pyproj.Transformer.from_crs(7844, map_crs, always_xy=True)

    for i in range(len(c.bin_left_edges)):
        bin_left = c.bin_left_edges[i]
        idx = well_bin_lefts == bin_left
        lon = curr_sal[idx].longitude.values
        lat = curr_sal[idx].latitude.values
        logger.debug(
            f"Mapping {curr_sal[idx].well_id.values} for bin_left_edge {bin_left} ( lons = {lon}    lats = {lat}"
        )
        if len(lon):
            easting, northing = tr.transform(lon, lat)
            ax.scatter(
                easting,
                northing,
                marker=scattermarker,
                color=c.bin_colours[i],
                edgecolor="#555555",
                linewidth=0.3,
                s=markersize,
                zorder=5,
            )

    map_final_annotations = []
    for ann in map_annotations:
        if not ann["well_id"] in curr_sal.well_id.unique():
            logger.warning(
                f"****Warning: annotation {ann} is not in the dataset - cannot add it ******"
            )
        else:
            map_final_annotations.append(ann)

    for ann in map_final_annotations:
        row = curr_sal[curr_sal.well_id == ann["well_id"]].iloc[0]
        label = ann.get("label", ann["well_id"])
        easting, northing = tr.transform(row.longitude, row.latitude)
        arrowprops = ann.get("arrowprops", None)
        if arrowprops is not None:
            arrowprops = dict(
                {
                    "arrowstyle": "-|>",
                    "color": "#444444",
                    "mutation_scale": 8,
                    "shrinkA": 0,
                    "shrinkB": 0,
                },
                **arrowprops,
            )
        ax.annotate(
            label,
            (easting, northing),
            (easting + ann["x_km"] * 1000, northing + ann["y_km"] * 1000),
            color="#444444",
            fontsize="x-small",  # map annotation
            ha=ann["ha"],
            va=ann["va"],
            arrowprops=arrowprops,
            zorder=6,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    if len(legend):
        labels, patches = zip(*legend)
        if leg_frame:
            frameon = True
            framealpha = 1
            edgecolor = "white"
        else:
            frameon = False
            framealpha = None
            edgecolor = None
        leg = ax.legend(
            patches,
            labels,
            loc=leg_loc,
            fontsize="x-small",
            frameon=frameon,
            framealpha=framealpha,
            edgecolor=edgecolor,
        )
        for t in leg.get_texts():
            t.set_color("#444444")
    return ax


def plot_tds_curr_pct_diff_map(
    curr_pct_diff,
    pct_diff,
    map_elements,
    map_annotations,
    cm="auto",
    label_col="curr_tds_pct_diff_indicator",
    ax=None,
    leg_frame=True,
    leg_loc="lower right",
    map_crs=8059,
    markersize=45,
    scattermarker="s",
    **kwargs,
):
    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    for spine in ax.spines.values():
        spine.set_visible(False)

    legend = []
    if len(map_elements):
        if "legend_zorder" in map_elements[0]:
            map_elements = sorted(map_elements, key=lambda x: x["legend_zorder"])
    for me in map_elements:
        me["shapely_object"].plot(ax=ax, **me["plot_kwargs"])
        if me.get("label", None):
            if me["legend_item_type"] == "line":
                legend_patch = ax.plot([], [], **me["legend_kwargs"])[0]
            elif me["legend_item_type"] == "rect":
                legend_patch = mpatches.Rectangle((0, 0), 1, 1, **me["legend_kwargs"])
            legend.append((me["label"], legend_patch))

    if cm == "auto":
        cm = PctDiffColormap(pct_diff)

    tr = pyproj.Transformer.from_crs(7844, map_crs, always_xy=True)
    logger.debug(f"curr_pct_diff = \n{curr_pct_diff[['well_id', label_col]]}")

    for i in range(len(pct_diff["bins_left"])):
        label = pct_diff["labels"][i]
        idx = curr_pct_diff[label_col] == label
        lon = curr_pct_diff[idx].longitude.values
        lat = curr_pct_diff[idx].latitude.values
        if len(lon):
            easting, northing = tr.transform(lon, lat)
            ax.scatter(
                easting,
                northing,
                marker=scattermarker,
                color=cm.label_colours[i],
                edgecolor="#555555",
                linewidth=0.3,
                s=markersize,
                zorder=5,
            )

    map_final_annotations = []
    for ann in map_annotations:
        if not ann["well_id"] in curr_pct_diff.well_id.unique():
            logger.warning(
                f"****Warning: annotation {ann} is not in the dataset - cannot add it ******"
            )
        else:
            map_final_annotations.append(ann)

    for ann in map_final_annotations:
        row = curr_pct_diff[curr_pct_diff.well_id == ann["well_id"]].iloc[0]
        label = ann.get("label", ann["well_id"])
        easting, northing = tr.transform(row.longitude, row.latitude)
        arrowprops = ann.get("arrowprops", None)
        if arrowprops is not None:
            arrowprops = dict(
                {
                    "arrowstyle": "-|>",
                    "color": "#444444",
                    "mutation_scale": 8,
                    "shrinkA": 0,
                    "shrinkB": 0,
                },
                **arrowprops,
            )
        ax.annotate(
            label,
            (easting, northing),
            (easting + ann["x_km"] * 1000, northing + ann["y_km"] * 1000),
            color="#444444",
            fontsize="x-small",  # map annotation
            ha=ann["ha"],
            va=ann["va"],
            arrowprops=arrowprops,
            zorder=6,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    if len(legend):
        labels, patches = zip(*legend)
        if leg_frame:
            frameon = True
            framealpha = 1
            edgecolor = "white"
        else:
            frameon = False
            framealpha = None
            edgecolor = None
        leg = ax.legend(
            patches,
            labels,
            loc=leg_loc,
            fontsize="x-small",
            frameon=frameon,
            framealpha=framealpha,
            edgecolor=edgecolor,
        )
        for t in leg.get_texts():
            t.set_color("#444444")
    return ax


def plot_tds_trend_pct_change_map(
    tds_trend_pct_changes,
    trend_pct,
    map_elements,
    map_annotations,
    cm="auto",
    label_col="tds_trend_pct_change_indicator",
    ax=None,
    leg_frame=True,
    leg_loc="lower right",
    map_crs=8059,
    markersize=45,
    increase_scattermarker="^",
    decrease_scattermarker="v",
    **kwargs,
):
    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    for spine in ax.spines.values():
        spine.set_visible(False)

    legend = []
    if len(map_elements):
        if "legend_zorder" in map_elements[0]:
            map_elements = sorted(map_elements, key=lambda x: x["legend_zorder"])
    for me in map_elements:
        me["shapely_object"].plot(ax=ax, **me["plot_kwargs"])
        if me.get("label", None):
            if me["legend_item_type"] == "line":
                legend_patch = ax.plot([], [], **me["legend_kwargs"])[0]
            elif me["legend_item_type"] == "rect":
                legend_patch = mpatches.Rectangle((0, 0), 1, 1, **me["legend_kwargs"])
            legend.append((me["label"], legend_patch))

    if cm == "auto":
        cm = TrendPctColormap(trend_pct)

    tr = pyproj.Transformer.from_crs(7844, map_crs, always_xy=True)
    logger.debug(
        f"tds_trend_pct_changes = \n{tds_trend_pct_changes[['well_id', label_col]]}"
    )

    for i in range(len(trend_pct["bins_left"])):
        label = trend_pct["labels"][i]
        if "increase" in label:
            scattermarker = increase_scattermarker
        elif "decrease" in label:
            scattermarker = decrease_scattermarker
        idx = tds_trend_pct_changes[label_col] == label
        lon = tds_trend_pct_changes[idx].longitude.values
        lat = tds_trend_pct_changes[idx].latitude.values
        if len(lon):
            easting, northing = tr.transform(lon, lat)
            ax.scatter(
                easting,
                northing,
                marker=scattermarker,
                color=cm.label_colours[i],
                edgecolor="#555555",
                linewidth=0.3,
                s=markersize,
                zorder=5,
            )

    map_final_annotations = []
    for ann in map_annotations:
        if not ann["well_id"] in tds_trend_pct_changes.well_id.unique():
            logger.warning(
                f"****Warning: annotation {ann} is not in the dataset - cannot add it ******"
            )
        else:
            map_final_annotations.append(ann)

    for ann in map_final_annotations:
        row = tds_trend_pct_changes[
            tds_trend_pct_changes.well_id == ann["well_id"]
        ].iloc[0]
        label = ann.get("label", ann["well_id"])
        easting, northing = tr.transform(row.longitude, row.latitude)
        arrowprops = ann.get("arrowprops", None)
        if arrowprops is not None:
            arrowprops = dict(
                {
                    "arrowstyle": "-|>",
                    "color": "#444444",
                    "mutation_scale": 8,
                    "shrinkA": 0,
                    "shrinkB": 0,
                },
                **arrowprops,
            )
        ax.annotate(
            label,
            (easting, northing),
            (easting + ann["x_km"] * 1000, northing + ann["y_km"] * 1000),
            color="#444444",
            fontsize="x-small",  # map annotation
            ha=ann["ha"],
            va=ann["va"],
            arrowprops=arrowprops,
            zorder=6,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    if len(legend):
        labels, patches = zip(*legend)
        if leg_frame:
            frameon = True
            framealpha = 1
            edgecolor = "white"
        else:
            frameon = False
            framealpha = None
            edgecolor = None
        leg = ax.legend(
            patches,
            labels,
            loc=leg_loc,
            fontsize="x-small",
            frameon=frameon,
            framealpha=framealpha,
            edgecolor=edgecolor,
        )
        for t in leg.get_texts():
            t.set_color("#444444")
    return ax


def plot_tds_trend_triclass_bars(sal_trends, ax=None):
    gsr_colours = status_change_colours
    gsr_colours_rgba = {
        k: np.asarray([x / 255 for x in rgb] + [1]) for k, rgb in gsr_colours.items()
    }

    status_key_x = [0, 1, 2]
    status_keys = ["Increasing", "Stable", "Decreasing"]
    status_values = [
        len(sal_trends[sal_trends.status_change == v]) for v in status_keys
    ]
    status_colours = [gsr_colours_rgba[s] for s in status_keys]

    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.0))
        ax = fig.add_subplot(111)

    ax.barh(
        status_key_x,
        status_values,
        height=0.6,
        color=status_colours,
        edgecolor="#555555",
    )
    ax.set_yticks(status_key_x)
    ax.set_yticklabels(status_keys)  # rotation=40, ha="right")
    ax.set_ylim(status_key_x[-1] + 1, status_key_x[0] - 1)
    # ax.set_ylabel("Five year change in TDS (%)", fontsize="medium")

    label_ypos = np.asarray(status_values) + (max(status_values) / 30)
    percentage_counts = [y / sum(status_values) * 100 for y in status_values]
    percentage_labels = [
        f"{pct:.0f}" for pct in round_to_100_percent(percentage_counts, 0)
    ]
    for i, x in enumerate(status_key_x):
        if status_values[i] > 0:
            ax.text(
                label_ypos[i],
                x,
                percentage_labels[i] + "%",
                va="center",
                ha="left",
                color="#555555",
            )
    ax.set_xlabel("Number of wells", fontsize="medium")

    max_counts = max(status_values)
    ax.set_xlim(0, max_counts + (max_counts / 2.0))
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    return ax


def plot_tds_trend_triclass_map(
    sal_trends,
    map_elements,
    map_annotations,
    ax=None,
    leg_frame=True,
    map_crs=8059,
    leg_loc="lower right",
    markersize=60,
):
    tds_trend_map_markers = {"Increasing": "^", "Stable": "s", "Decreasing": "v"}

    gsr_colours = status_change_colours
    gsr_colours_rgba = {
        k: np.asarray([x / 255 for x in rgb] + [1]) for k, rgb in gsr_colours.items()
    }

    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    for spine in ax.spines.values():
        spine.set_visible(False)

    legend = []
    if len(map_elements):
        if "legend_zorder" in map_elements[0]:
            map_elements = sorted(map_elements, key=lambda x: x["legend_zorder"])
    for me in map_elements:
        me["shapely_object"].plot(ax=ax, **me["plot_kwargs"])
        if me.get("label", None):
            if me["legend_item_type"] == "line":
                legend_patch = ax.plot([], [], **me["legend_kwargs"])[0]
            elif me["legend_item_type"] == "rect":
                legend_patch = mpatches.Rectangle((0, 0), 1, 1, **me["legend_kwargs"])
            legend.append((me["label"], legend_patch))

    tr = pyproj.Transformer.from_crs(7844, map_crs, always_xy=True)
    for trend_label in ["Increasing", "Stable", "Decreasing"]:
        dfg = sal_trends[sal_trends.status_change == trend_label]
        if len(dfg):
            easting, northing = tr.transform(dfg.longitude.values, dfg.latitude.values)
            ax.scatter(
                easting,
                northing,
                marker=tds_trend_map_markers[trend_label],
                color=gsr_colours_rgba[trend_label],
                edgecolor="#555555",
                linewidth=0.3,
                s=markersize,
                zorder=5,
            )

    map_final_annotations = []
    for ann in map_annotations:
        if not ann["well_id"] in sal_trends.well_id.unique():
            logger.warning(
                f"****Warning: annotation {ann} is not in the dataset - cannot add it ******"
            )
        else:
            map_final_annotations.append(ann)

    for ann in map_final_annotations:
        row = sal_trends[sal_trends.well_id == ann["well_id"]].iloc[0]
        label = ann.get("label", ann["well_id"])
        easting, northing = tr.transform(row.longitude, row.latitude)
        arrowprops = ann.get("arrowprops", None)
        if arrowprops is not None:
            arrowprops = dict(
                {"arrowstyle": "->", "color": "#444444", "mutation_scale": 10},
                **arrowprops,
            )
        ax.annotate(
            label,
            (easting, northing),
            (easting + ann["x_km"] * 1000, northing + ann["y_km"] * 1000),
            color="#444444",
            fontsize="x-small",  # map annotation
            ha=ann["ha"],
            va=ann["va"],
            arrowprops=arrowprops,
            zorder=6,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    if len(legend):
        labels, patches = zip(*legend)
        if leg_frame:
            frameon = True
            framealpha = 1
            edgecolor = "white"
        else:
            frameon = False
            framealpha = None
            edgecolor = None
        leg = ax.legend(
            patches,
            labels,
            loc=leg_loc,
            fontsize="x-small",
            frameon=frameon,
            framealpha=framealpha,
            edgecolor=edgecolor,
        )
        for t in leg.get_texts():
            t.set_color("#444444")
    return ax


def plot_salinity_curr_pct_diffs_summary(
    curr_pct_diffs, pct_diff, results=None, cm="auto", style="internal", ax=None
):
    """Show summary figure for current TDS percentage differences.

    Args:
        curr_pct_diffs (pd.Series): from code
        pct_diff (dict): bins
        results (pd.DataFrame, optional): list of wells with curr_tds_pct_diff column. Optional.
        style (str): either 'internal' or 'publication'
        ax (Axes): optional
        cm (custom SalinityColormap object): or "auto" which will use
            :class:`wrap_technote.PctDiffColormap`.

    Returns: Axes object.

    """
    if style == "internal":
        ytick_fontsize = "small"
        default_figsize = (7, 4)
    elif style == "publication":
        ytick_fontsize = "medium"
        default_figsize = (5, 4)

    if cm == "auto":
        cm = PctDiffColormap(pct_diff)
    if ax is None:
        fig = plt.figure(figsize=default_figsize)
        ax = fig.add_subplot(111)
    y_idx = np.arange(len(curr_pct_diffs))
    ax.barh(
        y_idx,
        curr_pct_diffs.n_wells,
        color=cm.bin_colours,
        edgecolor="gray",
        linewidth=0.6,
    )
    ax.set_ylim(y_idx[-1] + 1, y_idx[0] - 1)
    _ = ax.set_yticks(y_idx)
    _ = ax.set_yticklabels(
        curr_pct_diffs.curr_tds_pct_diff_indicator, fontsize=ytick_fontsize
    )
    ax.set_xlabel("Number of wells")
    if style == "publication":
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    elif style == "internal":
        median_class = get_median_class(
            curr_pct_diffs.n_wells,
            class_values=curr_pct_diffs.curr_tds_pct_diff_indicator.values,
        )
        for i in y_idx:
            n = curr_pct_diffs.n_wells.iloc[i]
            pct = curr_pct_diffs.pct_wells.iloc[i]
            text = f"{n:.0f} ({pct:.1f}%)"
            ax.text(n, i, text, fontsize="small")
        label = f'Medians: class="{median_class}"'
        if not results is None:
            median_value = results.curr_tds_pct_diff.dropna().median()
            label += f" value={median_value:+.2f}%"
        ax.set_title(label, fontsize="small")
        x0, x1 = ax.get_xlim()
        ax.set_xlim(x0, x1 + (x1 - x0) / 10)
    ax.figure.tight_layout()
    return ax


def plot_salinity_trend_pct_summary(
    tds_trend_pct_changes, trend_pct, results=None, cm="auto", style="internal", ax=None
):
    """Show summary figure for current TDS percentage differences.

    Args:
        tds_trend_pct_changes (pd.Series): from code
        trend_pct (dict): bins
        results (pd.DataFrame, optional): list of wells with slope_pct_change_trend_pd column. Optional.
        cm (custom SalinityColormap object): or "auto" which will use
            :class:`wrap_technote.TrendPctColormap`.
        style (str): either 'internal' or 'publication'
        ax (Axes): optional

    Returns: Axes object.

    """
    if style == "internal":
        ytick_fontsize = "small"
        default_figsize = (7, 4)
    elif style == "publication":
        ytick_fontsize = "medium"
        default_figsize = (5, 4)
    if cm == "auto":
        cm = TrendPctColormap(trend_pct)
    if ax is None:
        fig = plt.figure(figsize=default_figsize)
        ax = fig.add_subplot(111)
    y_idx = np.arange(len(tds_trend_pct_changes))
    ax.barh(
        y_idx,
        tds_trend_pct_changes.n_wells,
        color=cm.bin_colours,
        edgecolor="gray",
        linewidth=0.6,
    )
    ax.set_ylim(y_idx[-1] + 1, y_idx[0] - 1)
    _ = ax.set_yticks(y_idx)
    _ = ax.set_yticklabels(
        tds_trend_pct_changes.tds_trend_pct_change_indicator, fontsize=ytick_fontsize
    )
    ax.set_xlabel("Number of wells")
    if style == "publication":
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    elif style == "internal":
        median_class = get_median_class(
            tds_trend_pct_changes.n_wells,
            class_values=tds_trend_pct_changes.tds_trend_pct_change_indicator,
        )
        for i in y_idx:
            n = tds_trend_pct_changes.n_wells.iloc[i]
            pct = tds_trend_pct_changes.pct_wells.iloc[i]
            text = f"{n:.0f} ({pct:.1f}%)"
            ax.text(n, i, text, fontsize="small")
        label = f'Medians: class="{median_class}"'
        if not results is None:
            median_value = results.slope_pct_change_trend_pd.dropna().median()
            label += f" value={median_value:+.2f}%"
        ax.set_title(label, fontsize="small")
    ax.figure.tight_layout()
    return ax


class SalinityBinsColormap(object):
    def __init__(self, bins_dfn, cmap, cmap_r):
        self.bins_dfn = bins_dfn
        self.labels = self.bins_dfn["labels"]
        self.split_labels = [
            l.replace("% above", "%\nabove").replace("% below", "%\nbelow")
            for l in self.labels
        ]

        self.norm_values = mcolors.Normalize(
            self.bins_dfn["bins"][1], self.bins_dfn["bins"][-2]
        )
        self.norm_label_indices = mcolors.Normalize(0, len(self.labels) - 1)

        self.cmap = copy.copy(plt.cm.get_cmap(cmap))
        self.cmap_values = copy.copy(plt.cm.get_cmap(cmap))
        self.cmap_label_indices = copy.copy(plt.cm.get_cmap(cmap_r))

        self.cmap.set_bad("darkgrey")
        self.cmap_values.set_bad("darkgrey")
        self.cmap_label_indices.set_bad("darkgrey")

        self.bin_colours = [
            self.cmap(self.norm_values(v)) for v in self.bins_dfn["bin_centres"]
        ]
        self.label_colours = [
            self.cmap_label_indices(self.norm_label_indices(i))
            for i in range(len(self.labels))
        ]
        self.label_to_index = dict(zip(self.labels, range(len(self.labels))))
        self.label_to_colour = dict(zip(self.labels, self.bin_colours))


class PctDiffColormap(SalinityBinsColormap):
    def __init__(self, bins_dfn):
        super().__init__(bins_dfn, "PiYG", "PiYG_r")


class TrendPctColormap(SalinityBinsColormap):
    def __init__(self, bins_dfn):
        super().__init__(bins_dfn, "BrBG", "BrBG_r")


def plot_salinity_historical_pct_diffs(
    tdsann,
    pct_diff,
    tds_indicator_col="tds_indicator",
    cm="auto",
    included_wells=None,
):
    """Plot historical salinity percent differences.

    Args:
        tdsann (pd.DataFrame): annual salinities - must have columns "well_id",
            "tds", "collected_year", and *tds_indicator_col* e.g. "tds_indicator"
        pct_diff (dict): definition of salinity percent difference bins
        tds_indicator_col (str): name of column in *tdsann* with the pct_diff indicator
            label
        cm (SalinityColormap, str): use "auto" to use PctDiffColormap

    """
    if cm == "auto":
        cm = PctDiffColormap(pct_diff)

    year0 = tdsann.collected_year.min()
    year1 = tdsann.collected_year.max()
    years = np.arange(year0, year1 + 1, 1)
    all_well_ids = sorted(tdsann.well_id.unique())
    if included_wells is not None:
        well_ids = list(included_wells) + [
            w for w in all_well_ids if not w in included_wells
        ]
    else:
        well_ids = all_well_ids
    nx = len(years)
    ny = len(well_ids)
    arr = np.empty((nx, ny), dtype=int) * np.nan
    for j in range(ny):
        well_id = well_ids[j]
        s = (
            tdsann[(tdsann.well_id == well_id)]
            .set_index("collected_year")[tds_indicator_col]
            .reindex(years)
        )
        arr[:, j] = s.map(cm.label_to_index).values

    fig_x = nx / 8
    fig_y = ny / 8
    fig_y2 = fig_y + 1.5
    min_fig_y = 5
    if fig_y2 < min_fig_y:
        fig_y2 = min_fig_y
    fig = plt.figure(figsize=(fig_x, fig_y2))
    gs = gridspec.GridSpec(2, 1, height_ratios=(20, 1))
    ax = fig.add_subplot(gs[0])
    cax = fig.add_subplot(gs[1])
    axim = ax.imshow(arr.T, cmap=cm.cmap_label_indices, aspect="auto")
    for j in range(ny):
        ax.axhline(j - 0.5, color="grey", lw=0.3)

    if included_wells is not None:
        ax.axhline(len(included_wells) - 0.5, color="green", lw=1.5)
    cbar = plot_colorbar(
        cax=cax,
        colours=cm.label_colours,
        cbar_labels=cm.split_labels,
        orientation="horizontal",
    )
    cbar.ax.tick_params(labelsize="small")
    plt.setp(cbar.ax.get_xticklabels(), rotation=30, ha="right")
    for i, y in enumerate(years):
        if y % 10 == 0:
            ax.axvline(i - 0.5, lw=0.5, color="k")
        elif y % 5 == 0:
            ax.axvline(i - 0.5, lw=0.5, dashes=(10, 2), color="k")
        else:
            ax.axvline(i - 0.5, lw=0.3, color="grey")

    # ax.set_ylim(*ax.get_ylim()[::-1])
    _ = ax.set_xticks(range(len(years)))
    _ = ax.set_xticklabels(
        [str(y) for y in years], rotation=90, fontsize="x-small", ha="center"
    )
    _ = ax.set_yticks(range(len(well_ids)))
    _ = ax.set_yticklabels(well_ids, fontsize="x-small")
    ax.tick_params(
        "y", which="major", left=True, right=True, labelleft=True, labelright=True
    )
    ax.tick_params(
        "x", which="major", top=True, bottom=True, labeltop=True, labelbottom=True
    )
    fig.tight_layout()
    return ax, cax
