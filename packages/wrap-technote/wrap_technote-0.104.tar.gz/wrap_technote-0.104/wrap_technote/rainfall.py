import collections
from pathlib import Path
import logging
import io
import sqlite3

# import datatest
import numpy as np
import pandas as pd
import requests

import ausweather

# import pytest
import wrap_technote as tn


from .utils import *

logger = get_logger()


class RainfallStationData:
    """Rainfall station data.

    You should initialise this by using any of these class methods:

    - :meth:`wrap_technote.RainfallStationData.from_bom_via_silo`
    - :meth:`wrap_technote.RainfallStationData.from_aquarius`
    - :meth:`wrap_technote.RainfallStationData.from_wrap_report`
    - :meth:`wrap_technote.RainfallStationData.from_data`

    e.g.

    .. code-block::

        >>> rf = tn.RainfallStationData.from_bom_via_silo('18017')

    You can then access data via the ``rf.daily``, ``rf.calendar``, or
    ``rf.financial`` attributes.

    Args:
        station_id (str): station ID
        exclude_incomplete_years (bool): only show complete years

    """

    def __init__(self, station_id, exclude_incomplete_years=False):
        self.station_id = station_id
        self.exclude_incomplete_years = False

    @property
    def exclude_incomplete_years(self):
        return self.__exclude_incomplete_years

    @exclude_incomplete_years.setter
    def exclude_incomplete_years(self, value):
        if value:
            self.__exclude_incomplete_years = True
        else:
            self.__exclude_incomplete_years = False

    @classmethod
    def from_bom_via_silo(cls, station_id, data_start=None):
        """Create from BoM data (via SILO).

        Args:
            station_id (str): BoM Station ID
            data_start (pd.Timestamp): date to download data from, default 1/1/1950

        Returns:
            :class:`wrap_technote.RainfallStationData`

        Note that this will download the data afresh from the SILO website.

        """
        if data_start is None:
            data_start = pd.Timestamp("1950-01-01")
        self = cls(station_id)
        self.df = download_bom_rainfall(station_id, data_start)
        return self

    @classmethod
    def from_aquarius(cls, station_id, data_start=None):
        """Create from Aquarius Timeseries data (for South Australia only)

        Args:
            station_id (str): AQTS LocationIdentifier.
            data_start (pd.Timestamp): date to download data from, default 1/1/1950

        Returns:
            :class:`wrap_technote.RainfallStationData`

        Note that this will download the data afresh from AQTS.

        """
        if data_start is None:
            data_start = pd.Timestamp("1950-01-01")
        self = cls(station_id)
        self.df = download_aquarius_rainfall(station_id, data_start)

        return self

    @classmethod
    def from_wrap_report(cls, station_id, report):
        """Create from WRAP Report dataset.

        Args:
            report (:class:`wrap_technote.Report`)
            station_id (str):

        Returns:
            :class:`wrap_technote.RainfallStationData`

        This will not download data, but instead (attempt to)
        retrieve it from the already-downloaded WRAP report
        SQLite database. The download would have occurred when
        somebody ran the ``wraptn rainfall ...`` command-line
        script.

        """
        self = cls(station_id)
        dfn = report.rainfall_dfn(self.station_id)
        data = report.get_rainfall_data(id=station_id, sheet=None)
        self.df = data["daily"]
        return self

    @property
    def daily(self):
        """Daily rainfall data.

        Returns:
            :class:`pandas.DataFrame`: dataframe with columns:

            - date (pd.Timestamp)
            - rainfall (float)
            - interpolated_code (int)
            - quality (int)
            - year (int)
            - dayofyear (int)
            - finyear (str)
            - station_id (str)

        """
        df = self.df.assign(station_id=self.station_id)
        return df

    @property
    def calendar(self):
        df = self.groupby("year").assign(station_id=self.station_id)
        df.insert(1, "start_date", [pd.Timestamp(f"{y}-01-01") for y in df.year])
        if self.exclude_incomplete_years:
            missing = tn.find_missing_days(
                self.daily, dt_col="date", year_type="calendar", value_col="rainfall"
            )
            complete = missing[missing == 0]
            df = df[df.year.isin(complete.index.values)]
        return df

    @property
    def financial(self):
        df = self.groupby("finyear").assign(station_id=self.station_id)
        df.insert(1, "start_date", [pd.Timestamp(f"{y[:4]}-07-01") for y in df.finyear])
        if self.exclude_incomplete_years:
            missing = tn.find_missing_days(
                self.daily, dt_col="date", year_type="financial", value_col="rainfall"
            )
            complete = missing[missing == 0]
            df = df[df.finyear.isin(complete.index.values)]
        return df

    def groupby(self, grouping_column):
        """Group daily rainfall by either calendar or financial year.

        Args:
            grouping_column (str): either 'year' or 'finyear'

        Returns:
            :class:`pandas.DataFrame`: dataframe with these columns:

            - year or finyear (str)
            - rainfall (float): rainfall in mm
            - rainfall_count (int): number of days with data
            - interpolated_count (int): number of days with interpolated_code != 0
            - quality_count (int): number of days with non-null quality code.

        """
        assert grouping_column in self.df.columns
        return self.df.groupby(grouping_column, as_index=False).agg(
            rainfall=("rainfall", "sum"),
            rainfall_count=("rainfall", "count"),
            interpolated_count=(
                "interpolated_code",
                lambda x: len([xi for xi in x if xi != 0]),
            ),
            quality_count=(
                "quality",
                lambda x: len([xi for xi in x if not pd.isnull(xi)]),
            ),
        )

    def save_to_excel(self, report=None, fn=None, overwrite=True):
        """Save data to Excel.

        Args:
            report (:class:`wrap_technote.Report`): used to derive the filename path
            fn (str): you can pass this directly if you wish
                overwrite (bool)

        """
        d = convert_daily_to_old_style_rainfall_sheets(self.daily)

        if fn is None:
            dfn = report.rainfall_dfn(self.station_id)
            stub = str(self.station_id) + "_" + dfn.station_name
            excel_filename = (
                report.rainfall_path / f"aquarius_data_{report.report_key}_{stub}.xlsx"
            )
        else:
            excel_filename = Path(fn)
        if overwrite:
            with pd.ExcelWriter(excel_filename) as writer:
                d["df"].to_excel(writer, "daily", index=False)
                d["annual"].reset_index().to_excel(
                    writer, "annual (calendar)", index=False
                )
                d["srn"].reset_index().rename(columns={"year": "Date"}).to_excel(
                    writer, "annual provenance", index=False
                )
                d["wateruse_year"].reset_index().to_excel(
                    writer, "annual (water-use year)", index=False
                )

    def save_to_database(self, report):
        """Save data to a SQLite database in the rainfall folder of a WRAP report.

        Args:
            report (:class:`wrap_technote.Report`): used to derive the filename path

        """
        fn = report.rainfall_path / f"rainfall_data_{report.report_key}.db"
        # with sqlite3.connect(fn) as db:
        from sqlalchemy import create_engine

        db = create_engine("sqlite:///" + str(fn))  # C:\\path\\to\\foo.db")
        if 1:
            for table in ("daily", "calendar", "financial"):
                logger.info(f"Saving '{table}'")
                try:
                    dbdf = pd.read_sql(f"select * from {table}", db)
                    dbdf = dbdf[~(dbdf.station_id == str(self.station_id))]
                    new_dbdf = pd.concat([dbdf, getattr(self, table)])
                    logger.info(f"Joined existing stations to {self.station_id}")
                except:
                    new_dbdf = getattr(self, table)
                    logger.info(f"Nothing in database (error) - using df direct.")
                finally:
                    if "date" in new_dbdf.columns:
                        new_dbdf["date"] = pd.to_datetime(new_dbdf["date"]).dt.strftime(
                            "%Y-%m-%d"
                        )
                    if "date_start" in new_dbdf.columns:
                        new_dbdf["date_start"] = pd.to_datetime(
                            new_dbdf["date_start"]
                        ).dt.strftime("%Y-%m-%d")
                    if "start_date" in new_dbdf.columns:
                        new_dbdf["start_date"] = pd.to_datetime(
                            new_dbdf["start_date"]
                        ).dt.strftime("%Y-%m-%d")
                    for i, column in enumerate(new_dbdf.columns):
                        series = new_dbdf[column]
                        example = series.iloc[0]
                        logger.info(
                            f"Column {i} {column} dtype = {series.dtype} {type(example)}"
                        )
                    new_dbdf.to_sql(table, db, index=False, if_exists="replace")


