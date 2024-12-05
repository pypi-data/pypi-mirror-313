import pandas as pd
from pandas.util.testing import assert_frame_equal
import numpy as np
from azureml.studio.core.utils.missing_value_utils import has_na, drop_na
from azureml.studio.core.data_frame_schema import ElementTypeName
import datetime


def compare_dataframe(
        table1: pd.DataFrame,
        table2: pd.DataFrame,
        with_order: bool = True):
    table1 = _clean_dataframe(table1)
    table2 = _clean_dataframe(table2)
    assert_frame_equal(table1, table2)
    return True


def compare_apply_math_dataframe(
        table1: pd.DataFrame,
        table2: pd.DataFrame,
        decimal_precision,
        with_order: bool = True):
    table1 = _clean_dataframe(table1)
    table2 = _clean_dataframe(table2)
    print(f'decimal precision: {decimal_precision}')
    # print(table1)
    # print(table2)
    np.testing.assert_array_almost_equal(table1, table2, decimal=decimal_precision)
    return True


def _clean_dataframe(table: pd.DataFrame):
    return table.reset_index(drop=True).reindex(sorted(table.columns), axis=1)


def normalize_dataframe_for_output(data: pd.DataFrame) -> pd.DataFrame:
    for column_index in range(len(data.columns)):
        data.iloc[:, column_index] = normalize_column_for_output(
            data.iloc[:, column_index])
    return data


def normalize_column_for_output(column: pd.Series) -> pd.Series:
    if pd.core.dtypes.common.is_timedelta64_dtype(
            column.dropna()) or is_type(
            column,
            datetime.timedelta,
            pd.Timedelta):
        return pd.to_timedelta(column)
    if pd.api.types.is_datetime64_any_dtype(
            column.dropna()) or is_type(
            column,
            datetime.datetime,
            datetime.date,
            pd.Timestamp):
        return pd.to_datetime(column)
    if column.dtype.name == "bool" or pd.api.types.infer_dtype(
            column) == "boolean" or is_type(column, bool):
        return _convert_to_bool(column)
    if column.dtype.name == "object" and column.dropna().count() > 0:
        return _convert_to_str(column)
    return column


def is_type(column: pd.Series, *types) -> bool:
    drop_na = column.dropna()
    if drop_na.count() == 0:
        return False
    for check_type in types:
        if drop_na.apply(
            lambda x: isinstance(
                x,
                check_type)).astype(bool).all():
            return True
    return False


def _convert_to_bool(column: pd.Series) -> pd.Series:
    return _drop_na_and_convert(column, ElementTypeName.BOOL)


def _drop_na_and_convert(column, new_type):
    column_has_na = has_na(column)
    # If no na value, directly convert with the type.
    if not column_has_na:
        return column.astype(new_type)
    # Otherwise, only convert the non-na values.
    # Fix bug 513210: If the index contain duplicated values, a ValueError will be raised by the reindex function.
    # To fix this bug, we store the original index, then update the column index with 1..n,
    # and recover the original index after we convert the column with the new
    # type.
    original_index = column.index
    column.index = range(len(column))
    column_without_na = drop_na(column, reset_index=False)
    # Use np.array instead of python list for better efficiency.
    index_of_na = np.array(column.index.difference(column_without_na.index))
    column_new = column_without_na.astype(new_type).reindex(index=column.index)
    if new_type == ElementTypeName.INT or new_type == ElementTypeName.FLOAT:
        column_new[index_of_na] = np.nan
    else:
        column_new[index_of_na] = column[index_of_na]
    column_new.index = original_index
    return column_new


def _convert_to_str(column: pd.Series):
    column_new = _drop_na_and_convert(column, ElementTypeName.STRING)
    # Replace pd.NaT (missing value in date-time column) with np.nan
    # Otherwise this column cannot be dumped into parquet
    column_new.replace(to_replace=pd.NaT, value=np.nan, inplace=True)
    return column_new
