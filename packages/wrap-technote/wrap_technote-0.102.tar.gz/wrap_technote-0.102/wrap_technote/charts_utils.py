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


logger = get_logger()


def apply_technote_chart_style():
    # plt.style.use("ggplot")
    # plt.rcParams["axes.facecolor"] = "white"
    # plt.rcParams["axes.edgecolor"] = "#555555"
    plt.rcParams["figure.dpi"] = 150
    # plt.rcParams["font.family"] = "Segoe UI"
    # plt.rcParams["hatch.linewidth"] = 0.5
    plt.rcParams["figure.max_open_warning"] = 100


def convert_colour_format(cf, from_fmt, to_fmt, **kwargs):
    if from_fmt.startswith("rgb255"):
        if to_fmt.startswith("rgb1"):
            return rgb255_to_rgb1a(*cf, **kwargs)
        elif to_fmt.startswith("rgb255"):
            return rgb255_to_rgb255a(*cf, **kwargs)
        elif to_fmt == "hex":
            cf2 = rgb255_to_rgb1a(*cf, **kwargs)
            return rgba1_to_hex(*cf2, **kwargs)
    elif from_fmt.startswith("rgb1"):
        if to_fmt.startswith("rgb255"):
            return rgb1_to_rgb255a(*cf, **kwargs)
        elif to_fmt.startswith("rgb1"):
            return rgb1_to_rgb1a(*cf, **kwargs)
        elif to_fmt == "hex":
            return rgba1_to_hex(*cf, **kwargs)


def rgb255_to_rgb1a(r, g, b, a=255, auto_convert_alpha=True):
    """Convert RGBA values from 0 to 255.

    Args:
        r (float): red fraction from 0 to 255
        g (float): green fraction from 0 to 255
        b (float): blue fraction from 0 to 255
        a (float): alpha % from 0 to 255 or 0 to 1
        auto_convert_alpha (bool): if a <= 0 convert that fraction between 0 and 1
            into one between 0 and 255.

    Returns: r, g, b, a (tuple of floats between 0 and 1)

    """
    if a < 1:
        a *= 255
    elif a == 1:
        a = 255
    return (r / 255, g / 255, b / 255, a / 255)


def rgb1_to_rgb255a(r, g, b, a=1, alpha_as=255):
    """Convert RGBA values from 0-1 to 0-255.

    Args:
        r (float): red fraction from 0 to 1
        g (float): green fraction from 0 to 1
        b (float): blue fraction from 0 to 1
        a (float): alpha % from 0 to 255 or 0 to 1
        alpha_as (int): if 255, return alpha between 0 and 255; if 1, return alpha
            between 0 and 1

    Returns: r, g, b, a (tuple of floats between 0 and 255)

    """
    return (r * 255, g * 255, b * 255, a * alpha_as)


def rgb1_to_rgb1a(r, g, b, a=1):
    """Ensure an alpha value.

    Args:
        r (float): red fraction from 0 to 1
        g (float): green fraction from 0 to 1
        b (float): blue fraction from 0 to 1
        a (float, optional): alpha % from 0 to 1

    Returns: r, g, b, a (tuple of floats between 0 and 1)

    """
    return r, g, b, a


def rgb255_to_rgb255a(r, g, b, a=255):
    """Ensure an alpha value.

    Args:
        r (float): red fraction from 0 to 255
        g (float): green fraction from 0 to 255
        b (float): blue fraction from 0 to 255
        a (float, optional): alpha % from 0 to 255

    Returns: r, g, b, a (tuple of floats between 0 and 255)

    """
    return r, g, b, a


def rgba1_to_hex(r, g, b, a=1):
    """Convert RGBA (0-1) to a hexadecimal code.

    Args:
        r (float): red fraction from 0 to 1
        g (float): green fraction from 0 to 1
        b (float): blue fraction from 0 to 1
        a (float, optional): alpha % from 0 to 1

    Returns: string of hex code beginning with "#"

    """
    h = lambda v: hex(int(v * 255))[-2:]
    return f"#{h(r)}{h(g)}{h(b)}"


status_change_colours = {
    "Rising": (0, 176, 240),
    "Stable": (0, 176, 80),
    #     "Declining": (255, 255, 0), # original ArcMAP GSR colour (yellow)
    "Declining": (254, 178, 76),
    "Decreasing": (0, 176, 240),  # Salinity
    "Increasing": (254, 178, 76),  # Salinity
}
"""RGB (0 to 255) tuples for each of the possible values that "status_change" can take.

"""