def download_bom_rainfall(station_id, data_start):
    """Download BoM rainfall data from SILO.

    Args:
        station_id (int or str): BoM station ID
        data_start (pd.Timestamp): date to download data from

    Returns:
        dict: Has four keys: 'df', 'annual', 'srn', and 'wateruse_year'

    This function uses :func:`ausweather.fetch_bom_station_from_silo`
    in the background.

    """
    station_id = int(f"{float(station_id):.0f}")
    logger.debug(f"Downloading {station_id} from {data_start}")

    data = ausweather.fetch_bom_station_from_silo(
        station_id, "groundwater@sa.gov.au", data_start
    )

    df = data["df"]
    df["date"] = pd.to_datetime(df["Date"])
    # df["Grade"] = pd.NA
    df["Grade"] = 1
    df = df.rename(
        columns={
            "Rain": "rainfall",
            "Srn": "interpolated_code",
            "Grade": "quality",
        }
    )
    df["year"] = df["date"].dt.year
    df["dayofyear"] = df["date"].dt.dayofyear
    df["finyear"] = [tn.date_to_wateruseyear(d) for d in df["date"]]

    cols = [
        "date",
        "rainfall",
        "interpolated_code",
        "quality",
        "year",
        "dayofyear",
        "finyear",
    ]
    return df[cols]


