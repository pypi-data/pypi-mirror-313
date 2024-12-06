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


def plot_wl_data_validation(
    wls,
    removals=None,
    well_ids=None,
    well_id_col="well_id",
    well_title_col="well_title",
    dt_col="obs_date",
    wl_col="rswl",
    label_col="reason",
    show_comments=True,
    adjust_comments=False,
    adjust_text_lim=5,
    path=".",
    ms=3,
    savefig_and_close=False,
    dpi=130,
    leg_fontsize="x-small",
    comment_fontsize="x-small",
    **kws,
):
    """Plot a graph of salinity data for validation purposes.

    Args:
        wls (pandas.DataFrame): water level data
        removals (pandas.DataFrame): removed water level data (should contain
            the column *label_col* as well)
        well_id_col (str): unique identifier for the well in both dataframes.
        well_ids (list): if you only want to plot one or two wells, specify
            them here. By default, it will iterate over all wells in the dataframes.
        dt_col (str): datetime column in both dataframes
        wl_col (str): water level data column in both dataframes
        ms (int): marker size default =3
        label_col (str): reason for removal of data (only needed in the
            *removals* dataframe)
        show_comments (bool): show comments from SA Geodata as text labels.
        adjust_comments (bool): use the adjustText python library to attempt
            and move the comment labels so that they do not overlap. It is quite
            slow, so be aware of that.
        adjust_text_lim (int): number of iterations for adjustText to run. 2 or 3
            will be fast but likely ineffective for all but the simplest plots.
            100 will be quite slow but a thorough test on almost all plots. 30
            is a good compromise.
        path (str): path to save figures into.
        savefig_and_close (bool): save fig to png and close
        dpi (int): resolution of saved PNGs00

    Returns:
        list: a list of matplotlib Axes.

    Any keyword arguments beginning with ``adjust_text`` will be sent to the
    :func:`adjustText.adjust_text` function, so for example to tell adjustText to
    use autoalign, pass *adjust_text_autoalign=True* to this function.

    .. todo:: Add example chart for plot_wl_data_validation

    """
    if well_ids is None:
        if removals is not None:
            if len(removals):
                well_ids = sorted(
                    list(
                        set(
                            list(wls[well_id_col].unique())
                            + list(removals[well_id_col].unique())
                        )
                    )
                )
        else:
            well_ids = list(set(list(wls[well_id_col].unique())))
    axes = []

    if savefig_and_close:
        fig = plt.figure(figsize=(8, 4))

    for i, well_id in enumerate(well_ids):
        logger.debug(f"Charting WL data for {well_id}")
        if savefig_and_close:
            ax = fig.add_subplot(111)
        else:
            fig = plt.figure(figsize=(8, 4))
            ax = fig.add_subplot(111)

        w_wls = wls[wls[well_id_col] == well_id]
        if not well_title_col in w_wls:
            well_title = ""
        else:
            well_title = w_wls[well_title_col].dropna()
            if len(well_title) > 1:
                well_title = well_title.iloc[0]
            else:
                well_title = well_id
        logger.debug(f"Also known as {well_title}")

        if removals is not None:
            w_removals = removals[removals[well_id_col] == well_id]

        ax.set_prop_cycle(color=removal_reason_colours)
        if removals is not None:
            for reason, rdf in w_removals.groupby("reason"):
                ax.plot(rdf[dt_col], rdf[wl_col], marker="X", lw=0, label=reason)
        if len(w_wls):
            ax.plot(
                w_wls[w_wls.database == "Aquarius"][dt_col],
                w_wls[w_wls.database == "Aquarius"][wl_col],
                lw=0,
                marker=".",
                ms=ms,
                color="gray",
                alpha=1,
                label="Aquarius",
            )
            ax.plot(
                w_wls[w_wls.database == "SA Geodata"][dt_col],
                w_wls[w_wls.database == "SA Geodata"][wl_col],
                lw=0,
                marker=".",
                ms=ms,
                color="black",
                alpha=1,
                label="SA Geodata",
            )
            (wl_line,) = ax.plot(
                w_wls[dt_col],
                w_wls[wl_col],
                lw=0.2,
                marker="",
                color="black",
                alpha=1,
                label="Filtered data",
            )
        texts = []
        if show_comments:
            w_wls_c = w_wls[~pd.isnull(w_wls.comments)]
            if len(w_wls_c):
                ax.plot(
                    w_wls_c[dt_col],
                    w_wls_c[wl_col],
                    marker="o",
                    lw=0,
                    mfc="none",
                    mec="purple",
                    mew=0.5,
                    label="SA Geodata comments",
                )
                for j, (idx, row) in enumerate(w_wls_c.iterrows()):
                    x = row[dt_col]
                    y = row[wl_col]
                    text = ax.text(
                        x,
                        y,
                        f'"{row.comments}"'.replace(".", ".\n"),
                        color="purple",
                        fontsize=comment_fontsize,
                    )
                    texts.append(text)
        ax.legend(fontsize=leg_fontsize, frameon=False, ncol=2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title(well_title)
        ax.set_ylabel(wl_col)
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_minor_locator(mdates.YearLocator())
        ax.grid(True, lw=0.5, color="#aaaaaa", alpha=0.5, ls="-")
        ax.grid(
            True, which="minor", axis="x", lw=0.5, color="#aaaaaa", alpha=0.5, ls=":"
        )

        y0, y1 = sorted(ax.get_ylim())
        if wl_col.lower() != "rswl":
            ax.set_ylim(y1, y0)
        else:
            ax.set_ylim(y0, y1)

        # Rearrange the labels if requested
        if adjust_comments:
            logger.debug(
                f"Using adjust_text to shift comment annotations for {well_id}"
            )
            adjust_text_kws = {}
            adjust_text_kws["arrowprops"] = kws.get(
                "adjust_text_arrowprops", dict(arrowstyle="->", color="purple", lw=0.4)
            )
            adjust_text_kws["autoalign"] = kws.get("adjust_text_autoalign", False)
            adjust_text_kws["lim"] = adjust_text_lim
            for key, argval in kws.items():
                if key.startswith("adjust_text"):
                    adjust_text_kws[key.replace("adjust_text_", "")] = argval
            adjust_text(
                texts,
                x=mdates.date2num(wl_line.get_xdata()),
                y=wl_line.get_ydata(),
                **adjust_text_kws,
            )

        if savefig_and_close:
            fig.savefig(
                str(Path(path) / f"plot_wl_data_validation_{well_id}.png"), dpi=dpi
            )
            fig.clf()
        else:
            axes.append(ax)

    return axes


def plot_wl_months_coloured(
    df, wl_col="rswl", dt_col="obs_date", mcmap=None, fig=None, ax=None, cax=None
):
    """Plot water level with months highlighted in colours.

    Args:
        df (:class:`pandas.DataFrame`): table of data to plot
        wl_col (str): column of *df* with water level measurements
        dt_col (str): column of *df* with datetime of observations
        mcmap (:class:`wrap_technote.MonthlyColormap`, optional):
            special object catering for the colour mapping to use
            for the months.
        fig (:class:`matplotlib.pyplot.Figure`)
        ax (:class:`matplotlib.pyplot.Axes`): axes to use for the
            main chart
        cax (:class:`matplotlib.pyplot.Axes`): axes to use for the
            colour mapping legend

    Returns:
        dict: dictionary with keys *ax* (:class:`matplotlib.pyplot.Axes`),
        *cbar* (:class:`matplotlib.colorbar.Colorbar`), and
        *mcmap* (:class:`wrap_technote.MonthlyColormap`)

    Example:

    .. code-block:: python

        >>> import wrap_technote, dew_gwdata
        >>> db = dew_gwdata.sageodata()
        >>> wls = db.water_levels(db.find_wells("PLL013"))
        >>> wrap_technote.plot_wl_months_coloured(wls)

    .. figure:: figures/plot_wl_months_coloured.png

    """
    if mcmap is None:
        mcmap = MonthlyColormap()
    if fig is None:
        fig = plt.figure(figsize=(7, 3))
    if ax is None:
        ax = fig.add_subplot(111)

    ax.plot(df[dt_col], df[wl_col], marker="None", lw=0.5, color="black")
    pc = ax.scatter(
        df[dt_col],
        df[wl_col],
        c=[mcmap.cmap(mcmap.norm(d.month)) for d in df[dt_col]],
        lw=0.1,
        edgecolor="black",
        marker="o",
        s=30,
        zorder=10,
        cmap=mcmap.cmap,
        norm=mcmap.norm,
        alpha=0.8,
    )
    cbar = plt.colorbar(mcmap.mappable, cax=cax)

    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    c0, c1 = cbar.mappable.get_clim()
    cbar_ticks = []
    cbar_labels = []
    cbar_divisions = 12
    cbar_step = (c1 - c0) / cbar_divisions
    for i, value in enumerate(range(1, 13)):
        cbar_labels.append(month_names[i])
        cbar_ticks.append(((cbar_step * i) + c0) + (cbar_step / 2))

    cbar.set_ticks(cbar_ticks)
    cbar.set_ticklabels(cbar_labels)

    ax.set_ylabel(wl_col)

    y0, y1 = sorted(ax.get_ylim())
    if wl_col.lower() != "rswl":
        ax.set_ylim(y1, y0)
    else:
        ax.set_ylim(y0, y1)

    return {"ax": ax, "cbar": cbar, "mcmap": mcmap}


def plot_wl_seasonality(
    df,
    anndf=None,
    seasons=None,
    dots=False,
    annmarkers="large & open",
    dt_col="obs_date",
    wl_col="rswl",
    span_length=5,
    style="default",
):
    """Make a chart for analysing seasonal highs and lows for a well.

    Args:
        df (:class:`pandas.DataFrame`): water level data
        anndf (:class:`pandas.DataFrame`, optional): annual seasonal
            water level max and mins. Should
            also have a season column "season", and each season for each year,
            "year+season", each containing strings.
            If it is not supplied, no seasonal breakdown is charted.
        seasons (:class:`wrap_technote.Seasons`, optional): definition of seasons
        dots (bool): show each measurement as a dot
        annmarkers (str): markers for the annual mins and maxs. Either "large & open"
            or "small & filled".
        dt_col (str): datetime column in ``df`` (and ``anndf`` if supplied)
        wl_col (str): water level column in ``df`` (and ``anndf`` if supplied)
        span_length (int): number of years in each pane of the figure
        style (str): matplotlib style

    Returns:
        dict: dictionary with keys "fig" and "axes" (the latter is a list)

    Example:

    .. code-block:: python

        >>> import wrap_technote, dew_gwdata
        >>> db = dew_gwdata.sageodata()
        >>> wls = db.water_levels(db.find_wells("MOR100"))
        >>> wrap_technote.plot_wl_seasonality(wls, dots=True)

    .. figure:: figures/plot_wl_seasonality_1.png

    To define seasonal summer/recovery periods and also show the seasonal
    max and mins:

    .. code-block:: python

        >>> seasons = (
        ...     wrap_technote.Seasons()
        ...     .append("recovery", "max", end=wrap_technote.doy("Jan 15"))
        ...     .append("pumped", "min", end=wrap_technote.doy("Jul 1"))
        ...     .append("recovery", "max")
        ... )
        >>> annualdata = wrap_technote.analyse_wl_by_seasons(wls, seasons)
        >>> wrap_technote.plot_wl_seasonality(wls, annualdata, seasons=seasons)

    .. figure:: figures/plot_wl_seasonality_2.png

    """

    colours = [
        np.asarray(plt.cm.hsv(i)) * 0.8 for i in np.linspace(0, 1, span_length + 1)
    ]

    year_min = df[dt_col].dt.year.min()
    year_max = df[dt_col].dt.year.max()

    yearspan_starts = list(get_yearspans_between(year_min, year_max + 1, span_length))
    dayofyears = list(month_dayofyears.values())
    month_labels = list(month_dayofyears.keys())

    # Obtain a grid of chart axes.
    ncol = 3
    nrow = int(np.ceil((len(yearspan_starts) / ncol)))
    logger.debug(f"style on plot_wl_seasonality: {style}")
    with plt.style.context(style):
        fig, axes = plt.subplots(
            nrow,
            ncol,
            figsize=(10, 3.0 * nrow),
            sharey="row",
            sharex=True,
            gridspec_kw=dict(wspace=0.05, hspace=0),
        )

        # Get the Axes object as a 1-dimensional list.
        axes = axes.ravel()

        ylims = {}
        for k, yearspan_start in enumerate(yearspan_starts):
            col_ix = k % ncol

            # Use a new axis for each
            ax = axes[k]

            yearspan_end = yearspan_start + span_length

            plotted = False

            # Chart each year as a separate line.
            for i, year in enumerate(range(yearspan_start, yearspan_end)):
                # We want the line to extend off the chart into the previous year's data,
                # and to the following year's data. Any gap larger than 3 years will appear
                # as a break in the line.
                df3yr = df[abs(df[dt_col].dt.year - year) <= 1]
                doy_offset = (df3yr[dt_col] - datetime(year, 1, 1)).dt.days

                # Ensure that January 1st (i.e. offset of 0) has value of 1
                doy_offset += 1

                # If there is data from the year in question, chart the line.
                if dots:
                    marker = "o"
                    ms = 1
                else:
                    marker = "None"
                    ms = None
                if colours:
                    c = colours[i]
                else:
                    c = None
                if len(df3yr[df3yr[dt_col].dt.year == year]):
                    plotted = True
                    (l2,) = ax.plot(
                        doy_offset,
                        df3yr[wl_col],
                        lw=0.5,
                        marker=marker,
                        ms=ms,
                        alpha=1,
                        label=year,
                        color=c,
                    )

                if not anndf is None and seasons is not None:
                    # Find any maxmins occurring in this calendar year and plot them
                    dfym = anndf[anndf[dt_col].dt.year == year]
                    for season, dfyms in dfym.groupby("season"):
                        s_doy_offset = (
                            dfyms[dt_col] - datetime(year, 1, 1)
                        ).dt.days + 1
                        marker = seasons.period_kws[season].get("marker", "s")
                        if annmarkers == "large & open":
                            kws = dict(ms=9, mec=l2.get_color(), mew=1, mfc="none")
                        elif annmarkers == "small & filled":
                            kws = dict(
                                ms=4, mec=l2.get_color(), mew=1, mfc=l2.get_color()
                            )
                        ax.plot(
                            s_doy_offset,
                            dfyms[wl_col],
                            marker=marker,
                            ls="none",
                            label="",
                            **kws,
                        )

            labels_plotted = []
            if not seasons is None:
                # Show the seasons as striped sections.
                for period in seasons.periods:
                    season = period["season"]
                    color = seasons.period_kws[season].get("color", "k")
                    if season in labels_plotted:
                        label = None
                    else:
                        label = season
                    ax.axvspan(
                        period["start"],
                        period["end"],
                        color=color,
                        alpha=0.05,
                        label=label,
                    )
                    labels_plotted.append(season)

            ax.legend(fontsize="x-small", ncol=3, frameon=True, framealpha=0.4)
            ax.set_xlim(0, 366)
            ax.set_xticks(dayofyears)
            ax.set_xticklabels(month_labels)
            if k < ncol:
                ax.tick_params(
                    axis="x", bottom=True, top=True, labelbottom=False, labeltop=True
                )
            plt.setp(
                ax.get_xticklabels(), fontsize="x-small"
            )  # rotation=20, ha="right")
            ax.grid(True, lw=0.1, alpha=0.2)
            if k % ncol == 0:
                ax.set_ylabel(wl_col, fontsize="small")
            plt.setp(ax.get_yticklabels(), fontsize="small")

        for ka in range(len(axes)):
            if ka > k:
                axes[ka].set_visible(False)
            else:
                if wl_col.lower() != "rswl":
                    w_bottom = df[wl_col].max()
                    w_top = df[wl_col].min()
                else:
                    w_bottom = df[wl_col].min()
                    w_top = df[wl_col].max()
                axes[ka].set_ylim(w_bottom, w_top)

        # fig.tight_layout()
        return {"fig": fig, "axes": axes}


def plot_wl_seasonal_timeseries(
    df, anndf, scatter=False, seasons=None, mcmap=None, ax=None, fig=None, cax=None
):
    """Plot the seasonal max and min water levels for a time series.

    Args:
        df (:class:`pandas.DataFrame`): water level data set
        anndf (:class:`pandas.DataFrame`): data set of annual max and mins
            from *df* (use :func:`wrap_technote.analyse_wl_by_seasons` to
            obtain this table)
        scatter (bool): show annual max/mins as dots
        seasons (:class:`wrap_technote.Seasons`): definition of seasonal
            variations, useful for controlling the plotting style of the
            max/min lines. Not needed normally.
        mcmap (:class:`wrap_technote.MonthlyColormap`, optional): show
            coloured dots for the month of each observation.
        ax (Axes, optional): main plot
        fig (Figure, optional): main figure
        cax (matplotlib Axes, optional): axes to draw the color mapping legend
            in (only needed if scatter is True and mcmap is supplied)

    Returns:
        :class:`matplotlib.Axes`: axes object

    Example:

    .. code-block:: python

        >>> import wrap_technote, dew_gwdata
        >>> db = dew_gwdata.sageodata()
        >>> wls = db.water_levels(db.find_wells("PLL013"))
        >>> wrap_technote.plot_wl_months_coloured(wls, dots=True, span_length=6)
        >>> # Define seasonal periods
        >>> seasons = (
        ...     wrap_technote.Seasons()
        ...     .append("summer", "min", end=doy("2018-03-15"), marker="v", color="red")
        ...     .append("recovery", "max", end=doy("2018-11-15"), marker="^", color="blue")
        ...     .append("summer", "min")
        ... )
        >>> # Calculate annual max and mins
        >>> annualdata = wrap_technote.analyse_wl_by_seasons(wls, seasons)
        >>> wrap_technote.plot_wl_seasonal_timeseries(wls, annualdata)

    .. figure:: figures/plot_wl_seasonal_timeseries_1.png

    To change the way the chart looks - e.g. show recovery as a black line
    and to not show summer minimums.

    .. code-block:: python

        >>> seasons.period_kws["recovery"]["color"] = "black"
        >>> seasons.period_kws["summer"]["color"] = "none"
        >>> wrap_technote.plot_wl_seasonal_timeseries(
        ...     wls,
        ...     annualdata,
        ...     seasons=seasons,
        ...     scatter=True,
        ...     mcmap=wrap_technote.MonthlyColormap(),
        ... )

    .. figure:: figures/plot_wl_seasonal_timeseries_2.png

    """
    if fig is None:
        fig = plt.figure(figsize=(7, 3))
    if ax is None:
        ax = fig.add_subplot(111)

    if scatter:
        if mcmap:
            c = [mcmap.norm(d.month) for d in df.obs_date]
            cmap = mcmap.cmap
        else:
            c = "gray"
            cmap = None
        cset = ax.scatter(
            df.obs_date,
            df.rswl,
            c=c,
            lw=0.1,
            edgecolor="black",
            cmap=cmap,
            label="",
            s=12,
        )

        if mcmap:
            cbar = plt.colorbar(mcmap.mappable, cax=cax)

            month_names = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
            c0, c1 = cbar.get_clim()
            cbar_ticks = []
            cbar_labels = []
            cbar_divisions = 12
            cbar_step = (c1 - c0) / cbar_divisions
            for i, value in enumerate(range(1, 13)):
                cbar_labels.append(month_names[i])
                cbar_ticks.append(((cbar_step * i) + c0) + (cbar_step / 2))

            cbar.set_ticks(cbar_ticks)
            cbar.set_ticklabels(cbar_labels)

    ax.plot(df.obs_date, df.rswl, marker="None", color="gray", lw=0.4, label="All data")

    for season, seasondf in anndf.groupby("season"):
        if not seasons is None:
            color = seasons.period_kws[season]["color"]
        else:
            color = None
        ax.plot(
            seasondf.obs_date,
            seasondf.rswl,
            label=season,
            lw=0.8,
            color=color,
            marker=None,
        )

    ax.legend(fontsize="small")
    ax.set_ylabel("RSWL (m AHD)")
    return ax


def plot_wl_bom_classes(
    df_classes,
    df_all=None,
    dt_col="obs_date",
    wl_col="rswl",
    bom_class_col="rswl_bom_class",
    ax=None,
    fig=None,
    cax=None,
    bcmap=None,
    classes_scatter=None,
    all_scatter=None,
    break_hydrograph_at=None,
    tight_layout=True,
):
    """Create hydrograph with annual ranked recovered levels highlighted
    using the BoM classification.

    Args:
        df_classes (:class:`pandas.DataFrame`): table with the BoM
            classification of the ranked recovered water level
            (see a filtered version of :func:`wrap_technote.analyse_wl_by_seasons`
            for how to obtain this table)
        df_all (:class:`pandas.DataFrame`): table with all data
            for the background hydrograph
        dt_col (str): column in both *df_classes* and *df_all* with the
            measurement datetime
        wl_col (str): column in both *df_classes* and *df_all* with the
            annual/recovered water level
        bom_class_col (str): column in *df_classes* with the ranked BoM
            classification as a string e.g. "Very much below average"
        ax (mpl.Axes)
        fig (mpl.Figure)
        cax (either False, None, or mpl.Axes): if it is False, then a
            colorbar will not be drawn.
        bcmap (:class:`wrap_technote.BoMClassesColormap`)
        break_hydrograph_at (tuple): list of datetimes to break the df_all table into to
            plot.

    Returns:
        dict: dictionary with keys *ax* (:class:`matplotlib.pyplot.Axes`),
        *cbar* (:class:`matplotlib.colorbar.Colorbar`), and
        *bcmap* (:class:`wrap_technote.MonthlyColormap`)

    Example:

    .. code-block:: python

        >>> import wrap_technote as tn
        >>> import dew_gwdata
        >>> db = dew_gwdata.sageodata()
        >>> wls = db.water_levels(db.find_wells("BRS020"))
        >>> wls = tn.filter_wl_observations(wls)
        >>> seasons = (
        ...     tn.Seasons()
        ...     .append("stressed", "min", end=tn.doy("May 15"))
        ...     .append("recovery", "max", end=tn.doy("Nov 15"))
        ...     .append("stressed", "min")
        ... )
        >>> wls_ann = tn.analyse_wl_by_seasons(wls, seasons)
        >>> # Keep only the recovered annual water level.
        >>> wls_rec = wls_ann.loc[wls_ann.season == "recovery"]
        >>> wls_rec["rswl_percentile"] = wls_rec.rswl.rank(pct=True) * 100
        >>> wls_rec["rswl_bom_class"] = wls_rec.rswl_percentile.transform(tn.percentile_to_bom_class)
        >>> tn.plot_wl_bom_classes(wls_rec, wls)

    .. figure:: figures/plot_wl_bom_classes.png

    """
    if ax is None:
        if fig is None:
            fig = plt.figure(figsize=(7, 3))
        ax = fig.add_subplot(111)
    if bcmap is None:
        bcmap = BoMClassesColormap()
    if classes_scatter is None:
        classes_scatter = {}
    if all_scatter is None:
        all_scatter = {}
    all_scatter = dict(dict(lw=0.3, color="black"), **all_scatter)
    classes_scatter = dict(
        dict(edgecolor="k", linewidth=0.5, s=50, marker="o"), **classes_scatter
    )
    if break_hydrograph_at is None:
        break_hydrograph_at = []
    break_hydrograph_at.append(df_all[dt_col].max() + timedelta(days=1))

    if df_all is not None:
        start_date = df_all[dt_col].min() - timedelta(days=1)
        for end_date in sorted(break_hydrograph_at):
            didx = (df_all[dt_col] > start_date) & (df_all[dt_col] < end_date)
            ax.plot(df_all.loc[didx, dt_col], df_all.loc[didx, wl_col], **all_scatter)
            start_date = end_date
    cset = ax.scatter(
        df_classes[dt_col],
        df_classes[wl_col],
        c=[bom_classes.index(x) for x in df_classes[bom_class_col]],
        cmap=bcmap.cmap,
        **classes_scatter,
    )
    cbar = None
    if cax is not False:
        cbar = plt.colorbar(cset, cax=cax)
        bcmap.fix_ticklabels(cbar)

    ax.set_xlabel("Date")
    ax.set_ylabel("RSWL (m AHD)")
    if tight_layout:
        ax.figure.tight_layout()

    y0, y1 = sorted(ax.get_ylim())
    if wl_col.lower() != "rswl":
        ax.set_ylim(y1, y0)
    else:
        ax.set_ylim(y0, y1)

    return {"ax": ax, "cax": cax, "cbar": cbar}


def plot_wls_with_logger(
    manual_df,
    logger_df=None,
    ax=None,
    dt_col="obs_date",
    wl_col="dtw",
    zoom_to="all",
    zoom_buffer=None,
):
    """Plot a graph of water levels including Aquarius logger data
    if available.

    Args:
        manual_df (:class:`pandas.DataFrame`): manual WL observations
        logger_df (:class:`pandas.DataFrame`): continuous logger WL
            observations
        dt_col (str): columns in both *manual_df* and *logger_df*
            that contain datetimes
        wl_col (str): columns in both *manual_df* and *logger_df*
            that contain water levels (measured as depth to water)
        zoom_to (str): "all", "logger", "since-logger"
        zoom_buffer (timedelta): buffer on zoom, 1 month by default
            You can set it to False for no buffer

    Returns:
        :class:`matplotlib.pyplot.Axes`: axes object

    Example:

    .. code-block:: python

        >>> import wrap_technote as tn, dew_gwdata
        >>> db = dew_gwdata.sageodata()
        >>> sag_df = db.water_levels(db.find_wells("MUW034"))
        >>> hyd_df = db.fetch_hydstra_dtw_data(wells)
        >>> tn.plot_wls_with_logger(sag_df, hyd_df)

    .. figure:: figures/plot_wls_with_logger.png

    The *zoom_to* keyword argument will help with visualizing wells that
    have a long history:

    .. code-block:: python

        >>> sag_df = db.water_levels(db.find_wells("YAT37"))
        >>> hyd_df = db.fetch_hydstra_dtw_data(wells)
        >>> tn.plot_wls_with_logger(sag_df, hyd_df, zoom_to="since-logger")

    .. figure:: figures/plot_wls_with_logger_2.png

    """
    if ax is None:
        ax = plt.gca()
    if not logger_df is None:
        for qc, dfq in logger_df.groupby("grade"):
            m = "."
            (f,) = ax.plot(dfq[dt_col], dfq[wl_col], lw=0.8)
            ax.scatter(
                [],
                [],
                marker=m,
                facecolor=f.get_color(),
                s=100,
                label=f"Aquarius QC\n{qc}",
            )
        if len(logger_df):
            lims = (
                max(logger_df[wl_col].max(), manual_df[wl_col].max()),
                min(logger_df[wl_col].min(), manual_df[wl_col].min()),
            )
        else:
            lims = manual_df[wl_col].max(), manual_df[wl_col].min()
        if wl_col.lower() == "rswl":
            lims = lims[::-1]
        ax.set_ylim(*lims)
        ax.set_ylabel(wl_col)
    ax.plot(
        manual_df[dt_col],
        manual_df[wl_col],
        marker="o",
        mec="k",
        mfc="none",
        label="Manually-dipped",
        lw=0.5,
        mew=0.3,
        color="k",
        ls=":",
        ms=2,
    )
    if zoom_buffer is None:
        zoom_buffer = timedelta(days=30)
    elif zoom_buffer is False:
        zoom_buffer = timedelta(seconds=1)
    if len(logger_df):
        if zoom_to == "logger":
            ax.set_xlim(
                logger_df[dt_col].min() - zoom_buffer,
                logger_df[dt_col].max() + zoom_buffer,
            )
        elif zoom_to == "since-logger":
            ax.set_xlim(logger_df[dt_col].min() - zoom_buffer, None)
    ax.legend(loc="best", fontsize="small")
    return ax


def plot_wl_trend(
    wls,
    trend_wls,
    trend_lines=None,
    trend_line_start=None,
    trend_line_end=None,
    all_wls=None,
    well_id_col="well_id",
    well_title_col="well_id",
    dt_col="obs_date",
    wl_col="rswl",
    hist_min_date_col="rswl_min_date",
    ax=None,
    ms=5,
    year_span=12,
    override_year_span=False,
):
    """Plot water level trend.

    Args:
        wls (pd.DataFrame):
        trend_wls (pd.DataFrame):
        trend_lines (?):
        trend_line_start (?):
        trend_line_end (?):
        all_wls (pd.DataFrame, optional):
        well_id_col (str): column with the well identifier
        well_title_col (str): column with the well title
        dt_col (str): column(s) containing dates
        wl_col (str): column containing water levels - either 'rswl', 'swl', or 'dtw'
        hist_min_date_col (str): TODO
        ax (matplotlib.pyplot.Axes)
        ms (int)
        year_span (int)
        override_year_span (?)

    Returns:
        :class:`matplotlib.pyplot.Axes`: axes object

    .. todo:: Document plot_wl_trend function, add example code and figure

    """
    well_id = wls[well_id_col].unique()[0]
    if ax is None:
        fig = plt.figure(figsize=(8, 3))
        ax = fig.add_subplot(111)
    if all_wls is not None:
        ax.plot(
            all_wls[dt_col],
            all_wls[wl_col],
            lw=0.5,
            marker="o",
            ms=ms - 2,
            mew=0.2,
            mec="grey",
            mfc="grey",
            color="grey",
            alpha=0.2,
            label="All data",
        )
    lw = 0.5
    ax.plot(
        wls[dt_col],
        wls[wl_col],
        color="#222222",
        lw=lw,
        marker="o",
        mfc="orange",
        mec="gray",
        ms=ms - 1,
        mew=0.3,
        alpha=0.5,
        label="Annual recovered WL",
    )
    ax.plot(
        trend_wls[dt_col],
        trend_wls[wl_col],
        marker="o",
        mfc="red",
        mec="k",
        ms=ms,
        mew=0.3,
        lw=0,
        alpha=0.7,
        label="Used for trend calculation",
    )
    hist_idx = wls[dt_col] == trend_wls[hist_min_date_col].iloc[0]
    ax.plot(
        wls[hist_idx][dt_col],
        wls[hist_idx][wl_col],
        marker="o",
        mec="purple",
        mfc="none",
        mew=0.5,
        ms=ms + 5,
        ls="none",
        label="Historical minimum",
    )

    if trend_lines is not None:
        trend_line = trend_lines.loc[well_id]
        trend_line_ts = [trend_line_start, trend_line_end]
        trend_line_wls = calculate_trendline_at_dates(trend_line, trend_line_ts)
        ax.plot(trend_line_ts, trend_line_wls, lw=1, color="r", label="Linear trend")
        end_ts = trend_line_ts[1]
        fg, bg = status_to_colours(trend_line.status_change, param="WL")
        trend_label = f": {trend_line.status_change} at {trend_line.slope_yr:.2f} m/y"
    else:
        end_ts = pd.Timestamp(trend_wls[dt_col].max())
        fg = "black"
        bg = "white"

    start_ts = end_ts - timedelta(days=365.25 * year_span)
    if override_year_span:
        hist_min_ts = trend_wls[hist_min_date_col].iloc[0] - timedelta(days=120)
        if hist_min_ts < start_ts:
            start_ts = hist_min_ts
    ax.set_xlim(start_ts, end_ts + timedelta(days=120))
    leg = ax.legend(loc="best", fontsize="small", frameon=False)
    if year_span <= 15:
        ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.set_ylabel(wl_col)
    title_text = ax.set_title(
        f"{wls[well_title_col].iloc[0]}{trend_label}",
        color=fg,
        backgroundcolor=bg,
        fontsize="medium",
    )
    if all_wls is not None:
        lim_wls_whole = all_wls
    else:
        lm_wls_whole = wls
    lim_wls = lim_wls_whole[
        (lim_wls_whole[dt_col] >= start_ts) & (lim_wls_whole[dt_col] <= end_ts)
    ][wl_col]
    yspan = lim_wls.max() - lim_wls.min()
    y0 = lim_wls.min() - yspan * 0.1
    y1 = lim_wls.max() + yspan * 0.1
    if wl_col == "rswl":
        ax.set_ylim(y0, y1)
    else:
        ax.set_ylim(y1, y0)

    ax._title_text = title_text
    return ax


def plot_wl_rankings_internal(curr_ranks, title=""):
    """Plot bar chart of WL rankings for internal use.

    Args:
        curr_ranks (DataFrame): e.g. from
            `resource.read_data("recovery_wl_data", "current ranked WLs")
        title (str): chart title e.g. resource_key

    Returns:
        :class:`matplotlib.pyplot.Figure`: figure object

    The figure shows the number and percent of wells for each
    BoM class in both bar chart and stacked bar chart form,
    with the median well's class indicated on the figure.

    .. todo:: Add example code and figure for plot_wl_rankings_internal

    """

    bcmap = BoMClassesColormap()
    bom_keys = bcmap.class_names
    class_counts = bom_classes_dict()
    class_counts.update(curr_ranks.rswl_bom_class.value_counts().to_dict())

    fig = plt.figure(figsize=(6, 3))
    gs = gridspec.GridSpec(1, 2, width_ratios=(5, 2))
    ax = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    bc_range = [i for i in range(len(bom_keys))]
    bc_counts = [class_counts[x] for x in bom_keys]
    ax.barh(bc_range, bc_counts, color=bcmap.colours_rgba(1), edgecolor="k", lw=0.8)
    ax.set_yticks(range(len(bcmap.labels)))
    _ = ax.set_yticklabels(bcmap.labels, fontsize="small")
    label_ypos = np.asarray(bc_counts) + (max(bc_counts) / 30)
    percentage_counts = [y / sum(bc_counts) * 100 for y in bc_counts]
    percentage_labels = [
        f"{pct:.0f}" for pct in round_to_100_percent(percentage_counts, 0)
    ]
    bottom = 0
    for i in range(len(bc_range)):
        if bc_counts[i] > 0:
            ax.text(
                label_ypos[i],
                bc_range[i],
                f"{bc_counts[i]} wells ({percentage_labels[i]}%)",
                va="center",
                ha="left",
                color="#222222",
                fontsize="small",
            )
        ax2.bar(
            [1],
            [percentage_counts[i]],
            bottom=bottom,
            facecolor=bcmap.class_to_rgba(bom_keys[i]),
            edgecolor="k",
            lw=0.5,
        )
        bottom += percentage_counts[i]
    ax.set_xlabel("Number of wells", fontsize="medium")
    y0, y1 = ax.get_xlim()
    ax.xaxis.set_major_locator(
        mticker.MaxNLocator(nbins="auto", steps=[1, 2, 5, 10], integer=True)
    )
    ax.set_xlim(0, y1 + np.ceil((max(bc_counts) / 30)))
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    for sp in ["top", "bottom", "left"]:
        ax2.spines[sp].set_visible(False)
    ax2.tick_params(
        axis="y",
        left=False,
        labelleft=False,
        right=True,
        labelright=True,
    )
    ax2.set_xticks([])
    ax2.set_xlim(0, 1.5)
    ax2.set_ylim(-0.5, 100)
    ax2.set_ylabel(
        f"Percentage of wells ({sum(bc_counts)} wells in total)", fontsize="small"
    )
    ax2.yaxis.set_label_position("right")
    median_ranking = get_median_ranking(curr_ranks["rswl_bom_class"])
    ax2.annotate(
        f"Median well: {median_ranking}",
        (1.4, 50),
        (0.4, 50),
        arrowprops=dict(arrowstyle="->", color="k"),
        color="k",
        rotation=90,
        ha="right",
        va="center",
        fontsize="small",
    )

    ax.set_title(title, fontsize="medium")
    fig.tight_layout()
    return fig


def plot_wl_historical_rankings(ranks, qc, title="", figsize=None):
    """Plot historical recovered WLs

    Args:
        ranks (pd.DataFrame): all ranked WLs
        qc (pd.DataFame): data quality table
        title (str)
        figsize (tuple): width, height in inches

    Returns:
        :class:`matplotlib.pyplot.Figure`: matplotlib Figure

    """
    figsize_override = {}

    # curr_wells = ranks[ranks.obs_date.dt.year == 2019].well_id.unique()
    # ranks = ranks[ranks.well_id.isin(curr_wells)]

    year_min = ranks.season_year.str[:4].astype(int).min()
    year_max = ranks.season_year.str[:4].astype(int).max()
    years = np.arange(year_min, year_max + 1, step=1)
    ncols = len(years)
    year_labels = []
    for i in range(ncols):
        if i < len(years):
            year_labels.append(f"{years[i]:.0f}")
        else:
            year_labels.append("")

    unsorted_well_ids = ranks.well_id.unique()
    sort_records = []
    for w in unsorted_well_ids:
        qc_condition = qc[qc.well_id == w].all_conditions.iloc[0]
        years_data = len(
            ranks[ranks.well_id == w].season_year.str[:4].astype(int).unique()
        )
        sort_records.append(
            {"well_id": w, "qc_condition": qc_condition, "years_data": years_data}
        )
    sort_records = (
        pd.DataFrame(sort_records)
        .sort_values(["qc_condition", "years_data"], ascending=False)
        .reset_index(drop=True)
    )

    well_ids = sort_records.well_id.values
    qc_false = sort_records[sort_records.qc_condition == False].index
    if len(qc_false):
        false_condition = qc_false[0]
    else:
        false_condition = np.nan
    n_wells = len(well_ids)

    bcmap = BoMClassesColormap()
    ranks_arr = np.empty((n_wells, ncols), dtype=int)
    for i, well_id in enumerate(well_ids):
        for j in range(ncols):
            if j < len(years):
                year = years[j]
            ranking = None
            ranks_subset = ranks[
                (ranks.well_id == well_id)
                & (ranks.season_year.str[:4].astype(int) == year)
            ]
            if len(ranks_subset):
                ranking = ranks_subset.iloc[0].rswl_bom_class
                short_ranking = bcmap.class_names.index(ranking)
            else:
                short_ranking = -1
            ranks_arr[i, j] = short_ranking

    logger.debug(f"Number of wells: {len(well_ids)}")
    logger.debug(f"Number of years: {len(years)} ({year_min} to {year_max})")

    if figsize is None:
        figsize = (len(years) / 6.5, len(well_ids) / 5.6)
        logger.debug(f"Figure size in inches: {figsize}")
        if figsize[0] < 3.5:
            figsize = (3.5, figsize[1])
            logger.debug(f"Overriding figure width. figsize now {figsize}")
        if figsize[1] < 4:
            figsize = (figsize[0], 4)
            logger.debug(f"Overriding figure height. figsize now {figsize}")

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.imshow(ranks_arr, cmap=bcmap.cmap_nodata)

    yts = ax.set_yticks(range(n_wells))
    ytls = ax.set_yticklabels(well_ids, fontsize="xx-small")
    ax.tick_params(
        "y", which="major", left=True, right=True, labelleft=True, labelright=True
    )

    xts = ax.set_xticks(range(len(year_labels)))
    xtls = ax.set_xticklabels(year_labels, fontsize="x-small", rotation=90, ha="center")
    ax.tick_params(
        "x", which="major", bottom=True, top=True, labelbottom=True, labeltop=True
    )

    ax.axhline(false_condition - 0.5, color="green", lw=1)
    for year in years:
        if year % 10 == 0:
            year_label = f"{year:.0f}"
            if year_label in year_labels:
                dashes = (1, 0)
                if year_label == "2000":
                    lw = 1
                    ls = "-"
                elif year_label == "2010":
                    lw = 1
                    ls = "--"
                    dashes = (10, 3)
                else:
                    lw = 0.5
                    ls = ":"
                ax.axvline(
                    year_labels.index(year_label) - 0.5,
                    color="black",
                    lw=lw,
                    ls=ls,
                    dashes=dashes,
                )

    ax.set_xticks(np.arange(-1, len(year_labels)) + 0.5, minor=True)
    ax.set_yticks(np.arange(-1, n_wells) + 0.5, minor=True)
    ax.grid(True, which="minor", axis="both", lw=0.2, color="grey")
    ax.tick_params("x", which="minor", bottom=False)
    ax.tick_params("y", which="minor", left=False)
    ax.set_title(title)
    ax.grid(False)
    fig.tight_layout()
    return fig


def plot_wl_trends_internal(wltrends, title=""):
    return plot_trends_internal(
        wltrends,
        title=title,
        class_names=("Declining", "Stable", "Rising"),
        param_yaxis_label="m/y",
        param_col="slope_yr",
    )


def plot_wl_ranking_classes(curr_ranks, ax=None):
    """Plot_wl_ranking_classes

    Args:
        curr_ranks (?)

    Returns:
        :class:`matplotlib.pyplot.Axes`: axes

    .. todo::

        Document the plot_wl_ranking_classes function. This is
        the one that goes into the Tech Note.

    """
    bcmap = BoMClassesColormap()
    bom_keys = bcmap.class_names
    class_counts = bom_classes_dict()
    class_counts.update(curr_ranks.rswl_bom_class.value_counts().to_dict())
    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    bc_range = [i for i in range(len(bom_keys))]
    bc_counts = [class_counts[x] for x in bom_keys]
    ax.barh(bc_range, bc_counts, color=bcmap.colours_rgba(1), edgecolor="k")
    ax.set_yticks(range(len(bcmap.labels)))
    _ = ax.set_yticklabels(bcmap.labels, fontsize="small")
    label_ypos = np.asarray(bc_counts) + (max(bc_counts) / 30)
    percentage_counts = [y / sum(bc_counts) * 100 for y in bc_counts]
    percentage_labels = [
        f"{pct:.0f}" for pct in round_to_100_percent(percentage_counts, 0)
    ]
    for i in range(len(bc_range)):
        if bc_counts[i] > 0:
            ax.text(
                label_ypos[i],
                bc_range[i],
                percentage_labels[i] + "%",
                va="center",
                ha="left",
                color="#555555",
            )
    ax.set_xlabel("Number of wells", fontsize="medium")
    y0, y1 = ax.get_xlim()
    ax.xaxis.set_major_locator(
        mticker.MaxNLocator(nbins="auto", steps=[1, 2, 5, 10], integer=True)
    )
    ax.set_xlim(0, y1 + np.ceil((max(bc_counts) / 30)))
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)

    return ax


