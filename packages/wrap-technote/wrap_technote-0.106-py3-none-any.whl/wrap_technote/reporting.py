from datetime import datetime, timedelta, date
import importlib
import glob
import logging
from pathlib import Path
import os
import re
import sqlite3

import numpy as np
from jinja2 import Template, Environment, PackageLoader, select_autoescape
import pandas as pd

from .gwutils import *
from .utils import *

logger = get_logger()

CURRENT_RPERIOD = "2024-25"


increasing_codes = {"WL": "Rising", "TDS": "Increasing"}
"""Dictionary to map a parameter e.g. 'WL' to the word
used to describe what happens when it goes up ('Rising')."""

decreasing_codes = {"WL": "Declining", "TDS": "Decreasing"}
"""Dictionary to map a parameter e.g. 'WL' to the word
used to describe what happens when it goes down ('Declining')."""


ANNUAL_WRA_PATH = Path(
    r"R:\DFW_CBD\Projects\Projects_Science\Water Resource Assessments\Annual"
)
"""Path to the location where all reporting periods are kept."""

reporting_period_paths = {
    "2024-25": ANNUAL_WRA_PATH / "2024-25" / "Code",
    "2023-24": ANNUAL_WRA_PATH / "2023-24" / "Code",
    "2022-23": ANNUAL_WRA_PATH / "2022-23" / "Code",
    "2021-22": ANNUAL_WRA_PATH / "2021-22" / "Code",
    "2020-21": ANNUAL_WRA_PATH / "2020-21" / "Code",
    "2019-20": ANNUAL_WRA_PATH / "2019-20 reporting" / "Code",
    "2019BC": ANNUAL_WRA_PATH / "2018-19" / "Code",
    "2018BC": ANNUAL_WRA_PATH / "2017-18" / "Code",
    "2017BC": ANNUAL_WRA_PATH / "2016-17" / "Code",
    "2016BC": ANNUAL_WRA_PATH / "2015-16" / "Code",
    "2015BC": ANNUAL_WRA_PATH / "2014-15" / "Code",
    "2014BC": ANNUAL_WRA_PATH / "2013-14" / "Code",
    "2013BC": ANNUAL_WRA_PATH / "2012-13" / "Code",
    "2012BC": ANNUAL_WRA_PATH / "2011-12" / "Code",
    "2011BC": ANNUAL_WRA_PATH / "2010-11" / "Code",
}
"""Dictionary containing shortcuts to indicate the location of 
reporting periods. Each key is a shortcut string. Each value is 
a path to a folder which contains the **definition spreadsheets**."""

paths_reporting_period = {v: k for k, v in reporting_period_paths.items()}
"""An inverted version of the :attr:`wrap_technote.reporting.reporting_period_paths` mapping."""


INDEX_PAGE_STYLE = """
body, th, td {
    font-family: Verdana;
    font-size: 0.8em;
}

table {
    border-collapse: collapse;
    border: 1px solid black;
}

td, th {
    border: 1px solid #cccccc;
    padding: 3px;
}

thead td { font-weight: bold; }

pre {
    font-size: 1.2em;
}
"""


def create_index_pages_for_all_reporting_periods(style=INDEX_PAGE_STYLE):
    """Create index pages for all reporting periods.

    It also creates an index to those pages i.e. a starting point for all
    data produced by this module.

    Args:
        style (str): CSS for page.

    Returns:
        str: the filename of the index page to all reporting periods.

    """
    rp_keys = {}
    for path in ANNUAL_WRA_PATH.glob("*"):
        if path.is_dir():
            if "Code" in [p.name for p in path.iterdir()]:
                rp_key = rp_code_path_to_key(path / "Code")
                rp_keys[rp_key] = path
    rp_key_table = []
    for rp_key, path in rp_keys.items():
        create_index_page_for_reporting_period(rp_key)
        rp_key_table.append({"rp_key": rp_key, "path": path})
    print(rp_key_table)
    rp_key_table = pd.DataFrame(rp_key_table)
    rp_key_table["rp_key"] = rp_key_table.apply(
        lambda x: f'<a href="file:///{str(Path(x.path) / "index.html")}">{x.rp_key}</a>',
        axis=1,
    )

    curr_dir = Path(".").parent

    index_fn = curr_dir / "index.html"
    with open(index_fn, "w") as f:
        f.write(
            f"""
        <html>
        <head>
            <title>Reporting periods</title>
            <style>
            {style}
            </style>
        </head>
        <body>
            <h1>Reporting periods index</h1>
            <p><pre>{str(curr_dir)}</pre></p>
            {rp_key_table.to_html(escape=False)}
        </body>
        </html>
        """
        )
    return index_fn.absolute()


def create_index_page_for_reporting_period(rp, style=INDEX_PAGE_STYLE):
    """Produce a HTML page of links to child resources for a reporting period.

    Args:
        rp_key (str): the reporting period key.

    Returns:
        str: HTML document which contains the reports, groundwater summary pages,
        water level resource pages, salinity resource pages, and rainfall pages,
        all hyperlinked.

    """
    if isinstance(rp, str):
        rp = load_reporting_period(rp)

    rp_key = rp.key

    html = get_html_table(rp_key)
    rp_parent_path = rp.path.parent
    with open(rp_parent_path / "index.html", "w") as f:
        f.write(
            f"""
    <html>
    <head>
        <title>{rp_parent_path.stem}</title>
        <style>
        {style}
        </style>
    </head>
    <body>
        <h1>{rp_parent_path.stem} index</h1>
        <p><a href='file:///{str(rp_parent_path.parent / "index.html")}'>Show all reporting periods</a></p>
        <p><pre>{str(rp_parent_path)}</pre></p>
        {html}
    </body>
    </html>
    """
        )


def get_html_table(rp):
    """Produce a HTML table of links to child resources for a reporting period.

    Args:
        rp_key (str): the reporting period key.

    Returns:
        str: HTML table element which contains the reports, groundwater summary pages,
        water level resource pages, salinity resource pages, and rainfall pages,
        all hyperlinked.

    """
    if isinstance(rp, str):
        rp = load_reporting_period(rp)

    rp_key = rp.key

    mappings = rp.read_table("Report_Resources_mapping")
    rows = []
    for report_key in rp.report_keys:
        report = load_report(report_key, rp)
        rmappings = mappings[(mappings.report == report_key)]
        gw_summary = rmappings[rmappings.param == "Groundwater summaries"]
        rf_summary = rmappings[rmappings.param == "Rainfall"]

        if len(gw_summary) > 0:
            gw_summary = gw_summary.iloc[0].path
            url = "file:///" + str(rp.path.parent / gw_summary / "gw_summary.html")
            gw_summary = f'<a href="{url}">{report_key} (GW)</a>'
        else:
            gw_summary = ""

        if len(rf_summary) > 0:
            rf_summary = rf_summary.iloc[0].path
            url = "file:///" + str(rp.path.parent / rf_summary / "rainfall.html")
            rf_summary = f'<a href="{url}">{report_key} (Rainfall)</a>'
        else:
            rf_summary = ""

        wl_rows = rmappings[rmappings.param == "WL"]
        tds_rows = rmappings[rmappings.param == "TDS"]
        rowspan = max([len(wl_rows), len(tds_rows)])
        for i in range(rowspan):
            if i < len(wl_rows):
                rk_row = wl_rows.iloc[i]
                url = "file:///" + str(
                    rp.path.parent
                    / rk_row.path
                    / "technote_static"
                    / "waterlevels.html"
                )
                wl_rkey = (f'<a href="{url}">{rk_row.resource_key}</a>', 1, 1)
            else:
                wl_rkey = ("", 1, 1)

            if i < len(tds_rows):
                rk_row = tds_rows.iloc[i]
                url = "file:///" + str(
                    rp.path.parent / rk_row.path / "technote_static" / "salinities.html"
                )
                tds_rkey = (f'<a href="{url}">{rk_row.resource_key}</a>', 1, 1)
            else:
                tds_rkey = ("", 1, 1)

            if i == 0:
                row = [
                    (report_key, rowspan, 1),
                    (gw_summary, rowspan, 1),
                    wl_rkey,
                    tds_rkey,
                    (rf_summary, rowspan, 1),
                ]
            else:
                row = [wl_rkey, tds_rkey]
            rows.append(row)

    html = """<table><thead><td>Report</td><td>Groundwater summary page</td><td>Water level resource page</td>
    <td>Salinity resource page</td><td>Rainfall page</td></thead>
    """
    for row in rows:
        html += "<tr>"
        for value, rowspan, colspan in row:
            html += f"<td rowspan={rowspan} colspan={colspan}>" + value + "</td>"
        html += "</tr>"
    html += "</table>"
    return html


