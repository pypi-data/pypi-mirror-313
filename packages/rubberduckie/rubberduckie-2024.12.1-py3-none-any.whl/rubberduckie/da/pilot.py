import numpy as np
import pandas as pd


def calc_weeks_between(date_start, date_end):
    """Calculate number of weeks between two dates
    Colin Li @ 2023Q1
    Args:
        date_start (datetime.datetime): start date
        date_end (datetime.datetime): end date

    Returns:
        int: number of weeks in between
    """
    y_start, w_start = date_start.isocalendar()[:2]
    y_end, w_end = date_end.isocalendar()[:2]
    if y_end == y_start:
        w = w_end - w_start + 1
    elif y_end > y_start:
        w = (52 - w_start + 1) + (52 * (y_end - y_start - 1)) + w_end
    return w


def prepare_dev_triangle(df, max_dev_period):
    """Prepare development triangle

    Colin Li @ 2023Q1

    Args:
        df (pandas.DataFrame): dataframe contains below colunms:
                               1. uid: unique identifer for each sample
                               2. week_1: week number
                               3. dev_period: development period number
        max_dev_period (int): max number of develop period for triangle

    Returns:
        pandas.DataFrame: dataframe triangle
    """
    m_cols = len({"uid", "week_1", "dev_period"}.intersection(df.columns))
    w_text = "Columns 'uid', 'week_1', 'dev_period' must exist in input dataframe!"
    assert m_cols == 3, w_text

    # Generate pivot
    df["y_pred"] = 1
    df_t = pd.pivot_table(
        data=df, values="y_pred", columns="dev_period", index="week_1", aggfunc="count"
    )
    df_t.columns.name = None

    # Fill missing dev period column(s)
    week_max = df["week_1"].max()
    cols_exp = set(range(1, max_dev_period + 1))
    cols_mis = cols_exp - set(df_t.columns)
    print("Cols created for missing dev period:", cols_mis)
    for c in cols_mis:
        df_t[c] = np.nan
    df_t = df_t[cols_exp].copy()

    # Fill mising week row(s)
    idx_mis = cols_exp - (set(df_t.index))
    print("Rows created for missing week number:", idx_mis)
    for i in idx_mis:
        df_t.loc[i] = np.nan
    df_t = df_t.sort_index().copy()

    # Prepare triangle: fill the right cells with 0s
    for w in range(1, max_dev_period + 1):
        df_t.loc[w, range(1, max_dev_period - w + 2)] = df_t.loc[
            w, range(1, max_dev_period - w + 2)
        ].fillna(0)

    # Prepare triangle: calculate cumulated sum
    df_t = df_t.cumsum(axis=1)
    df_t.reset_index()

    # return df triangle
    return df_t


if __name__ == "__main__":
    pass