def plot_wl_ranking_map(
    curr_ranks,
    map_elements,
    map_annotations,
    ax=None,
    leg_frame=True,
    map_crs=8059,
    leg_loc="lower right",
    markersize=45,
):
    """plot_wl_ranking_map

    Args:
        curr_ranks
        map_elements
        map_annotations
        ax
        leg_frame (bool)
        map_crs (int)
        leg_loc (str)
        markersize (int)

    Returns:
        :class:`matplotlib.pyplot.Axes`: axes

    .. todo::

        Document the plot_wl_ranking_map function. This is
        the one that goes into the Tech Note.

    """
    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    for spine in ax.spines.values():
        spine.set_visible(False)

    bcmap = BoMClassesColormap()
    bom_keys = bcmap.class_names

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
    for bom_class in bom_keys[::-1]:
        dfg = curr_ranks[curr_ranks["rswl_bom_class"] == bom_class]
        if len(dfg):
            easting, northing = tr.transform(dfg.longitude.values, dfg.latitude.values)
            ax.scatter(
                easting,
                northing,
                marker="o",
                color=bcmap.class_to_rgba(bom_class),
                edgecolor="#555555",
                linewidth=0.3,
                s=markersize,
                zorder=5,
            )

    for ann in map_annotations:
        logger.debug(f"annotating map with {ann}")
        if ann["well_id"] in curr_ranks.well_id.unique():
            row = curr_ranks[curr_ranks.well_id == ann["well_id"]].iloc[0]
            label = ann.get("label", ann["well_id"])
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
            easting, northing = tr.transform(row.longitude, row.latitude)
            ax.annotate(
                label,
                (easting, northing),
                (
                    easting + ann.get("x_km", 0) * 1000,
                    northing + ann.get("y_km", 0) * 1000,
                ),
                color="#444444",
                fontsize="x-small",  # map annotation
                ha=ann.get("ha", "left"),
                va=ann.get("va", "bottom"),
                arrowprops=arrowprops,
                zorder=6,
            )
        else:
            logger.debug(f"{ann['well_id']} not found in {curr_ranks.well_id.unique()}")
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


