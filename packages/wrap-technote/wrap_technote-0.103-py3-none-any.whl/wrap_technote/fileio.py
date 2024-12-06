import pandas as pd


def read_csv(*args, date_cols=None, **kwargs):
    """Read CSV file and convert date and numeric columns to the correct
    data types.

    Args:
        date_cols (list or None): if None, use *date_cols* ["obs_date", "creation_date",
            "modified_date", "collected_date"]; if "auto", use all columns ending with
            "_date"; otherwise a list of columns

    Other arguments and keyword arguments are passed to :func:`pandas.read_csv`.

    Returns:
        pandas DataFrame

    """
    df = pd.read_csv(*args, **kwargs)
    if date_cols == "auto":
        date_cols = [c for c in df.columns if c.endswith("_date")]
    elif date_cols is None:
        date_cols = ("obs_date", "creation_date", "modified_date", "collected_date")
    for col in date_cols:
        if col in df:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in df.columns:
        if not col in date_cols:
            df[col] = pd.to_numeric(df[col], errors="ignore")
    return df