wl_status_change_colours = [
    rgb255_to_rgb1a(*status_change_colours[c]) for c in wl_status_changes
]
"""RGB (0 to 255) tuples for each of the possible values that "status_change" can take
for WL data.

"""

tds_status_change_colours = [
    rgb255_to_rgb1a(*status_change_colours[c]) for c in tds_status_changes
]
"""RGB (0 to 255) tuples for each of the possible values that "status_change" can take
for TDS data.

"""


extract_method_lut = {
    "AIRL": "Air Lift",
    "BAIL": "Bailer",
    "BUCK": "Bucket",
    "EST": "Estimated",
    "FLOW": "Flow",
    "HAND": "Hand",
    "PUMP": "Pump",
    "UKN": "Unknown",
    "WMLL": "Windmill",
    "GRAB": "Grab",
    "?": "?",
}
"""Explanatory description for the "extract_method" values for TDS data.

"""

measured_during_lut = {
    "A": "Aquifer Test",
    "D": "Drilling",
    "F": "Field Survey",
    "S": "Final Sample on drilling completion",
    "G": "Geophysical Logging",
    "L": "Landowner Sample",
    "M": "Monitoring",
    "R": "Rehabilitation",
    "U": "Unknown",
    "W": "Well Yield",
    "?": "?",
}
"""Explanatory description for the "measured_during" values for TDS data.

"""

extract_method_markers = {
    "AIRL": "$a$",
    "BAIL": "v",
    "BUCK": ">",
    "EST": "$?$",
    "FLOW": "P",
    "HAND": "<",
    "PUMP": "o",
    "UKN": ".",
    "WMLL": "o",
    "GRAB": "<",
    "?": ".",
}
"""matplotlib marker shape codes for the "extract_method" values for TDS data.

"""

meas_during_colours = {
    "M": "tab:cyan",  # 'Monitoring',
    "F": "tab:blue",  # 'Field Survey',
    "A": "tab:green",  # 'Aquifer Test',
    "W": "tab:olive",  # 'Well Yield',
    "L": "tab:pink",  # 'Landowner Sample',
    "G": "tab:purple",  # 'Geophysical Logging',
    "D": "tab:red",  # 'Drilling',
    "S": "tab:orange",  # 'Final Sample on drilling completion',
    "R": "tab:brown",  # 'Rehabilitation',
    "U": "tab:gray",  # 'Unknown',
    "?": "black",  # '?'
}
"""matplotlib string colours for the "measured_during" values for TDS data.

"""

removal_reason_colours = [
    "rosybrown",
    "coral",
    "peru",
    "orange",
    "darkgoldenrod",
    "tan",
    "darkkhaki",
    "olive",
    "yellowgreen",
    "green",
    "darkslategray",
    "darkcyan",
    "lightslategrey",
    "darkblue",
    "mediumorchid",
]
"""Sequence of matplotlib string colours for multiple removal reasons for data validation
figures.

"""


season_colours = {
    "0-summer": "sandybrown",
    "summer": "sandybrown",
    "1-autumn": "khaki",
    "autumn": "khaki",
    "2-winter": "deepskyblue",
    "winter": "deepskyblue",
    "3-spring": "yellowgreen",
    "spring": "yellowgreen",
}
"""Matplotlib string colours for the seasons.

"""


rainfall_colours = {"rainfall": (0 / 255, 176 / 255, 240 / 255, 1), "mean": "#bebebe"}
"""RGBA (0 to 1) tuple for the rainfall data figures, and a hex colour for the average
rainfall line.

"""


def adjust_lightness(color, amount=0.5):
    """Adjust colour to be lighter or darker.

    https://stackoverflow.com/a/49601444

    """
    import matplotlib.colors as mc
    import colorsys

    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def wrap(s, width=20, chars=("=", "-")):
    """Wrap a string."""
    if s is None:
        s = ""
    for char in chars:
        for prefix in (" ", ""):
            for suffix in ("", " "):
                s = s.replace(f"{prefix}{char}{suffix}", char)
    return "\n".join(textwrap.wrap(s, width=width))