def plot_wl_trend_triclass_bars(wl_trend_df, ax=None):
    """todo

    Args:
        wl_trend_df (pd.DataFrame)
        ax

    Returns:
        :class:`matplotlib.pyplot.Axes`: Axes object

    """
    gsr_colours = status_change_colours
    gsr_colours_rgba = {
        k: np.asarray([x / 255 for x in rgb] + [1]) for k, rgb in gsr_colours.items()
    }
    status_key_x = [0, 1, 2]
    status_keys = ["Rising", "Stable", "Declining"]
    status_values = [
        len(wl_trend_df[wl_trend_df.status_change == v]) for v in status_keys
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
    ax.set_yticklabels(status_keys)
    ax.set_ylim(status_key_x[-1] + 1, status_key_x[0] - 1)

    label_ypos = np.asarray(status_values) + (max(status_values) / 30)
    percentage_counts = [y / sum(status_values) * 100 for y in status_values]
    percentage_labels = [
        f"{pct:.0f}" for pct in round_to_100_percent(percentage_counts, 0)
    ]
    for i, x in enumerate(status_key_x):
        if percentage_counts[i] > 0:
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
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True, steps=[1, 2, 5, 10]))

    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    return ax


def plot_wl_trend_triclass_map(
    wl_trend_df,
    map_elements,
    map_annotations,
    ax=None,
    leg_frame=True,
    map_crs=8059,
    leg_loc="lower right",
    markersize=60,
):
    wl_trend_map_markers = {"Rising": "^", "Stable": "s", "Declining": "v"}

    if ax is None:
        fig = plt.figure(figsize=(3.6, 2.8))
        ax = fig.add_subplot(111)

    for spine in ax.spines.values():
        spine.set_visible(False)

    gsr_colours = status_change_colours
    gsr_colours_rgba = {
        k: np.asarray([x / 255 for x in rgb] + [1]) for k, rgb in gsr_colours.items()
    }

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
    for trend_label in ["Rising", "Stable", "Declining"]:
        dfg = wl_trend_df[wl_trend_df.status_change == trend_label]
        if len(dfg):
            easting, northing = tr.transform(dfg.longitude.values, dfg.latitude.values)
            ax.scatter(
                easting,
                northing,
                marker=wl_trend_map_markers[trend_label],
                color=gsr_colours_rgba[trend_label],
                edgecolor="#555555",
                linewidth=0.3,
                s=markersize,
                zorder=5,
            )

    logger.debug(f"wl_trend_df: \n{wl_trend_df}")

    for ann in map_annotations:
        logger.debug(f"Charting annotation: {ann}")
        if ann["well_id"] in wl_trend_df.well_id.unique():
            row = wl_trend_df[wl_trend_df.well_id == ann["well_id"]].iloc[0]
            label = ann.get("label", ann["well_id"])
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
            easting, northing = tr.transform(row.longitude, row.latitude)
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
        else:
            logger.debug(
                f" > did not find {ann['well_id']} in {wl_trend_df.well_id.unique()}"
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
