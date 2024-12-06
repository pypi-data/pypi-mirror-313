from datetime import datetime
import io
import logging
import os
import contextlib
from pathlib import Path
import sys

from loguru import logger as loguru_logger
import numpy as np
from PIL import Image, ImageChops
import geopandas as gpd
import pandas as pd


def get_logger():
    """Get a logging object (adds stderr for warning logger messages.

    Returns:
        loguru.Logger: logger suitable for use anywhere in wrap_technote.

    .. todo:: add sinks to a database for simple logging output.

    """
    from loguru import logger

    logger.remove()
    logger.add(sys.stderr, level="WARNING")
    return logger


logger = get_logger()


class Run:
    """Run an analysis.

    This is a parent class to be inherited. See, for example,
    :class:`wrap_technote.waterlevels.QueryAndValidateWaterLevels`.


    Args:
        log_to (func, or None): function which accept a single string.
        log_level (str): logging level to use.

    Other keyword arguments will be part of the initial data for the
    first step of the analysis; see subclasses.

    """

    def __init__(self, log_to=None, log_level="DEBUG", **kwargs):
        self.log_to = log_to
        self.log_level = log_level
        self.steps = []

        self.data = kwargs

    def if_then_use(self, data_variable_name, func):
        """Tool for constructing child classes.

        Args:
            data_variable_name (bool): key to self.data which should be tested
            func (function): the method to run or skip based on condition

        Returns:
            a function or a tuple of name, function - see :meth:`wrap_technote.Run.append_step`
            for more details on how this is parsed.

        """
        test_func = (
            lambda **kwargs: func(**kwargs) if self.data[data_variable_name] else {}
        )
        name = func.__name__
        return (name, test_func)

    def append_step(self, func):
        """Add an analysis step.

        Args:
            func (function or tuple of str, function): the analysis
                function; if it is an anonymous function (lambda), then
                you can provide a tuple where the first item is a string
                and the second item is the function.

        """
        if isinstance(func, tuple):
            name = func[0]
            function = func[1]
        else:
            function = func
            name = func.__name__
        step = Step(function, log_level=self.log_level, additional_log_to=self.log_to)
        step.name = name
        self.steps.append(step)

    def run_steps(self, first=0, last=None):
        """Execute analysis steps.

        Args:
            first (int): the first analysis step to execute (starting from
                zero)
            last (int): the last (inclusive) analysis step to execute

        Note that if you omit early step, it's likely later ones will
        fail due to the data not being generated and cached.

        """
        if last is None:
            last = len(self.steps) - 1

        logger.info(f"Running {self.__class__.__name__} steps {first} through {last}")
        for i, step in enumerate(self.steps):
            if i >= first and i <= last:
                logger.info(f"running step {i} {step.name}")
                step.run(self.data)
                logger.debug(
                    f"step {i} {step.name} returned data: {step.returned_data.keys()}"
                )
            self.data.update(step.returned_data)
        logger.info(f"Completed {self.__class__.__name__} steps {first} through {last}")


class Step:
    """Analysis step.

    Args:
        function
        log_level (str): logging to undertake.

    """

    def __init__(self, function, log_level="DEBUG", additional_log_to=None):
        self.log_level = log_level
        self.function = function
        self.name = self.function.__name__
        self.returned_data = {}
        self.log_messages = []
        self.additional_log_to = additional_log_to

    def log_message(self, msg):
        """Log a message both internally and to the additional logger if supplied."""
        self.log_messages.append(msg)
        if self.additional_log_to:
            self.additional_log_to(msg)

    def print_logs(self, output_stream=None, package=None):
        """Print log messages."""
        if output_stream is None:
            output_stream = sys.stdout
        messages = self.log_messages
        if package is None:
            messages = self.log_messages
        else:
            messages = [m for m in self.log_messages if package in m.splitlines()[0]]
        output_stream.write("\n".join(messages))

    def run(self, data):
        """Run the analysis step.

        This function adds a temporary logger to capture the step's details.

        """
        logger_id = loguru_logger.add(self.log_message, level=self.log_level)

        returned = self.function(**data)

        loguru_logger.remove(logger_id)

        if returned is None:
            returned = {}
        self.returned_data = returned