class MonthlyColormap:
    """Define a circular colour mapping for the months of the year.

    Args:
        cmap (matplotlib Colormap, optional): suggested to use a
            circular one.
        rot (int): integer between 0 and 12 to rotate it by so that
            the seasons make sense

    Attributes:
        cmap (:class:`matplotlib.colors.ListedColormap`): the name of the
            colormap is "monthly_cmap"
        norm (:class:`matplotlib.colors.Normalize`)
        mappable (:class:`matplotlib.pyplot.cm.ScalarMappable`)

    """

    def __init__(self, cmap=None, rot=None):
        if cmap is None:
            cmap = plt.cm.get_cmap("twilight")
            rot = 7
        if rot is None:
            rot = 0
        colours = [cmap(((x + rot) / 12) % 1) for x in range(12)]
        self.cmap = mcolors.ListedColormap(colours, name="monthly_cmap")
        self.norm = mcolors.Normalize(1, 12)
        self.mappable = plt.cm.ScalarMappable(norm=self.norm, cmap=self.cmap)
        self.mappable.set_array([])


class BoMClassesColormap:
    """Define a colour mapping for the BoM percentile classes.

        .. figure:: figures/BoM_deciles.png

    Args:
        wrap_labels (bool): wrap the BoM descriptions on "much"

    Attributes:
        cmap (:class:`matplotlib.colors.ListedColormap`): the name of the
            colormap is "monthly_cmap"
        norm (:class:`matplotlib.colors.Normalize`)
        mappable (:class:`matplotlib.pyplot.cm.ScalarMappable`)

    """

    # This is from the State of the Climate 2018 report:
    # colours = [
    #     (239, 84, 45),    # 0: Lowest on record
    #     (255, 193, 85),   # 1: Very much below average
    #     (255, 233, 170),  # 2: Below average
    #     (255, 255, 255),  # 3: Average
    #     (158, 225, 223),  # 4: Above average
    #     (87, 208, 221),   # 5: Very much above average
    #     (11, 118, 169),   # 6: Highest on record
    # ]

    #: RGB (0 to 255) tuples for the seven class codes:
    colours = [
        (178, 24, 43),  # 0: Lowest on record
        (239, 138, 98),  # 1: Very much below average
        (253, 219, 199),  # 2: Below average
        (247, 247, 247),  # 3: Average
        (209, 229, 240),  # 4: Above average
        (103, 169, 207),  # 5: Very much above average
        (33, 102, 172),  # 6: Highest on record
    ]

    #: RGB (0 to 255) tuples for eight class codes (i.e. index 0 -> code "no data").
    colours_nodata = [
        (120, 120, 120),
    ] + colours  # -1: not applicable

    #: The names of each of the BoM classifications
    class_names = [
        "Lowest on record",
        "Very much below average",
        "Below average",
        "Average",
        "Above average",
        "Very much above average",
        "Highest on record",
    ]

    #: foreground colours for each BoM class name
    foreground_colours = ["white", "white", "white", "black", "black", "white", "white"]

    #: foreground colours for each BoM class name (version 2... ?)
    foreground_colours_2 = [
        "white",
        "black",
        "black",
        "black",
        "black",
        "black",
        "white",
    ]

    @property
    def hexdict(self):
        """Dictionary of hex colour codes for each class name."""
        return {c: rgba1_to_hex(*self.class_to_rgba(c)) for c in self.class_names}

    def __init__(self, wrap_labels=True):
        self.cmap = mcolors.ListedColormap(self.colours_1, name="bom_cmap")
        self.norm = mcolors.Normalize(0, 6)
        self.mappable = plt.cm.ScalarMappable(norm=self.norm, cmap=self.cmap)
        self.mappable.set_array([])
        self.wrap_labels = wrap_labels

        #: A version of the colourmap including a "nodata" value.
        self.cmap_nodata = mcolors.ListedColormap(
            self.colours_nodata_1, name="bom_cmap2"
        )
        #: A matplotlib Normalize instance of the colourmap including a "nodata" value.
        self.norm_nodata = mcolors.Normalize(0, 7)
        #: A matplotlib ScalarMappable for the colourmap including a "nodata" value.
        self.mappable_nodata = plt.cm.ScalarMappable(
            norm=self.norm_nodata, cmap=self.cmap_nodata
        )
        self.mappable_nodata.set_array([])
        self.wrap_labels = wrap_labels

    @property
    def colours_1(self):
        """List of RGB (0 to 1) tuples for each BoM class."""
        return [tuple([x / 255 for x in rgb]) for rgb in self.colours]

    @property
    def colours_nodata_1(self):
        """List of RGB (0 to 1) tuples for each BoM class (including nodata as 0)."""
        return [tuple([x / 255 for x in rgb]) for rgb in self.colours_nodata]

    def colours_rgba(self, alpha=1):
        """Add alpha to the RGB colours.

        Args:
            alpha (float): between 0 and 1, opacity (1 == opaque, 0 = transparent)

        Returns: list of (r, g, b, a) tuples for all the classes (rgba between 0 and 1)

        """
        return [tuple([x / 255 for x in rgb] + [alpha]) for rgb in self.colours]

    def class_to_rgba(self, bom_class, alpha=1):
        """Transform a BoM class name e.g. "Lowest on record" to an RGBA tuple.

        Args:
            bom_class (str): one of the BoM class definitions
            alpha (float): between 0 (transparent) and 1 (opaque)

        Returns: (r, g, b, a) tuple (between zero and one)

        """
        if bom_class == "No data":
            return self.colours_nodata_1[0]
        idx = self.class_names.index(bom_class)
        return self.colours_rgba(alpha=alpha)[idx]

    def class_to_foreground_colour(self, bom_class):
        """Transform a BoM class name e.g. "Lowest on record" to a foreground colour.

        Args:
            bom_class (str): one of the BoM class definitions

        Returns: str (matplotlib colour)

        """
        idx = self.class_names.index(bom_class)
        return self.foreground_colours[idx]

    def class_to_foreground_colour_2(self, bom_class):
        """Transform a BoM class name e.g. "Lowest on record" to a foreground colour.

        Args:
            bom_class (str): one of the BoM class definitions

        Returns: str (matplotlib colour)

        """
        idx = self.class_names.index(bom_class)
        return self.foreground_colours_2[idx]

    @property
    def labels(self):
        """Wrap labels (if required) on the word 'much' for the class names."""
        labels = [
            "Lowest on record",
            "Very much below average",
            "Below average",
            "Average",
            "Above average",
            "Very much above average",
            "Highest on record",
        ]
        if self.wrap_labels:
            return [l.replace("much ", "much\n") for l in labels]
        else:
            return labels

    @property
    def labels_nodata(self):
        """Wrap labels (if required) on the word 'much' for the class names (including
        nodata value).

        """
        labels = [
            "No data",
            "Lowest on record",
            "Very much below average",
            "Below average",
            "Average",
            "Above average",
            "Very much above average",
            "Highest on record",
        ]
        if self.wrap_labels:
            return [l.replace("much ", "much\n") for l in labels]
        else:
            return labels

    def plot_legend(self, cax, cbar_labels=None, nodata=False, **kwargs):
        """Plot legend into an Axes.

        Args:
            cax (matplotlib Axes): axes to fill with a legend.

        Returns: matplotlib Colorbar object.

        """
        # fig = plt.figure()
        if nodata:
            cmap = self.cmap_nodata
        else:
            cmap = self.cmap
        cset = cax.scatter([], [], c=[], cmap=cmap)
        cbar = plt.colorbar(cset, cax=cax, **kwargs)
        self.fix_ticklabels(cbar, cbar_labels=cbar_labels, nodata=nodata)
        return cbar

    def fix_ticklabels(self, cbar, wrap_labels=None, cbar_labels=None, nodata=False):
        """Fix colorbar ticks and labels.

        Args:
            cbar (:class:`matplotlib.Colorbar`)
            wrap_labels (bool)

        """
        if wrap_labels is None:
            wrap_labels = self.wrap_labels
        c0, c1 = cbar.mappable.get_clim()
        cbar_ticks = []

        if nodata:
            cbar_divisions = 8
        else:
            cbar_divisions = 7
        cbar_step = (c1 - c0) / cbar_divisions
        if not cbar_labels:
            cbar_labels = []
            make_cbar_labels = True
        else:
            make_cbar_labels = False
        for i, value in enumerate(range(0, cbar_divisions)):
            if make_cbar_labels:
                cbar_labels.append(self.labels[i])
            cbar_ticks.append(((cbar_step * i) + c0) + (cbar_step / 2))
        cbar.set_ticks(cbar_ticks)
        cbar.set_ticklabels(cbar_labels)