def download_aquarius_rainfall(station_id, data_start=None):
    """Download rainfall data from DEW's Aquarius Web Portal website.

    Args:
        station_id (int or str): Aquarius location ID
        data_start (pd.Timestamp): date to download data from (optional)

    Returns:
        dict:  with four keys: 'df', 'annual', 'srn', and 'wateruse_year'

    """
    if data_start is None:
        data_start = pd.Timestamp("1800-01-01")

    logger.debug(f"Downloading {station_id} from {data_start} from Aquarius")

    url = f"https://water.data.sa.gov.au/Export/BulkExport?DateRange=EntirePeriodOfRecord&TimeZone=9.5&Calendar=CALENDARYEAR&Interval=Daily&Step=1&ExportFormat=csv&TimeAligned=True&RoundData=True&IncludeGradeCodes=True&IncludeApprovalLevels=False&IncludeQualifiers=False&IncludeInterpolationTypes=False&Datasets[0].DatasetName=Rainfall.Best%20Available--Continuous%40{station_id}&Datasets[0].Calculation=Aggregate&Datasets[0].UnitId=89"
    resp = requests.get(url, verify=False)

    buffer = io.StringIO()
    buffer.write(resp.text)
    buffer.seek(0)
    i = 0
    for line in buffer:
        if i == 2:
            station_name = line.strip("\n").strip(",").strip()
        break

    df = pd.read_csv(
        buffer, skiprows=5, names=["Date", "end_timestamp", "Rain", "Grade"]
    )

    df = df.rename(columns={"Date": "date", "Rain": "rainfall", "Grade": "quality"})
    df["interpolated_code"] = 0
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["dayofyear"] = df["date"].dt.dayofyear
    df["finyear"] = [tn.date_to_wateruseyear(d) for d in df["date"]]

    cols = [
        "date",
        "rainfall",
        "interpolated_code",
        "quality",
        "year",
        "dayofyear",
        "finyear",
    ]
    return df[cols]