class DataFileDict(dict):
    """A dictionary where keys have spaces replaced by underscores
    transparently.

    """

    def __getitem__(self, key):
        key = key.lower().replace(" ", "_")
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        key = key.lower().replace(" ", "_")
        return super().__setitem__(key, value)


def intround(value):
    """Convert value to an integer."""
    return int(np.round(value))


def percentile_to_bom_class(values, fractional=False):
    """Convert percentile ranking to the BoM class.

    Args:
        values (sequence of numbers): the percentiles
        fractional (bool): whether the percentiles are 0-1 (True)
            or 0-100 (False).

    Returns:
        numpy.ndarray: string values either
        "Highest on record", "Very much above average", "Above average",
        "Average", "Below average", "Very much below average", or
        "Lowest on record"

    """
    values = np.asarray(values)
    if not fractional:
        values = values / 100.0
    min_value = np.nanmin(values)
    max_value = np.nanmax(values)
    results = []
    for value in values:
        if value == max_value:
            results.append("Highest on record")
        elif value == min_value:
            results.append("Lowest on record")
        else:
            if value < 0.1:
                results.append("Very much below average")
            elif value < 0.3:
                results.append("Below average")
            elif value < 0.7:
                results.append("Average")
            elif value < 0.9:
                results.append("Above average")
            elif value <= 1:
                results.append("Very much above average")
            elif np.isnan(value):
                results.append("No data")
            else:
                raise Exception(
                    "It should be impossible to get to this point in the code."
                )
    return np.asarray(results)


def map_percentile_into_bom_class(value, fractional=False):
    """Convert percentile to BoM classification.

    Args:
        value (float): the percentile - either between 0 and 100, or, if fractional
            is True, between 0 and 1
        fractional (bool): whether percentiles are out of 1 or 100

    Returns:
        str: the relevant BoM classification (out of 'Lowest on record',
        'Very much below average', 'Below average', 'Average',
        'Above average', 'Very much above average', or 'Highest on record').

    """
    if not fractional:
        value = value / 100.0
    if value == 0:
        return "Lowest on record"
    elif value < 0.1:
        return "Very much below average"
    elif value < 0.3:
        return "Below average"
    elif value < 0.7:
        return "Average"
    elif value < 0.9:
        return "Above average"
    elif value < 1:
        return "Very much above average"
    elif value == 1:
        return "Highest on record"


def round_to_100_percent(number_set, digit_after_decimal=0):
    """Convert a set of percentages
    which add up to 100% but no longer add up to 100 when rounded, to
    numbers which when rounded add up to 100. The excess/deficit is distributed
    using the algorithm described below.

    Args:
        number_set (sequence of X numbers)
        digit_after_decimal (int): how many decimals to round to, e.g.
            0 means the function will return integers.

    Returns:
        list: X numbers rounded according to digit_after_decimal

    From https://stackoverflow.com/q/25271388:

        This function take a list of number and return a list of percentage, which
        represents the portion of each number in sum of all numbers
        Moreover, those percentages are adding up to 100%!!!
        Notice: the algorithm we are using here is 'Largest Remainder'
        The down-side is that the results won't be accurate, but they are never
        accurate anyway:)

    """
    if np.sum(number_set) == 0:
        unround_numbers = [0 for x in number_set]
    else:
        unround_numbers = [
            x / float(np.sum(number_set)) * 100 * 10**digit_after_decimal
            for x in number_set
        ]
    decimal_part_with_index = sorted(
        [(index, unround_numbers[index] % 1) for index in range(len(unround_numbers))],
        key=lambda y: y[1],
        reverse=True,
    )
    remainder = 100 * 10**digit_after_decimal - np.sum(
        [int(x) if not np.isnan(x) else 0 for x in unround_numbers]
    )
    index = 0
    while remainder > 0:
        unround_numbers[decimal_part_with_index[index][0]] += 1
        remainder -= 1
        index = (index + 1) % len(number_set)
    return [
        (int(x) if not np.isnan(x) else np.nan) / float(10**digit_after_decimal)
        for x in unround_numbers
    ]