def fix_ticklabels(cbar, cbar_labels=None):
    c0, c1 = cbar.mappable.get_clim()
    cbar_ticks = []
    if cbar_labels is None:
        cbar_labels = []
        make_labels = True
    else:
        make_labels = False
    cbar_divisions = len(cbar_labels)
    cbar_step = (c1 - c0) / cbar_divisions
    for i, value in enumerate(range(0, cbar_divisions)):
        if make_labels:
            cbar_labels.append(colours[i])
        cbar_ticks.append(((cbar_step * i) + c0) + (cbar_step / 2))
    cbar.set_ticks(cbar_ticks)
    cbar.set_ticklabels(cbar_labels)
    return cbar


def plot_colorbar(
    cax,
    colours,
    cbar_labels=None,
    split_cbar_labels_on="Very much",
    orientation="vertical",
):
    if split_cbar_labels_on:
        cbar_labels = [
            l.replace(split_cbar_labels_on, split_cbar_labels_on + "\n")
            for l in cbar_labels
        ]
    cmap = mcolors.ListedColormap(colours, name="custom_colours")
    cset = cax.scatter([], [], c=[], cmap=cmap)
    cbar = plt.colorbar(cset, cax=cax, orientation=orientation)
    cbar = fix_ticklabels(cbar, cbar_labels=cbar_labels)
    for axis in ["top", "bottom", "left", "right"]:
        cax.spines[axis].set_linewidth(0.2)
    return cbar