def convert_daily_to_old_style_rainfall_sheets(df):
    """Convert daily rainfall data to the old style of sheets.

    Args:
        df (pd.DataFrame): columns should be 'date', 'rainfall',
            'interpolated_code', 'quality', 'year', 'dayofyear',
            and 'finyear'.

    Returns:
        dict:

    """
    df = df.rename(columns={"date": "Date", "rainfall": "Rain", "quality": "Grade"})
    df = df.dropna(subset=["Date"], how="any")
    df["Date"] = pd.to_datetime(pd.to_datetime(df.Date).dt.date)
    df["year"] = df.Date.dt.year
    df["wu_year"] = df.Date.apply(tn.date_to_wateruseyear)
    df = df.dropna(subset=["Rain"], how="any")
    df = df[df.Grade >= 1]
    df["Srn"] = 0
    df = df[["Date", "year", "wu_year", "Rain", "Srn", "Grade"]]

    annual = df.groupby(df.Date.dt.year).Rain.sum()

    all_dates = pd.date_range(start=df.Date.min(), end=df.Date.max(), freq="1d")
    df_all = df.set_index("Date").reindex(all_dates).reset_index()
    df_all["Date"] = df_all["index"]
    df_all["year"] = df_all.Date.dt.year
    df_all["wu_year"] = df_all.Date.apply(tn.date_to_wateruseyear)
    df_all["Srn"] = df_all.Srn.fillna(25)
    df_all["Grade"] = df_all.Grade.fillna(-15)
    df_all["Grade"] = df_all.Grade.astype(int)
    df_all["Srn"] = df_all.Srn.astype(int)
    df_all.loc[df_all.Srn.isin([25, 35, 75]), "srn"] = "Interpolated"
    df_all.loc[df_all.Srn.isin([13, 15]), "srn"] = "Deaccumulated"
    srn = df_all.groupby(["year", "srn"]).Date.count().unstack(level=1)
    srn = srn.reindex(sorted(df_all.year.unique()), fill_value=0)
    for column in ["Interpolated", "Deaccumulated"]:
        if not column in srn.columns:
            srn[column] = 0

    wateruse_year = df.groupby(df.wu_year, as_index=False).Rain.sum()

    return {
        "df": df,
        "annual": annual,
        "srn": srn,
        "wateruse_year": wateruse_year,
    }


def reduce_daily_to_monthly(
    daily_df, dt_col="Date", year_col="wu_year", value_col="Rain"
):
    """Reduce daily rainfall totals into monthly totals per year.

    Args:
        daily_df (pandas DataFrame): daily rainfall data
        dt_col (str): column of *daily_df* with the date as a datetime
        year_col (str): column of *daily_df* with a value to group as
            years. It could be the year itself i.e.
            `daily_df[dt_col].dt.year` or it could be the financial year
        value_col (str): column with the rainfall total

    Returns:
        pd.DataFrame: a dataframe with columns *year_col*, "month", and *value_col*.

    """
    grouper = daily_df.groupby([daily_df[year_col], daily_df[dt_col].dt.month])
    sums = grouper[value_col].sum()
    return sums.reset_index().rename(columns={dt_col: "month"})


def get_seasonal_rainfall_data(daily, dt_col="Date", year_col="year", value_col="Rain"):
    """Convert daily rainfall data to monthly and seasonal.

    Args:
        daily (pd DataFrame): daily rainfall totals

    Returns:
        tuple: tuple of length two: monthly, seasons (both pd.DataFrames)

    """
    daily["year"] = daily[dt_col].dt.year
    monthly = reduce_daily_to_monthly(daily, year_col=year_col)

    monthly["season"] = monthly.month.map(months_to_seasons)
    monthly.loc[monthly.season == "summer", "season"] = "0-summer"
    monthly.loc[monthly.season == "autumn", "season"] = "1-autumn"
    monthly.loc[monthly.season == "winter", "season"] = "2-winter"
    monthly.loc[monthly.season == "spring", "season"] = "3-spring"
    monthly["year-season"] = monthly["year"].astype(str) + "-" + monthly["season"]
    monthly = monthly.sort_values(["year", "month"])
    seasons = (
        monthly.groupby(["year-season", "year", "season"])[value_col]
        .sum()
        .reset_index()
    )
    return monthly, seasons