"""Reference lists for the BoM percentile classifications."""
bom_classes = list(percentile_to_bom_class([0, 5, 20, 50, 80, 95, 100]))
bom_classes_index = [bom_classes.index(x) for x in bom_classes]


def chunk(l, n=1000):
    """Yield successive n-sized chunks from a list l.

    Args:
        l (sequence)
        n (int)

    Returns:
        iterator: each iteration yields a list of length <= n

    .. code-block:: python

        >>> from dew_gwdata.utils import chunk
        >>> for x in chunk([0, 1, 2, 3, 4], n=2):
        ...     print(x)
        [0, 1]
        [2, 3]
        [4]

    """
    y = 0
    for i in range(0, len(l), n):
        y += 1
        yield l[i : i + n]
    if y == 0:
        yield l


class add_import_path:
    """Context manager for adding a path to sys.path temporarily."""

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass


def df_to_shp(
    df,
    filename,
    x_col="longitude",
    y_col="latitude",
    convert_dt_cols=True,
    from_crs="epsg:7844",
    to_crs="epsg:8059",
    **kwargs,
):
    """Save a DataFrame as a shapefile.

    Args:
        df (pd.DataFrame): must have X and Y coordinates as columns
        filename (str): shapefile filename to create
        x_col (str): column of df with x coordinates
        y_col (str): column of df with y coordinates
        convert_dt_cols (bool): convert datetimes to string before
            writing, otherwise they are converted to epoch timestamps
            in the shapefile (not very useful!)
        from_crs (str): coordinate  system in df
        to_crs (str): coordinate system desired for shapefile

    Returns:
        nothing

    Other kwargs are passed to the geopandas.GeoDataFrame constructor.

    """
    if "crs" in kwargs:
        logger.warning('Please use the kwargs "from_crs" and "to_crs" instead of "crs"')
    if len(df):
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df[x_col], df[y_col]),
            crs=from_crs,
            **kwargs,
        )
        gdf = gdf.to_crs(to_crs)
        if convert_dt_cols:
            for col in gdf.columns:
                value = gdf[col].iloc[0]
                if isinstance(value, datetime):
                    gdf[col] = gdf[col].astype(str)
        gdf.to_file(
            filename,
            driver="ESRI Shapefile",
        )


@contextlib.contextmanager
def cd(newdir):
    """Context manager for changing directory temporarily."""
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def append_comment_to_dataframe_column(df, indexer, column, comment):
    """Append a comment to rows from a dataframe.

    Args:
        df (pd.DataFrame): will be modified in-place.
        indexer (boolean pd.Series): e.g. df.well_id == 'ANG010'
        column (str): column for comment
        comment (str): comment to append to any existing values.

    Returns:
        pd.DataFrame: df containing changes (the modification happens in place)

    """
    if not column in df:
        df.loc[indexer, column] = comment
    else:
        df.loc[indexer, column] = df[indexer][column] + "\n" + comment
        df[column] = [v.strip("\n") if v == str(v) else v for v in df[column]]
    return df


def highlight_fields(lines, highlight_method=None):
    """Highlight fields in strings.

    Args:
        lines (sequence): list of strings
        highlight_method (str): either a symbol or colour

    Returns:
        list: the strings submitted, with fields replaced

    So for example if highlight_method = "blue", then this will
    replace lines like "the cat is <|angry|> today" with
    "the cat is <span style='background: blue'>angry</span> today"

    """
    if not highlight_method:
        replacements = []
    elif highlight_method[0] in ("*", "_", "`"):
        replacements = [("<|", highlight_method), ("|>", highlight_method)]
    else:
        replacements = [
            ("<|", f"<span style='background: {highlight_method}'>"),
            ("|>", "</span>"),
        ]
    new_lines = []
    for line in lines:
        for repl_args in replacements:
            line = str(line).replace(*repl_args)
        new_lines.append(line)
    return new_lines


def df_for_sql(df, *args, **kwargs):
    for column in df.columns:
        if column.endswith("_date"):
            df[column] = pd.to_datetime(df[column])
    return df