def trim_whitespace_from_image(fn, append=None, new_fn=None):
    fn = str(fn)
    if new_fn is None:
        new_fn = fn
    if append:
        root, ext = os.path.splitext(fn)
        new_fn = root + append + ext

    def trim(im):
        bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
        logger.debug(f"bg image: {bg}")
        diff = ImageChops.difference(im.convert("RGB"), bg)
        logger.debug(f"ImageChops.difference(im, bg): {diff}")
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        logger.debug(f"bbox() = {bbox}")
        if bbox:
            logger.debug(f"found bbox to trim: {bbox}")
            return im.crop(bbox)
        else:
            logger.debug("Warning! Did not find any whitespace margin to trim.")
            return im

    im = Image.open(fn)
    im = trim(im)
    im.save(new_fn)


def plot_internal_classes_for_aggregate_resources(dfs, class_names, colours, col):
    """Plot a summary stacked bar chart showing classes for aggregate resources.

    Args:
        dfs (dict): dict; keys are the aggregate resource keys (really they are
            just labels for the x axis on the chart); keys should be a pandas
            DataFrame in each case.
        class_names (list): names for each class e.g. the "Decreasing", "Stable",
            "Increasing". They should be ordered such as will appear on the chart
            from bottom to top.
        colours (list): RGBA tuple colours for each class.
        col (str): column for *dfs* to extract the class value. The number of rows
            with a given value will be used to determine the height of each
            stacked bar segment.

    Returns: matplotlib Axes

    Examples follow below for Adelaide Plains:

        >>> import wrap_technote as tn
        >>> report = tn.load_report("Adelaide Plains", "2019-20")

    To do current WL rankings:

        >>> wlranks = report.get_aggregate_resources_data(
        ...     "WL", "recovery_wl_data", "current ranked WLs"
        ... )
        >>> bcmap = tn.BoMClassesColormap()
        >>> tn.plot_internal_classes_for_aggregate_resources(
        ...     wlranks, bcmap.class_names, bcmap.colours_rgba(), col="rswl_bom_class"
        ... )

    Five-year WL trends:

        >>> wltrends = report.get_aggregate_resources_data(
        ...     "WL", "recovery_wl_trends", "final trends"
        ... )
        >>> plot_internal_classes_for_aggregate_resources(
        ...     wltrends, wl_status_changes, wl_status_change_colours, col="status_change"
        ... )

    Five-year TDS trends:

        >>> tdstrends = report.get_aggregate_resources_data(
        ...     "TDS", "salinity_trends", "final trends"
        ... )
        >>> plot_internal_classes_for_aggregate_resources(
        ...     tdstrends,
        ...     tds_status_changes,
        ...     tds_status_change_colours,
        ...     col="status_change",
        ... )

    """
    pct_counts = {}
    raw_counts = {}
    labels = []
    across_all_counts = {c: 0 for c in class_names}
    for name, df in dfs.items():
        counts = {c: 0 for c in class_names}
        counts.update(df[col].value_counts().to_dict())
        for key, value in counts.items():
            across_all_counts[key] += value
        total_wells = sum(counts.values())
        if total_wells == 0:
            total_wells = np.nan
        pct_counts[name] = [counts[c] / total_wells * 100 for c in class_names]
        pct_counts[name] = round_to_100_percent(pct_counts[name])
        raw_counts[name] = [counts[c] for c in class_names]
        labels.append(name)

    width = (len(labels) + 1) * 1.4
    width_ratio_factor = 2.0
    fig = plt.figure(figsize=(width, 3.6))
    gs = gridspec.GridSpec(1, 2, width_ratios=(width * width_ratio_factor, 1))
    ax = fig.add_subplot(gs[0])
    cax = fig.add_subplot(gs[1])
    width = 0.3
    ax.axhline(50, lw=0.5, dashes=(20, 5), color="k", alpha=0.2)
    pct_counts_arr = np.array(list(pct_counts.values()))
    pct_counts_arr_cum = pct_counts_arr.cumsum(axis=1)
    n_wells = sum(across_all_counts.values())

    xlabels = [l.replace("_", "\n") + f"\n({sum(raw_counts[l])})" for l in labels]
    xticks = np.arange(len(xlabels))
    texts = []
    bars = []
    label_counts = np.zeros_like(xticks)

    for i, class_name in enumerate(class_names):
        colour = colours[i]
        heights = pct_counts_arr[:, i]
        starts = pct_counts_arr_cum[:, i] - heights
        bar = ax.bar(
            xticks,
            heights,
            bottom=starts,
            color=colour,
            width=width,
            linewidth=0.5,
            edgecolor="#555555",
        )
        bars += bar
        for j, label in enumerate(labels):
            category = pct_counts_arr[j, i]
            top = pct_counts_arr_cum[j, i]
            if category > 0:
                label_counts[j] += 1
                offset = width / 2 + 0.03
                ha = "left"
                if label_counts[j] % 2:
                    offset *= -1
                    ha = "right"
                text = ax.text(
                    j + offset,
                    top - (category / 2),
                    f"{pct_counts[label][i]:.0f}%\n({raw_counts[label][i]})",
                    color=adjust_lightness(colour, 0.5),
                    fontsize="small",
                    ha=ha,
                    va="center",
                    ma="center",
                )
                texts.append(text)
    cbar = plot_colorbar(cax, colours, cbar_labels=class_names)
    cbar.ax.tick_params(labelsize="small")
    ax.set_ylabel("Percentage of wells (number of wells)", fontsize="small")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center", fontsize="small")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.set_xlim(xticks[0] - 0.5, xticks[-1] + 0.5)
    ax.figure.tight_layout()
    return ax