def load_html_templates():
    """Return Jinja2 environment for the bundled templates."""
    return Environment(
        loader=PackageLoader("wrap_technote", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )


def load_reporting_period(key=CURRENT_RPERIOD, **kwargs):
    """Load a reporting period.

    This is the place to start! A reporting period relates to a financial
    year in which reporting is being undertaken. For example, in Janaury 2022
    we typically begin analysis and production of reports for the reporting
    period `'2021-22'`, which covers a range of different data periods, but
    typically:

    - Groundwater level data up till late 2021
    - Groundwater salinity data up till Dec 31 2021
    - Rainfall data up until September 2021

    Args:
        key (str): either a key to the dictionary ``reporting_period_paths``
            in this module (``reporting.py``) e.g. "2021-22" or a path
            to the folder containing the definition table spreadsheets.
            The default is set in this module to the latest reporting period.

    Returns:
        :class:`wrap_technote.ReportingPeriod`: ReportingPeriod object.

    """
    pattern_1 = re.compile(r"(\d\d\d\d)-(\d\d)")
    pattern_2 = re.compile(r"(\d\d\d\d)BC")
    if key in reporting_period_paths:
        path = reporting_period_paths[key]
        logger.debug(
            f"Found pre-existing definition hard-coded in source: key={key} path={path}"
        )
        path.mkdir(parents=True, exist_ok=True)
    elif pattern_1.match(key):
        m = pattern_1.match(key)
        year = m.group(1)
        path = ANNUAL_WRA_PATH / key / "Code"
        logger.debug(f"Matched financial year pattern: key={key} path={path}")
        path.mkdir(parents=True, exist_ok=True)
    elif pattern_2.match(key):
        m = pattern_2.match(key)
        year1 = m.group(1)
        end_year = str(int(year1) - 1)
        start_year = str(int(end_year) - 4)
        path = (
            ANNUAL_WRA_PATH / f"Backcalc_{year1}_{start_year}-{end_year[2:]}" / "Code"
        )
        logger.debug(f"Matched backcalculated shorthand pattern: key={key} path={path}")
        path.mkdir(parents=True, exist_ok=True)
    else:
        path = Path(key)
        logger.debug(f"No match found. Assuming key == path. key={key} path={path}")
        try:
            assert path.is_dir()
        except AssertionError:
            raise KeyError(f"Failed to identify reporting period '{key}'")
    return ReportingPeriod(path, **kwargs)


def load_report(key, rperiod=None, **kwargs):
    """Load a report.

    Args:
        key (str): the report_key field value -- see below for examples
        rperiod (str): either a key to the dictionary ``reporting_period_paths``
            in this module (``reporting.py``) e.g. "2021-22" or a path
            to the folder containing the definition table spreadsheets.

    Returns:
        :class:`wrap_technote.Report`:

    You can find possible values of `key` by looking at the reporting period
    object (i.e. different reports could exist in different years):

    .. code-block:: python

        >>> import wrap_technote as tn
        >>> rp = tn.load_reporting_period('2021-22')
        >>> rp.report_keys
        ['Adelaide Plains',
         'Baroota',
         'Barossa',
         'Clare Valley',
         'EMLR',
         'Eyre Pen',
         'Far North',
         'Mallee and Peake',
         'Marne-Saunders',
         'McLaren Vale',
         'South East',
         'WMLR',
         'KI']

    """
    if rperiod is None:
        rperiod = load_reporting_period()
    return Report(key, reporting_period=rperiod, **kwargs)


def load_resource(key, rperiod=None, **kwargs):
    """Load a report.

    Args:
        key (str): the resource_key field value -- see below for examples
        rperiod (str): either a key to the dictionary ``reporting_period_paths``
            in this module (``reporting.py``) e.g. "2021-22" or a path
            to the folder containing the definition table spreadsheets.

    Returns:
        :class:`wrap_technote.Resource`:

    You can find possible values of `key` by looking at the reporting period
    object (i.e. different resources could exist in different years):

    .. code-block:: python

        >>> import wrap_technote as tn
        >>> rp = tn.load_reporting_period('2021-22')
        >>> rp.resource_keys
        ['Central_Adelaide_T1_TDS',
         'Kangaroo_Flat_T2_TDS',
         'NAP_T1_TDS',
         'NAP_T2_TDS',
         'Central_Adelaide_T1_WL',
         'Kangaroo_Flat_T2_WL',
         'NAP_T1_WL',
         'NAP_T2_WL',
         'Baroota_All_WL',
         'Baroota_All_TDS',
         'Barossa_FRA_TDS',
         'Barossa_Lower_TDS',
         'Barossa_Upper_TDS',
         'Barossa_FRA_WL',
         'Barossa_Lower_WL',
         'Barossa_Upper_WL',
         'Clare_FRA_TDS',
         'Clare_FRA_WL',
         'Angas_Bremer_MGL_TDS',
         'EMLR_FRA_TDS',
         'EMLR_MGL_TDS',
         'EMLR_Permian_TDS',
         'Angas_Bremer_MGL_WL',
         'Angas_Bremer_QPAP_WL',
         'EMLR_FRA_WL',
         'EMLR_MGL_WL',
         'EMLR_Permian_Finniss_WL',
         'EMLR_Permian_Tookayerta_WL',
         'EP_Musgrave_Bramfield_TDS',
         'EP_Musgrave_Polda_TDS',
         'EP_Southern_Basins_Coffin_Bay_TDS',
         'EP_Southern_Basins_Lincoln_South_TDS',
         'EP_Southern_Basins_Uley_North_TDS',
         'EP_Southern_Basins_Uley_South_TDS',
         'EP_Southern_Basins_Uley_Wanilla_TDS',
         'EP_Musgrave_Bramfield_WL',
         'EP_Musgrave_Polda_WL',
         'EP_Southern_Basins_Coffin_Bay_WL',
         'EP_Southern_Basins_Lincoln_South_WL',
         'EP_Southern_Basins_Uley_North_WL',
         'EP_Southern_Basins_Uley_South_WL',
         'EP_Southern_Basins_Uley_Wanilla_WL',
         'Far_North_JK_TDS',
         'Far_North_JK_WL',
         'Mallee_MGL_TDS',
         'Peake_Roby_Sherlock_Confined_TDS',
         'Mallee_MGL_WL',
         'Peake_Roby_Sherlock_Confined_WL',
         'Marne_Saunders_FRA_TDS',
         'Marne_Saunders_MGL_TDS',
         'Marne_Saunders_FRA_WL',
         'Marne_Saunders_MGL_WL',
         'McLaren_Vale_FRA_TDS',
         'McLaren_Vale_Maslin_Sand_TDS',
         'McLaren_Vale_PWF_TDS',
         'McLaren_Vale_All_TDS',
         'McLaren_Vale_FRA_WL',
         'McLaren_Vale_Maslin_Sand_WL',
         'McLaren_Vale_PWF_WL',
         'South_East_Confined_TDS',
         'South_East_Confined_LLC_Padthaway_TDS',
         'South_East_Confined_Tintinara_Tatiara_TDS',
         'South_East_LLC_Unconfined_Donovans_Coastal_Plains_TDS',
         'South_East_LLC_Unconfined_Highlands_TDS',
         'South_East_Padthaway_Unconfined_Flats_TDS',
         'South_East_Padthaway_Unconfined_Range_TDS',
         'Tatiara_Unconfined_Highlands_TDS',
         'Tatiara_Unconfined_Plains_TDS',
         'Tintinara_Coonalpyn_Unconfined_TDS',
         'South_East_Confined_LLC_WL',
         'South_East_Confined_Padthaway_WL',
         'South_East_Confined_Tatiara_WL',
         'South_East_Confined_Tintinara_Coonalpyn_WL',
         'South_East_LLC_Unconfined_Donovans_Coastal_Plains_WL',
         'South_East_LLC_Unconfined_Highlands_WL',
         'South_East_Padthaway_Unconfined_Flats_WL',
         'South_East_Padthaway_Unconfined_Range_WL',
         'Tatiara_Unconfined_Highlands_WL',
         'Tatiara_Unconfined_Plains_WL',
         'Tintinara_Coonalpyn_Unconfined_Mallee_Highlands_WL',
         'Tintinara_Coonalpyn_Unconfined_Plains_WL',
         'WMLR_FRA_TDS',
         'WMLR_Permian_TDS',
         'WMLR_Tertiary_Limestone_TDS',
         'WMLR_FRA_WL',
         'WMLR_Permian_WL',
         'WMLR_Tertiary_Limestone_WL']

    """
    if rperiod is None:
        rperiod = load_reporting_period()
    return Resource(key, reporting_period=rperiod, **kwargs)


def rp_key_to_path(key):
    pattern_1 = re.compile(r"(\d\d\d\d)-(\d\d)")
    pattern_2 = re.compile(r"(\d\d\d\d)BC")
    if key == "2019-20":
        return ANNUAL_WRA_PATH / "2019-20 reporting" / "Code"
    elif pattern_1.match(key):
        m = pattern_1.match(key)
        year = m.group(1)
        return ANNUAL_WRA_PATH / key / "Code"
    elif pattern_2.match(key):
        m = pattern_2.match(key)
        year1 = m.group(1)
        end_year = str(int(year1) - 1)
        start_year = str(int(end_year) - 4)
        return (
            ANNUAL_WRA_PATH / f"Backcalc_{year1}_{start_year}-{end_year[2:]}" / "Code"
        )
    else:
        raise KeyError("Reporting period key type not understood.")


def rp_code_path_to_key(path):
    if path == ANNUAL_WRA_PATH / "2019-20 reporting" / "Code":
        return "2019-20"
    elif path.parent.name.startswith("Backcalc_"):
        return path.parent.name.split("_")[1] + "BC"
    else:
        return path.parent.name


class ReportingPeriod:
    """Load definition and validation spreadsheets for a given reporting
    period.

    Args:
        path (str): path to the "Code" subfolder of a reporting period.

    See :func:`wrap_technote.load_reporting_period` for an easier way
    to load an existing reporting period using the shortcuts defined in the
    source code of the wrap_technote:reporting.py module, e.g. "2021-22".

    Attributes:
        key (str): the name of this period e.g. "2021-22"
        path (pathlib.Path): the path to the "Code" subfolder
        report_resources_mapping (pandas.DataFrame): the definition of
            the report keys and resource keys contained in this
            reporting preiod, from the Report_Resources_mapping.xlsx spreadsheet.
        report_keys (list of str): a list of the report keys defined for this
            reporting period.
        resource_keys (list of str): a list of the resource keys defined for this
            reporting period.

    """

    def __init__(self, path):
        if path in reporting_period_paths:
            path = reporting_period_paths[path]
        self.path = Path(path)
        self.dfs_cache = {}

    def _repr_html_(self):
        return (
            f"<table><thead><td>{__name__}.{self.__class__.__name__} object</td><td></td></thead>"
            f"<tr><td>key</td><td>{self.key}</td></tr>"
            f"<tr><td>path:</td><td>{self.path}</td></tr>"
            f"<tr><td>report_keys:</td><td>{', '.join(self.report_keys)}</td></tr>"
            "</table>"
        )

    @property
    def key(self):
        return self.path.parent.name

    # ==== Definition tables ====

    @property
    def report_resources_mapping(self):
        return self.read_table("Report_Resources_mapping")

    @property
    def season_definitions(self):
        return self.read_table("Season_definitions")

    @property
    def data_validation(self):
        return self.read_table("Data_validation")

    # ==== Frequently used fields from definition tables ====

    @property
    def report_keys(self):
        keys = self.report_resources_mapping.report.unique()
        return [k for k in keys if k == str(k)]  # some are "nan"

    @property
    def resource_keys(self):
        keys = self.report_resources_mapping.resource_key.unique()
        return [k for k in keys if k == str(k)]  # some are "nan"

    # ==== Methods ====

    def read_table(self, arg_filename):
        """Read and cache the file. Re-load only if modified more
        recently than cached.

        """
        path = self.path / arg_filename
        glob_path = str(path) + "*.xlsx"
        paths = [Path(f) for f in glob.glob(glob_path)]
        dfs = []
        for path in paths:
            filename = path.name
            if not os.path.isfile(path) and os.path.isfile(str(path) + ".xlsx"):
                path = Path(str(path) + ".xlsx")

            mtime = os.path.getmtime(path)

            recache = False
            if not filename in self.dfs_cache:
                recache = True
            elif mtime > self.dfs_cache[filename]["mtime"]:
                recache = True

            if recache:
                logger.debug(f"re-opening {filename} to store in cache")
                df = pd.read_excel(path)
                df["filename"] = filename
                self.dfs_cache[filename] = {"mtime": mtime, "df": df}
            dfs.append(self.dfs_cache[filename]["df"])
        return pd.concat(dfs, sort=True)


class Report:
    def __init__(self, report_key, reporting_period=None):
        self.report_key = report_key
        if not isinstance(reporting_period, ReportingPeriod):
            reporting_period = load_reporting_period(reporting_period)
        self.reporting_period = reporting_period

    def _repr_html_(self):
        return (
            f"<table><thead><td>{__name__}.{self.__class__.__name__} object</td><td></td></thead>"
            f"<tr><td>reporting_period:</td><td>{self.reporting_period.key}</td></tr>"
            f"<tr><td>report_key</td><td>{self.report_key}</td></tr>"
            f"<tr><td>rainfall_path:</td><td>{self.rainfall_path}</td></tr>"
            f"<tr><td>gw_summaries_path:</td><td>{self.gw_summaries_path}</td></tr>"
            f"<tr><td>resource_keys:</td><td>{', '.join(self.resource_keys)}</td></tr>"
            "</table>"
        )

    @property
    def resource_keys(self):
        df = self.read_table("Report_Resources_mapping")
        return [
            str(v) for v in df.resource_key.values if str(v) != "nan" and str(v) != ""
        ]

    @property
    def gw_summaries_path(self):
        df = self.read_table("Report_Resources_mapping")
        return self.reporting_period.path.parent / Path(
            df[df.param == "Groundwater summaries"].iloc[0].path
        )

    @property
    def rainfall_path(self):
        df = self.read_table("Report_Resources_mapping")
        return self.reporting_period.path.parent / Path(
            df[df.param == "Rainfall"].iloc[0].path
        )

    @property
    def extraction_path(self):
        df = self.read_table("Report_Resources_mapping")
        return self.reporting_period.path.parent / Path(
            df[df.param == "Extraction"].iloc[0].path
        )

    @property
    def report_settings(self):
        with add_import_path(str(self.gw_summaries_path)):
            import report_settings

            importlib.reload(report_settings)
            report_settings.report = self
            report_settings.reporting_period = self.reporting_period
            return report_settings

    def resource_settings(self, resource_key):
        with add_import_path(str(self.gw_summaries_path)):
            r = importlib.import_module(resource_key)
            r.resource_key = resource_key
            r.report = self
            r.reporting_period = self.reporting_period
            return r

    def read_table(self, filename):
        # logger.debug(f"Reading table: {filename}")
        df = self.reporting_period.read_table(filename)
        if "report" in df:
            return df[df.report == self.report_key]
        elif "report_key" in df:
            return df[df.report_key == self.report_key]
        else:
            return df

    def aggregate_resources(self, param=None):
        df = self.read_table("GW_Aggregate_resource_definitions")
        if param in ("WL", "TDS"):
            return df[df.param == param]
        else:
            return df

    def get_aggregate_resources_data(self, param, workbook_name, worksheet_name):
        """Get a dictionary of concatenated pandas DataFrames for
        aggregated resources.

        Args:
            param (str): either "WL" or "TDS"
            workbook_name (str): data spreadsheet to go to e.g. either
                "recovery_wl_data", "recovery_wl_trends", or "salinity_trends", or
                "validated data"
            worksheet_name (str): worksheet to retrieve.

        Returns: a dictionary; the key is the aggregate resource key and the value
            is a concatenated pandas dataframe of all the data tables for the resource
            keys within the aggregated resource.

        """
        result = {}
        logger.debug(f"Loading aggregate resources for {param}")
        aggs = self.aggregate_resources(param=param)
        logger.debug(f"Aggregate resources are:\n{aggs}")
        dfs = read_data(
            aggs.resource_key,
            workbook_name,
            worksheet_name,
            reporting_period=self.reporting_period,
        )
        for agg_res_key, sdf in aggs.groupby("aggregate_resource_key"):
            resource_keys = sdf.resource_key.unique()
            logger.debug(f"Concatenating data for {agg_res_key}:: {resource_keys}")
            concat_dfs = []
            for r in set(resource_keys):
                df = dfs[r]
                df["resource_key"] = r
                concat_dfs.append(df)
            rdf = pd.concat(concat_dfs)
            rdf = rdf[
                ["resource_key"] + [c for c in rdf.columns if not c == "resource_key"]
            ]
            result[agg_res_key] = rdf
            # result[agg_res_key] = pd.concat([dfs[r] for r in resource_keys])
        return result

    def rainfall_dfn(self, station_id=None):
        """Read the definition of a rainfall station period from the
        definition table "Report_Rainfall_stations".

        Args:
            station_id (str): ID of the rainfall station, from the column
                'station_id'. Example values are the BoM station number
                e.g. '23730' or the Aquarius location ID, e.g. 'A5121008'.
                If ``None``, returns a pd.DataFrame of all stations.

        Returns:
            pd.Series with index values corresponding to the column names
            from "Report_Rainfall_stations"

        pd.Series index values are:

        - report
        - previous_users
        - station_type
        - station_id
        - station_name
        - data_start
        - mean_period_start
        - mean_period_finish
        - rf_period_start
        - rf_period_finish
        - comments

        """
        rdf = self.read_table("Report_Rainfall_stations")
        if station_id is None:
            return rdf
        else:
            return rdf[rdf.station_id.astype(str) == str(station_id)].iloc[0]

    def rainfall_filenames(self, name_glob="*", id_glob="*"):
        """Returns metadata for rainfall data files located at the rainfall
        data path for this report.

        Note this is determined by what is in the folder and available, not
        what is specified in the definition table "Report_Rainfall_stations"

        Args:
            name_glob (str): default '*' (all files)
            id_glob (str): default '*' (all files)

        Returns:
            list of dicts - data keys below.

        Filenames should match a pattern of the following:
        ``DATASOURCE_data_REPORTNAME_STATIONID_STATIONNAME.xlsx`` where
        DATASOURCE is either 'silo', 'hydstra' or 'aquarius'. There might be
        spaces in REPORTNAME or STATIONNAME.

        An example return list is shown below. Each item of the list is a dict
        with keys:

            - filename (pathlib.Path)
            - station (str)
            - id (str)
            - name (str)
            - data_source (str): either 'silo' (BoM), 'hydstra', or 'aquarius'
            - dfn (pd.Series) with following keys from the definition
              table:

              - comments (str)
              - data_start (pd.Timestamp)
              - filename (str): source of definition data
              - mean_period_finish (pd.Timestamp)
              - mean_period_start (pd.Timestamp)
              - previous_users (str): original source of rainfall station in
                old status reports
              - report (str): report_key
              - rf_period_finish (pd.Timestamp)
              - rf_period_start (pd.Timestamp)
              - station_id (str)
              - station_name (str)
              - station_type (str): either 'BoM', 'Hydstra' or 'Aquarius'


        .. code-block:: none

            [{'filename': WindowsPath('R:/DFW_CBD/Projects/Projects_Science/Water Resource Assessments/Annual/2020-21/Data/Eyre Pen/Rainfall/silo_data_Eyre Pen_18017_PORT LINCOLN (BIG SWAMP).xlsx'),
             'station': '18017',
             'id': '18017',
             'name': 'PORT LINCOLN (BIG SWAMP)',
             'data_source': 'silo',
             'dfn': comments                    Southern Basins primary
             data_start                      1950-01-01 00:00:00
             filename              Report_Rainfall_stations.xlsx
             mean_period_finish              2020-12-31 00:00:00
             mean_period_start               1971-01-01 00:00:00
             previous_users                                   GW
             report                                     Eyre Pen
             rf_period_finish                2020-12-31 00:00:00
             rf_period_start                 2020-01-01 00:00:00
             station_id                                    18017
             station_name                              Big Swamp
             station_type                                    BoM
             Name: 22, dtype: object},
             ...
             {'filename': WindowsPath('R:/DFW_CBD/Projects/Projects_Science/Water Resource Assessments/Annual/2020-21/Data/Eyre Pen/Rainfall/hydstra_data_Eyre Pen_A5121003_Shoal Point.xlsx'),
             'station': 'A5121003',
             'id': 'A5121003',
             'name': 'Shoal Point',
             'data_source': 'hydstra',
             'dfn': comments                     Hydstra data - not BoM
             data_start                      2010-01-01 00:00:00
             filename              Report_Rainfall_stations.xlsx
             mean_period_finish              2020-12-31 00:00:00
             mean_period_start               2010-01-01 00:00:00
             previous_users                                   GW
             report                                     Eyre Pen
             rf_period_finish                2020-12-31 00:00:00
             rf_period_start                 2020-01-01 00:00:00
             station_id                                 A5121003
             station_name                            Shoal Point
             station_type                                Hydstra
             Name: 27, dtype: object}]

        """
        logger.debug(f"Looking for rainfall filenames matching name_glob={name_glob}")
        data = []
        silo_filenames = [
            f
            for f in self.rainfall_path.glob(
                f"silo_data_{self.report_key}_{id_glob}_{name_glob}.xlsx"
            )
        ]
        logger.debug(f"Found SILO filenames: {silo_filenames}")
        hydstra_filenames = [
            f
            for f in self.rainfall_path.glob(
                f"hydstra_data_{self.report_key}_{id_glob}_{name_glob}.xlsx"
            )
        ]
        aqts_filenames = [
            f
            for f in self.rainfall_path.glob(
                f"aquarius_data_{self.report_key}_{id_glob}_{name_glob}.xlsx"
            )
        ]
        logger.debug(f"Found Aquarius filenames: {aqts_filenames}")
        for filename in silo_filenames + hydstra_filenames + aqts_filenames:
            logger.debug(f"Found rainfall data file: {filename}")
            parts = Path(filename).stem.split("_")
            station_id, station_name = parts[3:5]
            try:
                dfn = self.rainfall_dfn(station_id)
            except IndexError:
                logger.warning(
                    f"No definition was found in Report_Rainfall_stations for {station_id} {station_name}"
                    "Substituting defaults instead."
                )
                station_types = {
                    "silo": "BoM",
                    "hydstra": "Hydstra",
                    "aquarius": "Aquarius",
                }
                dfn = pd.Series(
                    {
                        "report": self.report_key,
                        "previous_users": "",
                        "station_type": station_types[parts[0]],
                        "station_id": station_id,
                        "station_name": station_name,
                        "data_start": pd.Timestamp("1950-01-01"),
                        "mean_period_start": pd.Timestamp("1970-07-01"),
                        "mean_period_finish": pd.Timestamp("2019-06-30"),
                        "rf_period_start": pd.Timestamp("2018-07-01"),
                        "rf_period_finish": pd.Timestamp("2019-09-30"),
                        "comments": "default definition",
                    }
                )
            data.append(
                {
                    "filename": filename,
                    "station": station_id,
                    "id": station_id,
                    "name": station_name,
                    "data_source": parts[0],
                    "dfn": dfn,
                }
            )
        return data

    def rainfall_files(self, sheet_name=None, **kwargs):
        """Get rainfall data. Deprecated.

        I suggest you use these instead:

            >>> rfdata = report.rainfall_filenames()
            >>> for rfstation in rfdata:
            ...     df = report.get_rainfall_data_for_station(
            ...         rfstation, sheet_name="annual (water-use year)"
            ...     )
            ...

        """
        data = {}
        for d in self.rainfall_filenames(**kwargs):
            filename = d["filename"]
            parts = Path(filename).stem.split("_")
            station_id, station_name = parts[3:5]
            d["df"] = pd.read_excel(filename, sheet_name=sheet_name)
            yield d

    def find_rainfall_station(self, id=None, name=None, regex=False, **kwargs):
        """Find a rainfall station.

        Args:
            id (int): station identifier
            name (str): station name
            regex (bool): how "name" is used, as a regular expression match,
                or, if False, as an identical match.

        Returns: a dictionary of the rainfall station's definition.

        """
        logger.debug(f"Trying to load station_id={id} station_name={repr(name)}")
        filenames = self.rainfall_filenames()
        for i, station in enumerate(filenames):
            if id == station.get("station", None):
                return station
            elif name:
                if regex:
                    m = re.match(name, station["name"])
                    if m:
                        return station
                else:
                    if name == station.get("name", None):
                        return station
        raise KeyError(f"station_id={id} name={repr(name)} not found")

    def find_rainfall_stations(self, **kwargs):
        """Get a list of rainfall station definitions.

        Args:
            name_glob (str, default "*"):
            id_glob (str, default "*"):

        Returns: a list of dictionaries with keys "filename" (str), "station"
            (integer identifier), "name" (str, station name), "data_source"
            and "dfn".

        """
        return self.rainfall_filenames(**kwargs)

    def get_rainfall_data(
        self, station=None, sheet_name="annual (water-use year)", *args, **kwargs
    ):
        """Get rainfall data as a DataFrame.

        Args:
            station (dict with key "filename" or None): if None, see keyword
                arguments below. Otherwise it should be dictionary with a key
                "filename" - the value of that item will be used to load
                an Excel spreadsheet.
            sheet_name (str): a sheet in the spreadsheet. Valid options currently
                are: "daily", "annual (calendar)", "annual (water-use year)",
                and "annual provenance"

        Keyword Args:
            id (int): station identifier
            name (str): station name
            regex (bool): how "name" is used, as a regular expression match,
                or, if False, as an identical match.

        Returns: pandas.DataFrame

        """
        if station is None:
            station = self.find_rainfall_station(*args, **kwargs)
        return pd.read_excel(station["filename"], sheet_name=sheet_name)

    def get_all_rainfall_data(self, station=None, *args, **kwargs):
        """Get rainfall data as a DataFrame.

        Args:
            station (dict with key "filename" or None): if None, see keyword
                arguments below. Otherwise it should be dictionary with a key
                "filename" - the value of that item will be used to load
                an Excel spreadsheet.
            sheet_name (str): a sheet in the spreadsheet. Valid options currently
                are: "daily", "annual (calendar)", "annual (water-use year)",
                and "annual provenance"

        Keyword Args:
            id (int): station identifier
            name (str): station name
            regex (bool): how "name" is used, as a regular expression match,
                or, if False, as an identical match.

        Returns: pandas.DataFrame

        """
        if station is None:
            station = self.find_rainfall_station(*args, **kwargs)
        return pd.read_excel(station["filename"], sheet_name=None)

    def calculated_rainfall_files(self, format="long"):
        data = {}
        for excel_filename in self.rainfall_path.glob("report_rainfall*.xlsx"):
            parts = Path(excel_filename).stem.split("_")
            station, name, period_start, period_finish = parts[3:]
            data[station] = {
                "station": station,
                "name": name,
                "period_start": period_start,
                "period_finish": period_finish,
                "dfs": pd.read_excel(excel_filename, sheet_name=None),
                "excel_filename": excel_filename,
            }
        for station in data.keys():
            silo_pngs = [
                x for x in self.rainfall_path.glob(f"plot_station_{station}*.png")
            ]
            annual_pngs = [
                x
                for x in self.rainfall_path.glob(f"annual_rainfall_wuy_{station}_*.png")
            ]
            annual_pngs += [
                x
                for x in self.rainfall_path.glob(
                    f"annual_rainfall_calendar_{station}_*.png"
                )
            ]
            monthly_pngs = [
                x for x in self.rainfall_path.glob(f"monthly_rainfall_{station}_*.png")
            ]
            analysis_monthly_pngs = [
                x
                for x in sorted(
                    (self.rainfall_path / "analysis_figures").glob(
                        f"monthly_rainfall_internal_*_{station}*.png"
                    )
                )
            ]
            analysis_annual_calendar_pngs = [
                x
                for x in sorted(
                    (self.rainfall_path / "analysis_figures").glob(
                        f"annual_rainfall_internal_calendar_{station}*.png"
                    )
                )
            ]
            analysis_annual_financial_pngs = [
                x
                for x in sorted(
                    (self.rainfall_path / "analysis_figures").glob(
                        f"annual_rainfall_internal_financial_{station}*.png"
                    )
                )
            ]
            data[station]["silo_pngs"] = silo_pngs
            data[station]["annual_pngs"] = annual_pngs
            data[station]["monthly_pngs"] = monthly_pngs
            data[station]["analysis_monthly_pngs"] = analysis_monthly_pngs
            data[station][
                "analysis_annual_calendar_pngs"
            ] = analysis_annual_calendar_pngs
            data[station][
                "analysis_annual_financial_pngs"
            ] = analysis_annual_financial_pngs
            data[station]["relative_silo_pngs"] = [f"./{p.name}" for p in silo_pngs]
            data[station]["relative_annual_pngs"] = [f"./{p.name}" for p in annual_pngs]
            data[station]["relative_monthly_pngs"] = [
                f"./{p.name}" for p in monthly_pngs
            ]
            data[station]["relative_analysis_monthly_pngs"] = [
                f"./analysis_figures/{p.name}" for p in analysis_monthly_pngs
            ]
            data[station]["relative_analysis_annual_calendar_pngs"] = [
                f"./analysis_figures/{p.name}" for p in analysis_annual_calendar_pngs
            ]
            data[station]["relative_analysis_annual_financial_pngs"] = [
                f"./analysis_figures/{p.name}" for p in analysis_annual_financial_pngs
            ]

        first_station = data[list(data.keys())[0]]
        keys = first_station["dfs"].keys()
        tables = {}

        for k in keys:
            dfs = []
            for sid, s in data.items():
                logger.debug(f"df name k={k} -- sid={sid} --> keys={s.keys()}")
                df = s["dfs"][k]
                df["sid"] = sid
                dfs.append(df)
            df = pd.concat(dfs)
            df = df.drop_duplicates()
            tables[k] = df

        mtotal_key = [k for k in keys if k.endswith(" monthly totals")][0]

        data["pivoted"] = {}
        data["pivoted"]["calendar"] = (
            tables["calendar"].set_index("year").pivot(columns="sid")
        )
        data["pivoted"]["water-use year"] = (
            tables["water-use year"].set_index("wu_year").pivot(columns="sid")
        )
        data["pivoted"]["means"] = (
            tables["means"].set_index("Unnamed: 0").pivot(columns="sid")
        )
        data["pivoted"]["monthly means"] = (
            tables["monthly means"].set_index("Date").pivot(columns="sid")
        )

        dp = tables[mtotal_key].ffill()
        if "-" in mtotal_key:
            year0 = int(mtotal_key[:4])
            year1 = year0 + 1
            dp = dp[~((dp["Date"] == year1) & (dp["Date.1"] >= 7))]
        else:
            dp = tables[mtotal_key].ffill()
        data["pivoted"][mtotal_key] = dp.set_index(["Date.1"])[["Rain", "sid"]].pivot(
            columns="sid"
        )
        data["pivoted"]["trend line (water-use years)"] = (
            tables["trend line (water-use years)"]
            .set_index(["sid"])[["start", "finish", "slope (mm/y)", "intercept"]]
            .T
        )
        data["pivoted"]["trend line (calendar years)"] = (
            tables["trend line (calendar years)"]
            .set_index(["sid"])[["start", "finish", "slope (mm/y)", "intercept"]]
            .T
        )

        return data


class Resource:
    """Load definition and validation spreadsheets for a given groundwater
    resource and parameter in a given reporting period.

    Args:
        name (str): the resource_key e.g. "Central_Adelaide_T1_TDS"
        reporting_period (wrap_technote.ReportingPeriod or str): the reporting period
            such as "2019-20". This doesn't refer to the period of data being
            analysed, it refers to when the analysis was done, and defines
            a set of definition and validation spreadsheets. See
            :class:`wrap_technote.ReportingPeriod` for more details.

    Attributes:
        report_resources_mapping (pd.Series): the fields containing in the Code
            definition spreadsheet "Report_Resources_mapping.xlsx"

    """

    def __init__(self, resource_key, reporting_period=None):
        self.resource_key = resource_key
        if not isinstance(reporting_period, ReportingPeriod):
            reporting_period = load_reporting_period(reporting_period)
        self.reporting_period = reporting_period
        dfn = self.read_table("GW_Resource_definitions")
        self.well_selection_query = WellSelectionQuery(
            dfn, shapefile_path=self.reporting_period.path / "spatial_data"
        )

    def _repr_html_(self):
        return (
            f"<table><thead><td>{__name__}.{self.__class__.__name__} object</td><td></td></thead>"
            f"<tr><td>reporting_period</td><td>{self.reporting_period.key}</td></tr>"
            f"<tr><td>report_key</td><td>{self.report_key}</td></tr>"
            f"<tr><td>resource_key</td><td>{self.resource_key}</td></tr>"
            f"<tr><td>data_path:</td><td>{self.data_path}</td></tr>"
            f"<tr><td>trend:</td><td>{self.trend_dfn.start_year} - {self.trend_dfn.end_year}</td></tr>"
            "</table>"
        )

    @property
    def data_path(self):
        return self.reporting_period.path.parent / Path(
            self.read_table("Report_Resources_mapping").iloc[0].path
        )

    @property
    def data_path2(self):
        parts = list(self.data_path.parts)
        parts[0] = r"\\env.sa.gov.au\dfsroot"
        return Path(*parts)

    @property
    def static_path(self):
        p = self.data_path / "technote_static"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def parameter(self):
        return "WL" if "_WL" in self.resource_key else "TDS"

    @property
    def report_key(self):
        table = self.read_table("Report_Resources_mapping")
        return table.report.iloc[0]

    @property
    def report_resources_mapping(self):
        return self.read_table("Report_Resources_mapping").iloc[0]

    @property
    def dfn_salinity_indicators(self):
        if self.resource_key.endswith("TDS"):
            return self.read_table("Definitions_salinity_indicators").iloc[0]
        return KeyError("Not defined for WL resources.")

    @property
    def report(self):
        return load_report(self.report_key, self.reporting_period)

    @property
    def trend_dfn(self):
        thresholds = self.read_table("Definitions_triclass_trend_thresholds")
        subset = thresholds[thresholds.apply_to_well_ids == "all by default"]
        if len(subset):
            return subset.iloc[0]
        else:
            raise KeyError(
                "Definitions_triclass_trend_thresholds.xlsx must have a row with apply_to_well_ids == 'all by default'"
            )

    def trend_dfn_for_well(self, well_id):
        dfn = self.trend_dfn.to_dict()
        thresholds = self.read_table("Definitions_triclass_trend_thresholds")
        df = thresholds[thresholds.apply_to_well_ids.str.contains(well_id)]
        if len(df):
            update_with = df.iloc[0].to_dict()
            for k, v in update_with.items():
                try:
                    if np.isnan(v):
                        v = 0
                except TypeError:
                    pass
                if v:
                    dfn[k] = v
        return pd.Series(dfn)

    @property
    def trend_start_year(self):
        return self.trend_dfn.start_year

    @property
    def trend_end_year(self):
        return self.trend_dfn.end_year

    @property
    def trend_min_data_pts(self):
        return self.trend_dfn.min_data_pts

    def read_table(self, filename):
        logger.debug(f"Reading table: {filename}")
        df = self.reporting_period.read_table(filename)
        if "resource_key" in df:
            return df[df.resource_key == self.resource_key]
        else:
            return df

    def get_data_table_names(self):
        """Get table names from SQLite database filename.

        Returns: a list of two tuples e.g. [("validated_data", "valid_data"), ...]. The
            actual table name in the SQLite database is "validated_data__valid_data".

        """
        path = self.get_data_db_filename()
        logger.debug(f"Reading data table names from {path}")
        with sqlite3.connect(str(path)) as db_conn:
            query_sql = "select name from sqlite_master where type = 'table' and name not like 'sqlite_%'"
            df = pd.read_sql(query_sql, db_conn)
        return [x.split("__") for x in df["name"].values]

    def get_data_db_filename(self):
        """Get SQLite database filename as Path object."""
        filename = f"data_{self.resource_key}.sqlite"
        path = self.data_path / filename
        return path

    def read_data(self, prefix, sheet_name=None):
        """Open a data file matching *pattern* and sheet_name.

        Args:
            pattern (str): glob pattern e.g. "validated_data"
            sheet_name (str or None): if str, return just that sheet.
                If None, return all sheets as a dictionary.

        """
        path = self.get_data_db_filename()
        logger.debug(f"Reading data from {path}")
        if sheet_name is None and not "__" in prefix:
            with sqlite3.connect(str(path)) as db_conn:
                table_names = pd.read_sql(
                    "select name from sqlite_master where type = 'table'", db_conn
                ).name.unique()
                logger.debug(f"Reading all sheets for {prefix} :: {table_names}")
                dfs = DataFileDict()
                for table_name in table_names:
                    df = pd.read_sql(f"select * from {table_name}", db_conn)
                    for c in df.columns:
                        if c.endswith("_date"):
                            logger.debug(
                                f"converting {path}:{table_name}:{c} to datetime format."
                            )
                            df[c] = pd.to_datetime(
                                df[c], format="%Y-%m-%d %H:%M:%S", errors="coerce"
                            )
                    name = table_name.split("__")[1]
                    dfs[name] = df
                return dfs
        elif sheet_name is None and "__" in prefix:
            table_name = prefix
            with sqlite3.connect(str(path)) as db_conn:
                df = pd.read_sql(f"select * from {table_name}", db_conn)
                for c in df.columns:
                    if c.endswith("_date"):
                        logger.debug(
                            f"converting {path}:{table_name}:{c} to datetime format."
                        )
                        df[c] = pd.to_datetime(
                            df[c], format="%Y-%m-%d %H:%M:%S", errors="coerce"
                        )
                return df
        else:
            sheet_name = prefix + "__" + sheet_name.lower().replace(" ", "_")
            logger.debug(f"Reading one sheet: {sheet_name}")
            with sqlite3.connect(str(path)) as db_conn:
                df = pd.read_sql(f"select * from {sheet_name}", db_conn)
                for c in df.columns:
                    if c.endswith("_date"):
                        logger.debug(
                            f"converting {path}:{sheet_name}:{c} to datetime format."
                        )
                        df[c] = pd.to_datetime(
                            df[c], format="%Y-%m-%d %H:%M:%S", errors="coerce"
                        )
                return df

    def write_data_sheets(self, prefix, sheets, as_sqlite=True, as_excel=True):
        """Write data sheets to disk.

        Args:
            book_name (str): stem of sqlite file to store in, i.e.
                "validated_data" will go into the file "validated_data_{self.resource_key}.sqlite"
            sheets (dict): keys are sheet names, values are pandas DataFrames

        Sheet names will be converted to underscore characters e.g. "current ranked WLs"
        will become "current_ranked_wls".

        The index of all pandas DataFrames will not be written.

        """
        if as_sqlite:
            filename = f"data_{self.resource_key}.sqlite"
            path = self.data_path / filename
            logger.debug(f"Writing data sheet to sqlite db at {path}...")
            with sqlite3.connect(str(path)) as db_conn:
                for suffix, sheet_df in sheets.items():
                    sheet_name = prefix + "__" + suffix.lower().replace(" ", "_")
                    logger.debug(
                        f"Adding last_run information to {prefix} :: {suffix}..."
                    )
                    if len(sheet_df):
                        sheet_df.loc[:, "last_run_by"] = os.getlogin()
                        sheet_df.loc[:, "last_run_date"] = datetime.now().isoformat()
                    sheet_df = sheet_df.loc[:, ~sheet_df.columns.duplicated()]
                    logger.debug(
                        f"Writing {sheet_name} as table - columns {list(sheet_df.columns)}"
                    )
                    df_for_sql(sheet_df).to_sql(
                        sheet_name, db_conn, index=False, if_exists="replace"
                    )
        if as_excel:
            filename = f"{prefix}_{self.resource_key}.xlsx"
            path = self.data_path / filename
            logger.debug(f"Writing data spreadsheet to {path}...")
            with pd.ExcelWriter(path) as writer:
                for sheet_name, sheet_df in sheets.items():
                    sheet_name = sheet_name.lower().replace(" ", "_")
                    logger.debug("Adding last_run information to tables...")
                    if len(sheet_df):
                        sheet_df.loc[:, "last_run_by"] = os.getlogin()
                        sheet_df.loc[:, "last_run_date"] = datetime.now().isoformat()
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

    def find_wells(self, *args, **kwargs):
        """Find all wells with data at least from the reporting year.

        See :class:`wrap_technote.WellSelectionQuery` for arguments.

        Args:
            parameter (str, optional): either "WL" or "TDS"
            start_year (int, optional): by default, the end of the reporting period
            end_year (int, optional): by default, the end of the reporting period
            min_data_pts (int, optional): by default, 1

        """
        if len(args) == 0:
            args = (self.parameter,)
        if len(kwargs) == 0:
            kwargs = {
                "start_year": self.trend_dfn.end_year,
                "end_year": self.trend_dfn.end_year,
                "min_data_pts": 1,
            }
        return self.well_selection_query.find_wells(*args, **kwargs)

    def filter_table_by_well_ids(self, well_ids, table):
        tdf = self.read_table(table)
        tdf = tdf[tdf.parameter == self.parameter]
        return tdf[
            [
                len([y for y in x if y.strip() in well_ids]) > 0
                for x in tdf.well_id.str.split(",")
            ]
        ]

    def get_season_str(self, well_id, well_id_col="well_id"):
        """Find relevant season definition string from the
        Seasons_definition spreadsheet (for the recovered WL).

        Args:
            well_id (str): well identifier
            well_id_col (str): column to search for well identifier in.

        Only relevant if the parameter is WL.

        """
        assert self.parameter == "WL"
        sdf = pd.DataFrame(self.reporting_period.read_table("Season_definitions"))
        sdf = sdf[sdf.resource_key == self.resource_key]
        well_id_rows = sdf[
            sdf[well_id_col].str.contains(well_id, regex=False, na=False)
        ]
        if len(well_id_rows) == 0:
            logger.debug(
                f"Using {self.resource_key} default season definition for {well_id}"
            )
            return sdf[sdf.well_id == "default"].iloc[0]["seasons_from_str"]
        else:
            logger.debug(f"Found season definition directly for {well_id}")
            return well_id_rows.iloc[0]["seasons_from_str"]

    def get_season(self, *args, **kwargs):
        """Return relevant :class:`wrap_technote.Seasons` object for a given
        well (for the recovered WL).

        See :meth:`wrap_technote.Resource.get_season_str` for arguments
        and keyword arguments.

        """
        return Seasons.from_str(self.get_season_str(*args, **kwargs))

    def get_wl_ranking_qc_results(self, wls, unique_grouper="year+season"):
        """Get results of comparing the well data quality ("QC") table
        with the requirements ("GW_WL_rankings_qc_requirements.xlsx").


        The indexer list can be used to select those wells from the QC
        table which pass the requirements

        """
        table = self.read_table("GW_WL_rankings_qc_requirements")
        years_to_extract = [
            int(c.split()[0].split("_")[-1])
            for c in table.columns
            if c.strip().startswith("n_obs_in_")
        ]
        logger.debug(f"years_to_extract: {years_to_extract}")
        spans_to_count_in = [
            [int(x) for x in c.split()[0].split("_")[-2:]]
            for c in table.columns
            if c.strip().startswith("n_obs_btwn_")
        ]

        logger.debug(f"spans_to_count_in: {spans_to_count_in}")
        qc = wls.groupby("well_id").apply(
            lambda df: calc_well_record_quality(
                df,
                years_to_extract,
                dt_col="season_year",
                spans_to_count_in=spans_to_count_in,
                unique_grouper=unique_grouper,
            )
        )
        indexers = []
        comparisons = []
        for table_col in table.columns:
            try:
                qc_col, cmp_operator = table_col.split()
            except:
                continue
            logger.debug(
                f"Found potential QC filter condition: {qc_col} {cmp_operator}"
            )
            if qc_col in qc.columns:
                indexer = []
                logger.debug("Yep, this QC filter condition is good to go")
                for i, (well_id, row) in enumerate(qc.iterrows()):
                    well_value = str(row[qc_col])
                    cmp_value = str(table.iloc[0][table_col])
                    cmp = " ".join([qc_col, cmp_operator, cmp_value])
                    cmp_code = " ".join([well_value, cmp_operator, cmp_value])
                    if i == 0:
                        comparisons.append(cmp)
                    logger.debug(f"WL Ranking QC :: {well_id} :: {cmp} :: {cmp_code}")
                    indexer.append(eval(cmp_code))
                indexers.append(indexer)
        retdf = pd.DataFrame(indexers, index=comparisons, columns=qc.index).T
        logger.debug(f"retdf contents - \n{retdf}")
        bool_qc = qc[
            [qc.columns[i] for i in range(len(qc.columns)) if qc.dtypes[i] == bool]
        ]
        logger.debug(f"qc contents - \n{qc}")
        logger.debug(f"bool_qc contents - \n{bool_qc}")
        retdf = pd.merge(bool_qc, retdf, left_index=True, right_index=True)
        logger.debug(f"retdf v2 contents - \n{retdf}")
        retdf["all_conditions"] = retdf.apply(
            lambda x: np.all(x == True), axis=1
        ).values
        return qc, retdf

    def test_wls_in_trend_period(self, df, min_obs=2, dt_col="obs_date"):
        """Test whether there are >= *min_obs* within the trend period for
        *df*.

        Args:
            df (pandas DataFrame): all water level data for a well
            min_obs (int): minimum number of observations to accept
            dt_col (str): column with datetimes of observations

        Returns: bool

        """
        start_y = int(str(self.trend_dfn.start_recovery_season)[:4])
        end_y = int(str(self.trend_dfn.end_recovery_season)[:4])
        sub_df = df[
            (df.season_year.astype(str).str[:4].astype(int) >= start_y)
            & (df.season_year.astype(str).str[:4].astype(int) <= end_y)
        ]
        if len(sub_df) > 1:
            return True
        else:
            return False

    def filter_wl_to_trend_period(self, df, dt_col="obs_date", wl_col="rswl"):
        """Filter WL data to the trend period defined for this resource.

        If this function is being applied to a dataframe, beware it might
        return an empty DataFrame. In that case, using it with

            >>> df.groupby('well_id').apply(resource.filter_wl_to_trend_period)

        might lead to errors. Instead, first run:

            >>> df = df.groupby('well_id').filter(resource.test_wls_in_trend_period)
            >>> df.groupby('well_id').apply(resource.filter_wl_to_trend_period)

        Args:
            df (pandas DataFrame): all water level data
            dt_col (str): column with datetime of observations
            wl_col (str): column with water level data.

        Returns:
            pandas DataFrame with data from the trend period, including
            a column for extreme values ("rswl_min" for wl_col "rswl")
            and the date of the latest extreme value ("rswl_min_date" for
            wl_col "rswl").

        """
        start_y = int(str(self.trend_dfn.start_recovery_season)[:4])
        end_y = int(str(self.trend_dfn.end_recovery_season)[:4])
        logger.debug(f"Filtering to trend period: {start_y} to {end_y}")
        sub_df = df[
            (df.season_year.astype(str).str[:4].astype(int) >= start_y)
            & (df.season_year.astype(str).str[:4].astype(int) <= end_y)
        ]
        hist_df = df[df.season_year.astype(str).str[:4].astype(int) <= end_y]
        extrema_df = hist_df[hist_df[wl_col] == hist_df[wl_col].min()].sort_values(
            dt_col, ascending=False
        )
        sub_df.loc[:, wl_col + "_min"] = extrema_df.iloc[0][wl_col]
        sub_df.loc[:, wl_col + "_min_date"] = extrema_df.iloc[0][dt_col]
        return sub_df[[c for c in sub_df.columns if not c.startswith("Unnamed")]]

    def filter_tds_to_wells_with_trend_period_data(
        self, df, dt_col="collected_date", well_id_col="well_id"
    ):
        """Filter data so that only wells which have at least two data
        point in the trend period are retained.

        Note this still returns a dataframe containing data *outside* the trend
        period. It just ensures that all wells in the dataframe have at least
        *two* points *inside* the trend period.

        """
        well_ids_with_data = df[
            (df[dt_col] >= pd.Timestamp(f"{int(self.trend_dfn.start_year)}-01-01"))
            & (df[dt_col] <= pd.Timestamp(f"{int(self.trend_dfn.end_year)}-12-31"))
        ][well_id_col].unique()
        return df[df[well_id_col].isin(well_ids_with_data)]

    def filter_tds_to_trend_period(self, df, dt_col="collected_date", sal_col="tds"):
        """Filter salinity data to the trend period defined for this resource.

        Args:
            df (pandas DataFrame): all salinity data
            dt_col (str): column with datetime of observations
            sal_col (str): column with salinity data.

        Returns:
            pandas DataFrame with data from the trend period, including
            a column for extreme values ("tds_max" for sal_col "tds")
            and the date of the latest extreme value ("tds_max_date" for
            sal_col "tds").

        """
        start_y = int(str(self.trend_dfn.start_year))
        end_y = int(str(self.trend_dfn.end_year))
        sub_df = df[(df[dt_col].dt.year >= start_y) & (df[dt_col].dt.year <= end_y)]
        hist_df = df[df[dt_col].dt.year <= end_y]
        extrema_df = hist_df[hist_df[sal_col] == hist_df[sal_col].max()].sort_values(
            dt_col, ascending=False
        )
        sub_df.loc[:, sal_col + "_max"] = extrema_df.iloc[0][sal_col]
        sub_df.loc[:, sal_col + "_max_date"] = extrema_df.iloc[0][dt_col]
        return sub_df[[c for c in sub_df.columns if not c.startswith("Unnamed")]]

    def apply_trend(
        self,
        ddf,
        well_id_col="well_id",
        param_col="auto",
        dt_col="ndays",
        extreme_val_col=None,
        extrema="auto",
    ):
        """Calculate the linear trend and apply the trend thresholds.

        Args:
            ddf (pandas DataFrame): data to calculate linear trend against.
            well_id_col (str): well_id column from *ddf* - this is used to select
                for well-specific trend thresholds from Definitions_triclass_trend_thresholds.xlsx
            param_col (str): 'auto' to select column automatically, should
                always be preferred
            dt_col (str): column to regress against
            extreme_val_col (str): column to compare the latest value against
            extrema (str):

        Returns:
            pandas Series (row) with columns from :func:`wrap_technote.linear_trend`
                and also "status_change", 'status_threshold', and 'status'

        """
        if well_id_col:
            well_id = ddf[well_id_col].unique()[0]
            trend_dfn = self.trend_dfn_for_well(well_id)
        else:
            trend_dfn = self.trend_dfn
        if param_col == "auto":
            if trend_dfn.param == "WL":
                param_col = "rswl"
                extrema = "min"
            elif trend_dfn.param == "TDS":
                param_col = "tds"
                extrema = "max"

        trend_line = linear_trend(ddf, param_col=param_col, dt_col=dt_col).to_dict()

        if trend_dfn.param == "WL":
            annual_slope_cm = trend_line["slope_yr"] * 100
            if annual_slope_cm >= trend_dfn.ann_rate_threshold:
                trend_line["status_change"] = increasing_codes[trend_dfn.param]
            elif annual_slope_cm <= (-1 * trend_dfn.ann_rate_threshold):
                trend_line["status_change"] = decreasing_codes[trend_dfn.param]
            else:
                trend_line["status_change"] = "Stable"

            # TODO: ADD COLUMN FOR "trend_class" and fill out...

            # TODO: check water level against a threshold e.g. historical extrema?
            trend_line["status_threshold"] = ""

        elif trend_dfn.param == "TDS":
            annual_slope_tds = trend_line["slope_yr"]
            start_dt = date(trend_dfn.start_year, 1, 1)
            end_dt = date(trend_dfn.end_year, 12, 31)
            period_length_years = (trend_dfn.end_year - trend_dfn.start_year) + 1

            start_sal, end_sal = calculate_trendline_at_dates(
                trend_line, [start_dt, end_dt]
            )
            if start_sal <= 0:
                logger.error(
                    f"Predicted starting TDS of {start_sal:.0f} mg/L at {start_dt} "
                    "is impossible; trend too steep for timeframe."
                )
                sal_change = np.nan
                pct_change = np.nan

            else:
                sal_change = end_sal - start_sal
                pct_change = sal_change / start_sal * 100

            trend_line["sal_change"] = sal_change
            trend_line["sal_pct_change"] = pct_change

            if np.isnan(sal_change):
                if trend_line["slope_yr"] > 0:
                    trend_line["status_change"] = "Increasing"
                elif trend_line["slope_yr"] < 0:
                    trend_line["status_change"] = "Decreasing"
            else:
                if pct_change >= (
                    trend_dfn.ann_pct_change_threshold * period_length_years
                ):
                    trend_line["status_change"] = "Increasing"
                elif pct_change <= (
                    -1 * (trend_dfn.ann_pct_change_threshold * period_length_years)
                ):
                    trend_line["status_change"] = "Decreasing"
                else:
                    trend_line["status_change"] = "Stable"

            # Check salinity against absolute threshold
            if trend_dfn.absolute_threshold:
                if end_sal >= trend_dfn.absolute_threshold:
                    trend_line[
                        "status_threshold"
                    ] = f"Above {trend_dfn.absolute_threshold:.0f} mg/L"
                else:
                    trend_line["status_threshold"] = ""

        if trend_line["status_threshold"]:
            trend_line[
                "status"
            ] = f"{trend_line['status_change']} ({trend_line['status_threshold']})"
        else:
            trend_line["status"] = trend_line["status_change"]

        trend_line.update(trend_dfn)

        return pd.Series(trend_line)

    def get_salinity_curr_pct_diff_qc_results(self, df, tdsdf=None):
        """Get the automatic criteria QC results for salinity curr_pct_diff results.

        Args:
            df (pd.DataFrame): `r.df` from `wrap_technote.calculate_salinity_indicator_results`
            tdsdf (pd.DataFrame): you can provide annual mean TDS here (relevant columns are
                "collected_year", "well_id", and "tds"), otherwise it will attempt to read
                from salinity_indicators__annual_mean_tds and if that fails

        Returns: tuple (df, qcdf) - *df* is an in-place modified version of *df* with
            "include_curr_pct_diff" and "validation_comment" fields filled out.

        """
        table = self.read_table("Definitions_salinity_indicators")
        cols = [c for c in table.columns if c.startswith("QC: ") or c == "resource_key"]
        table = table[cols].rename(columns={c: c.replace("QC: ", "") for c in cols})
        if tdsdf is None:
            try:
                tdsdf = self.read_data("salinity_indicators", "annual_mean_tds")
            except sqlite3.OperationalError:
                tds = resource.read_data("validated_data", "valid_data")
                tdsdf = tn.reduce_to_annual_tds(tds, reduction_func="mean")
        tdsdf["collected_date"] = pd.to_datetime(
            [f"{y:.0f}-06-30" for y in tdsdf.collected_year]
        )

        years_to_extract = []

        spans_to_count_in = [
            [int(x) for x in c.split()[0].split("_")[-2:]]
            for c in table.columns
            if c.strip().startswith("n_obs_btwn_")
        ]

        logger.debug(f"spans_to_count_in: {spans_to_count_in}")
        qc = tdsdf.groupby("well_id").apply(
            lambda df: calc_well_record_quality(
                df,
                years_to_extract,
                spans_to_count_in=spans_to_count_in,
                dt_col="collected_date",
            )
        )
        indexers = []
        comparisons = []
        for table_col in table.columns:
            try:
                qc_col, cmp_operator = table_col.split()
            except:
                continue
            logger.debug(
                f"Found potential QC filter condition: {qc_col} {cmp_operator}"
            )
            if qc_col in qc.columns:
                indexer = []
                logger.debug("Yep, this QC filter condition is good to go")
                for i, (well_id, row) in enumerate(qc.iterrows()):
                    well_value = str(row[qc_col])
                    cmp_value = str(table.iloc[0][table_col])
                    cmp = " ".join([qc_col, cmp_operator, cmp_value])
                    cmp_code = " ".join([well_value, cmp_operator, cmp_value])
                    if i == 0:
                        comparisons.append(cmp)
                    logger.debug(f"QC :: {well_id} :: {cmp} :: {cmp_code}")
                    indexer.append(eval(cmp_code))
                indexers.append(indexer)
        retdf = pd.DataFrame(indexers, index=comparisons, columns=qc.index).T
        retdf["meets_qc_requirements"] = retdf.apply(
            lambda x: np.all(x == True), axis=1
        ).values
        qc_results = pd.merge(qc, retdf, left_index=True, right_index=True)

        if not "validation_comment" in df:
            df["validation_comment"] = ""

        for well_id, qc_row in qc_results[
            (qc_results.meets_qc_requirements == False).values
        ].iterrows():
            reason = "curr_pct_diff excluded due to: "
            qc_reasons = []
            for col, value in qc_row.items():
                if value is False and not col == "meets_qc_requirements":
                    v = qc_row.loc[col.split()[0]]
                    qc_reasons.append(f"{col} (= {v})")
            reason += ", ".join(qc_reasons) + " (QC)"
            logger.debug(f"Excluding {well_id}, reason: {reason}")
            df.loc[df.well_id == well_id, "include_curr_pct_diff"] = False
            df.loc[df.well_id == well_id, "validation_comment"] = (
                df.loc[df.well_id == well_id, "validation_comment"] + "\n" + reason
            )
        df["validation_comment"] = [str(x).strip("\n") for x in df.validation_comment]

        if len(qc_results) == 0:
            qc_results = pd.DataFrame(columns=["well_id", "meets_qc_requirements"])

        return df, qc_results

    def get_salinity_trend_pct_qc_results(self, df, tdsdf=None):
        """Get the automatic criteria QC results for salinity trend_pct results.

        Args:
            df (pd.DataFrame): `r.df` from `wrap_technote.calculate_salinity_indicator_results`
            tdsdf (pd.DataFrame): you can provide annual mean TDS here (relevant columns are
                "collected_year", "well_id", and "tds"), otherwise it will attempt to read
                from salinity_indicators__annual_mean_tds and if that fails

        Returns: tuple (df, qcdf) - *df* is an in-place modified version of *df* with
            "include_trend_pct" and "validation_comment" fields filled out.

        """
        table = self.read_table("Definitions_salinity_indicators")
        dfn = table.iloc[0]
        if tdsdf is None:
            try:
                tdsdf = self.read_data("salinity_indicators", "annual_mean_tds")
            except sqlite3.OperationalError:
                tds = self.read_data("validated_data", "valid_data")
                tdsdf = reduce_to_annual_tds(tds, reduction_func="mean")
        tdsdf["collected_date"] = pd.to_datetime(
            [f"{y:.0f}-06-30" for y in tdsdf.collected_year]
        )

        curr_year = tdsdf.collected_year.max()
        first_year = curr_year - (dfn.trend_length_years - 1)

        years_to_extract = []
        spans_to_count_in = [(first_year, curr_year)]

        logger.debug(f"spans_to_count_in: {spans_to_count_in}")
        qc = tdsdf.groupby("well_id").apply(
            lambda df: calc_well_record_quality(
                df,
                years_to_extract,
                spans_to_count_in=spans_to_count_in,
                dt_col="collected_date",
            )
        )
        if len(qc):
            result_col = [c for c in qc.columns if c.startswith("n_obs_btwn")][0]
            qc["meets_qc_requirements"] = qc[result_col] >= dfn.trend_min_data_pts

            if not "validation_comment" in df:
                df["validation_comment"] = ""
            for well_id, qc_row in qc[
                (qc.meets_qc_requirements == False).values
            ].iterrows():
                reason = f"trend_pct excluded as {result_col} ({qc_row[result_col]}) < {dfn.trend_min_data_pts} (QC)"
                qc_reasons = []
                logger.debug(f"Excluding {well_id}, reason: {reason}")
                df.loc[df.well_id == well_id, "include_trend_pct"] = False
                df.loc[df.well_id == well_id, "validation_comment"] = (
                    df.loc[df.well_id == well_id, "validation_comment"] + "\n" + reason
                )
            df["validation_comment"] = [
                str(x).strip("\n") for x in df.validation_comment
            ]

        if len(qc) == 0:
            qc = pd.DataFrame(columns=["well_id", "meets_qc_requirements"])

        return df, qc

    def apply_salinity_indicator_validations(self, df, conn=None):
        """Apply salinity_indicator_validations.

        Args:
            df (pd.DataFrame): `r.df` from `wrap_technote.calculate_salinity_indicator_results`

        Returns: *df* which is modified in-place.

        """
        if conn is None:
            import dew_gwdata

            conn = dew_gwdata.sageodata()

        valsdf = self.read_table("Data_validation")
        vals = valsdf[valsdf.parameter == "TDS"]
        for idx, row in vals.iterrows():
            row_well_ids = conn.find_wells(row.well_id)
            if len(row_well_ids) == 0:
                logger.warning(f"No drillhole identified for data_validation row {row}")
                continue
            row_well_ids = conn.drillhole_details(row_well_ids.dh_no).well_id
            reason = f"{row.action}: {row.comment} ({row.username})"
            action = row.action

            logger.debug(f"Checking TDS validation rule for {row.well_id}")
            if action == "Exclude well trend":
                logger.debug(
                    "Interpreting 'Exclude well trend' as 'Exclude long-term indicator and trend'"
                )
                action = "Exclude long-term indicator and trend"

            if action == "Exclude well entirely" or action == "Exclude well":
                # also remove from current tds...
                df.loc[df.well_id.isin(row_well_ids), "include_curr_pct_diff"] = False
                df.loc[df.well_id.isin(row_well_ids), "include_trend_pct"] = False
                logger.debug(f"Removed curr_pct_diff result for {row_well_ids}")
                logger.debug(f"Removed trend_pct result for {row_well_ids}")
                append_comment_to_dataframe_column(
                    df, df.well_id.isin(row_well_ids), "validation_comment", reason
                )
            elif action == "Exclude long-term indicator":
                df.loc[df.well_id.isin(row_well_ids), "include_curr_pct_diff"] = False
                append_comment_to_dataframe_column(
                    df, df.well_id.isin(row_well_ids), "validation_comment", reason
                )
                logger.debug(f"Removed curr_pct_diff result for {row_well_ids}")
            elif action == "Exclude long-term indicator and trend":
                df.loc[df.well_id.isin(row_well_ids), "include_curr_pct_diff"] = False
                df.loc[df.well_id.isin(row_well_ids), "include_trend_pct"] = False
                append_comment_to_dataframe_column(
                    df, df.well_id.isin(row_well_ids), "validation_comment", reason
                )
                logger.debug(f"Removed curr_pct_diff result for {row_well_ids}")
                logger.debug(f"Removed trend_pct result for {row_well_ids}")
            elif action == "Exclude trend only":
                df.loc[df.well_id.isin(row_well_ids), "include_trend_pct"] = False
                append_comment_to_dataframe_column(
                    df, df.well_id.isin(row_well_ids), "validation_comment", reason
                )
                logger.debug(f"Removed trend_pct result for {row_well_ids}")
        return df

    def get_summary_of_wells(self, **kwargs):
        """Get summary dataframe of wells for this resource."""
        if self.resource_key.endswith("WL"):
            return self.get_summary_of_wells_for_wl_resource(**kwargs)
        elif self.resource_key.endswith("TDS"):
            return self.get_summary_of_wells_for_tds_resource(**kwargs)

    def get_summary_of_wells_for_wl_resource(self, conn=None):
        valid = self.read_data("validated_data", "valid_data")
        invalid = self.read_data("validated_data", "invalid_data")
        ranks1 = self.read_data("recovery_wl_data", "ranked_wls")
        ranks2 = self.read_data("recovery_wl_data", "ranks_excl")
        ranks = pd.concat([ranks1, ranks2])
        curr_ranks = self.read_data("recovery_wl_data", "current_ranked_wls")
        trends = self.read_data("recovery_wl_trends", "final_trends")
        excl_trends = self.read_data("recovery_wl_trends", "trend_qc")

        valid_wls = valid.groupby("well_id").rswl.count().rename("num_valid_wls")
        invalid_wls = invalid.groupby("well_id").rswl.count().rename("num_invalid_wls")
        rank_lims = (
            ranks.groupby("well_id")
            .season_year.agg(["min", "count"])
            .rename(columns={"min": "first_ranked_wl", "count": "num_years_ranked"})
        )
        curr_ranks_info = curr_ranks.set_index("well_id")[["rswl_bom_class"]].rename(
            columns={"rswl_bom_class": "bom_ranking"}
        )
        trend_info = trends.set_index("well_id")[["slope_yr", "status_change"]].rename(
            columns={"slope_yr": "trend_m_y", "status_change": "trend_triclass_status"}
        )
        excl_trend_info = excl_trends.set_index("well_id")[["exclusion_reason"]].rename(
            columns={"exclusion_reason": "trend_excl_reason"}
        )

        df = pd.concat(
            [
                valid_wls,
                invalid_wls,
                rank_lims,
                curr_ranks_info,
                trend_info,
                excl_trend_info,
            ],
            axis=1,
            sort=True,
        )
        if conn:
            details = conn.drillhole_details(conn.find_wells(str(list(df.index))))
            df = pd.merge(
                details.set_index("well_id")[["unit_hyphen", "dh_name"]],
                df,
                left_index=True,
                right_index=True,
            )
        return df.sort_index().fillna("").round(2)

    def get_summary_of_wells_for_tds_resource(self, conn=None):
        valid = self.read_data("validated_data", "valid_data")
        invalid = self.read_data("validated_data", "invalid_data")
        curr_tds = self.read_data("validated_data", "current_mean_tds")
        trends = self.read_data("salinity_trends", "final_trends")
        excl_trends = self.read_data("salinity_trends", "excluded_trends")

        valid_tds = valid.groupby("well_id").tds.count().rename("num_valid_tds")
        invalid_tds = invalid.groupby("well_id").tds.count().rename("num_invalid_tds")
        curr_tds_info = curr_tds.set_index("well_id")[["tds"]].rename(
            columns={"tds": "curr_mean_tds"}
        )
        trend_info = trends.set_index("well_id")[
            ["slope_yr", "sal_pct_change", "status_change"]
        ].rename(
            columns={
                "slope_yr": "trend_mg_L_y",
                "sal_pct_change": "trend_pd_pct_change",
                "status_change": "trend_triclass_status",
            }
        )
        excl_trend_info = excl_trends.set_index("well_id")[["exclusion_reason"]].rename(
            columns={"exclusion_reason": "trend_excl_reason"}
        )

        df = pd.concat(
            [
                valid_tds,
                invalid_tds,
                curr_tds_info,
                trend_info,
                excl_trend_info,
            ],
            axis=1,
            sort=True,
        )
        if conn:
            details = conn.drillhole_details(conn.find_wells(str(list(df.index))))
            df = pd.merge(
                details.set_index("well_id")[["unit_hyphen", "dh_name"]],
                df,
                left_index=True,
                right_index=True,
            )
        return df.sort_index().fillna("").round(2)


class AggregateGroundwaterResource:
    """

    .. todo::

        document the AggregateGroundwaterResource class.


    """

    def __init__(
        self, aggregate_resource_key, reporting_period=CURRENT_RPERIOD, param=None
    ):
        if not isinstance(reporting_period, ReportingPeriod):
            reporting_period = load_reporting_period(reporting_period)
            self.reporting_period = reporting_period
        else:
            self.reporting_period = reporting_period
        self.aggregate_resource_key = aggregate_resource_key
        self.param = param

    def read_table(self, filename):
        """
        .. todo:: document the read_table method

        """
        logger.debug(f"Reading table: {filename}")
        df = self.reporting_period.read_table(filename)
        if "aggregate_resource_key" in df:
            return df[df.aggregate_resource_key == self.aggregate_resource_key]
        else:
            return df

    @property
    def dfn_table(self):
        """

        .. todo:: document this property"""
        return self.read_table("GW_Aggregate_resource_definitions")

    def resource_keys(self, param=None):
        """

        .. todo:: document this method

        """
        if param is None:
            param = self.param
        if param is None:
            return set(self.dfn_table.resource_key.unique())
        else:
            return set(self.dfn_table[lambda x: x.param == param].resource_key.unique())

    def read_data(self, workbook_name, worksheet_name=None, param=None):
        """Get a concatenated pandas DataFrame for
        an aggregate resource.

        Args:
            param (str): either "WL" or "TDS"
            workbook_name (str): data spreadsheet to go to e.g. either
                "recovery_wl_data", "recovery_wl_trends", or "salinity_trends", or
                "validated data"
            worksheet_name (str): worksheet to retrieve.

        Returns:
            df (pd.DataFrame): a single dataframe.

        """
        if "__" in workbook_name:
            workbook_name, worksheet_name = workbook_name.split("__")
        if param is None:
            logger.debug(
                f"param=None; self.param={self.param}; workbook_name={workbook_name} worksheet_name={worksheet_name}"
            )
            if self.param:
                param = self.param
            elif "wl_" in workbook_name:
                param = "WL"
            elif "salinity_" in workbook_name:
                param = "TDS"
            else:
                raise KeyError(f'param must be either "WL" or "TDS"')

        result = {}
        logger.debug(f"Loading aggregate resources for {param}")
        resource_keys = self.resource_keys(param=param)
        logger.debug(f"Aggregate resources are:\n{resource_keys}")
        dfs = read_data(
            resource_keys,
            workbook_name,
            worksheet_name,
            reporting_period=self.reporting_period,
        )
        concat_dfs = []
        for resource_key, df in dfs.items():
            df["resource_key"] = resource_key
            df = df[
                ["resource_key"] + [c for c in df.columns if not c == "resource_key"]
            ]
            concat_dfs.append(df)
        return pd.concat(concat_dfs)


def read_data(
    resource_keys, workbook_name, worksheet_name, reporting_period=CURRENT_RPERIOD
):
    """Get a dictionary of pandas DataFrames for resource_keys.

    Args:
        resource_keys (list): list of resource_keys.
        workbook_name (str): data table to go to e.g. either
            "recovery_wl_data", "recovery_wl_trends", or "salinity_trends", or
            "validated data"
        worksheet_name (str): worksheet to retrieve.

    Returns:
        dict: a dictionary; the key is the resource key and the value
        is the data as a pandas dataframe.

    """
    dfs = {}
    resource_dfs = {}
    logger.debug(
        f"reading data sheets for multiple resource_keys: "
        f"(sheet {workbook_name} :: {worksheet_name})"
    )
    for resource_key in set(resource_keys):
        logger.debug(f"... resource_key {resource_key}")
        resource = load_resource(resource_key, reporting_period)
        try:
            trends = resource.read_data(workbook_name, sheet_name=worksheet_name)
        except:
            logger.warning(
                f"Error reading data for resource={resource.resource_key} workbook_name={workbook_name} worksheet_name={worksheet_name}. Skipping."
            )
        else:
            resource_dfs[resource_key] = trends
    return resource_dfs


ReportingPeriodReport = Report
ReportingPeriodResource = Resource
