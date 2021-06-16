import numpy as np


def flag_na_rows_in_columns(df):
    has_na_rows = df.isna()
    column_names_with_na_rows = df.columns[has_na_rows.any()].to_list()
    return has_na_rows[column_names_with_na_rows].rename(columns=lambda c: c + "_isna")


def _get_column_average(column):
    if np.issubdtype(column.dtype, np.number):
        average = column.median()
    else:
        average = column.mode().iloc[0]
    return average


def fillna_with_group_average(df, group_names):
    return df.fillna(df.groupby(group_names).transform(_get_column_average))