def plot_trends_internal(
    trends, title, class_names, param_yaxis_label, param_col="slope_yr"
):
    """Plot bar chart of trend triclasses for internal use.

    Args:
        trends (DataFrame): e.g. from
            `resource.read_data("recovery_wl_trends", "final_trends")
        title (str): chart title e.g. resource_key

    Returns: matplotlib figure


    """

    class_colours = [rgb255_to_rgb1a(*status_change_colours[c]) for c in class_names]
    class_counts = {c: 0 for c in class_names}
    class_counts.update(trends.status_change.value_counts().to_dict())

    fig = plt.figure(figsize=(10, 4))
    gs = gridspec.GridSpec(1, 3, width_ratios=(10, 10, 1))
    ax = fig.add_subplot(gs[0])
    ax3 = fig.add_subplot(gs[1])
    ax2 = fig.add_subplot(gs[2])

    bc_range = [i for i in range(len(class_names))]
    bc_counts = [class_counts[x] for x in class_names]
    ax.barh(bc_range, bc_counts, color=class_colours, edgecolor="k", lw=0.8)
    ax.set_yticks(bc_range)
    _ = ax.set_yticklabels(class_names, fontsize="small")
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
            facecolor=class_colours[i],
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
    median_class = get_median_trend_triclass(
        trends["status_change"], classes=class_names
    )
    median_slope = trends[param_col].median()
    ax2.annotate(
        f"Median well: {median_class} at {median_slope:.2f} {param_yaxis_label}",
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

    ax3_class_names = [c for c in class_names if not c == "Stable"]
    xlabels = ["All\nwells"] + [f"{c}\nwells" for c in ax3_class_names]
    data_series = [trends[param_col]]
    for class_name in ax3_class_names:
        data_series.append(trends.loc[trends.status_change == class_name, param_col])
    data = ax3.boxplot(data_series)
    ax3.set_xticklabels(xlabels)
    ax3.set_ylabel(f"Trendline slope ({param_yaxis_label})")
    ax3.set_xlabel(
        "Box from 25 to 75th percentile\norange line = median", fontsize="small"
    )
    ax3.axhline(0, lw=0.5, color="b")

    fig.tight_layout()
    return fig
