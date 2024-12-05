import pandas as pd
import numpy as np
from pandas.core.dtypes.common import is_categorical_dtype

from azureml.studio.core.data_frame_schema import SchemaConstants, DataFrameSchema
from azureml.studio.core.logger import common_logger
from azureml.studio.common.utils.datetimeutils import is_timespan_dtype, convert_to_datetime, is_datetime_dtype, \
    convert_to_time_span
from azureml.studio.core.utils.missing_value_utils import has_na, drop_na, is_na
from azureml.studio.common.datatable.constants import ElementTypeName


def convert_column_by_element_type(
        column, new_type, date_time_format=None, time_span_format=None):
    """
    The following chart is the conversion table of different element types

    The column of the table denotes the element type of input column
    The row of the table denotes the new_type
    Y means conversion is allowed by this interface (Still, internal errors might raise during the conversion)
    N means such conversion is not allowed by this interface

    # NAN and TIMESPAN are now deprecated.

            INT    FLOAT    STRING    BOOL    CATEGORY    DATETIME    (TIMESPAN)  (NAN)    UNCATEGORY

    INT      Y       Y        Y        Y        Y            Y            Y        N         Y

    FLOAT    Y       Y        Y        Y        Y            Y            Y        Y         Y

    STRING   Y       Y        Y        Y        Y            Y            Y        Y         Y

    BOOL     Y       Y        Y        Y        Y            N            N        N         Y

    CATEGORY Y       Y        Y        Y        Y            Y            Y        Y         Y

    DATETIME Y       Y        Y        Y        Y            Y            N        Y         Y

   (TIMESPAN)Y       Y        Y        Y        Y            N            Y        N         Y

    (NAN)      N       N        N        N        N            N            N        N         N

    """

    if not isinstance(column, pd.Series):
        raise TypeError('Column type is not Pandas.Series.')

    if new_type == ElementTypeName.NAN:
        _raise_convert_type_error(
            target_type=new_type,
            error_message=f'Type {ElementTypeName.NAN} is now deprecated. '
                          f'New_type must not be {ElementTypeName.NAN} type.'
        )

    if len(column) == 0:
        common_logger.warning('Input column is empty. Return without conversion.')
        return column

    try:
        if is_na(column):
            return _convert_column_of_all_missing_values(column, new_type)

        elif new_type == ElementTypeName.INT:
            column_new = _convert_to_int(column)

        elif new_type == ElementTypeName.FLOAT:
            column_new = _convert_to_float(column)

        elif new_type == ElementTypeName.BOOL:
            column_new = _convert_to_bool(column)

        elif new_type == ElementTypeName.STRING:
            column_new = _convert_to_str(column)

        elif new_type == ElementTypeName.CATEGORY:
            column_new = _convert_to_category(column)

        elif new_type == ElementTypeName.DATETIME:
            column_new = _convert_to_datetime(column, date_time_format)

        elif new_type == ElementTypeName.TIMESPAN:
            column_new = _convert_to_timespan(column, time_span_format)

        elif new_type == ElementTypeName.UNCATEGORY:
            column_new = _convert_to_uncategory(column)

        else:
            raise ValueError(f'new_type {new_type} is not ElementTypeName')
    except MemoryError:
        # Fix Bug 501833:  Type conversion may copy data so the memory is exhausted.
        # In this scenario , it should not be raised as a ConvertColumnTypeError.
        # If a MemoryError is raised, we directly raise it.
        raise
    except BaseException as e:
        _raise_convert_type_error(
            target_type=new_type,
            error_message=str(e),
            base_error=e)

    return column_new


def _convert_to_int(column):
    if is_datetime_dtype(column) or is_timespan_dtype(column):
        common_logger.info(f'Convert time to int with the unit of seconds')
        column_new = _drop_na_and_convert(column, ElementTypeName.INT)
        # The values are of the unit of nano-seconds
        # To convert to seconds, need to divide by 1e9
        if has_na(column_new):
            return column_new/1e9
        return (column_new/1e9).astype(ElementTypeName.INT)

    return _drop_na_and_convert(column, ElementTypeName.INT)


def _convert_to_float(column):
    if is_datetime_dtype(column) or is_timespan_dtype(column):
        common_logger.warning(
            f'{ElementTypeName.DATETIME} and {ElementTypeName.TIMESPAN} '
            f'columns will first be converted into {ElementTypeName.INT} type, then {ElementTypeName.FLOAT} type ')
        column = _convert_to_int(column)

    # Replace pd.NaT (missing value in date-time column) with np.nan
    # Otherwise error will be raised in column.astype
    column.fillna(value=np.nan, inplace=True)

    return column.astype(ElementTypeName.FLOAT)


def _convert_to_str(column):
    column_new = _drop_na_and_convert(column, ElementTypeName.STRING)
    # Replace pd.NaT (missing value in date-time column) with np.nan
    # Otherwise this column cannot be dumped into parquet
    column_new.replace(to_replace=pd.NaT, value=np.nan, inplace=True)
    return column_new


def _convert_to_bool(column):
    common_logger.warning('0 and empty string will be converted into False')
    if is_datetime_dtype(column) or is_timespan_dtype(column):
        column = _convert_to_int(column)

    return _drop_na_and_convert(column, ElementTypeName.BOOL)


def _convert_to_uncategory(column):
    """
    Only category column will be converted into original type, otherwise return column without conversion
    """
    if is_categorical_dtype(column):
        # First convert column to numpy.array to drop the dtype
        return pd.Series(np.asarray(column))
    else:
        common_logger.warning('Return column without conversion')
        return column


def _convert_to_category(column):
    return column.astype(ElementTypeName.CATEGORY)


def _convert_to_datetime(column, date_time_format):
    if is_timespan_dtype(column):
        _raise_convert_type_error(
            target_type=ElementTypeName.DATETIME,
            error_message=f'{ElementTypeName.TIMESPAN} types must not be converted into {ElementTypeName.DATETIME} type'
        )

    element_type, _ = DataFrameSchema.get_column_element_type(column)
    if element_type == ElementTypeName.BOOL:
        raise ValueError(f"{ElementTypeName.BOOL} type column is not allowed to be converted into "
                         f"{ElementTypeName.DATETIME} type")

    return convert_to_datetime(column, date_time_format=date_time_format, unit='s',
                               errors=SchemaConstants.ERROR_ACTION_RAISE)


def _convert_to_timespan(column, time_span_format):
    if is_datetime_dtype(column):
        _raise_convert_type_error(
            target_type=ElementTypeName.TIMESPAN,
            error_message=f'{ElementTypeName.DATETIME} types must not be converted into {ElementTypeName.TIMESPAN} type'
        )

    element_type, _ = DataFrameSchema.get_column_element_type(column)
    if element_type == ElementTypeName.BOOL:
        raise ValueError(f"{ElementTypeName.BOOL} type column is not allowed to be converted into "
                         f"{ElementTypeName.TIMESPAN} type")

    return convert_to_time_span(column, unit=time_span_format, errors=SchemaConstants.ERROR_ACTION_RAISE)


def _drop_na_and_convert(column, new_type):
    column_has_na = has_na(column)
    # If no na value, directly convert with the type.
    if not column_has_na:
        return column.astype(new_type)

    # Otherwise, only convert the non-na values.
    # Fix bug 513210: If the index contain duplicated values, a ValueError will be raised by the reindex function.
    # To fix this bug, we store the original index, then update the column index with 1..n,
    # and recover the original index after we convert the column with the new type.
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


def convert_str_to_bool(val):
    if val in {'True', 'true', 'TRUE'}:
        return True
    if val in {'False', 'false', 'FALSE'}:
        return False
    raise ValueError(f"Not a valid boolean value: '{val}'")


CONVERTERS = {
    ElementTypeName.INT: int,
    ElementTypeName.FLOAT: float,
    ElementTypeName.STRING: str,
    ElementTypeName.BOOL: convert_str_to_bool,
    ElementTypeName.DATETIME: convert_to_datetime,
    ElementTypeName.TIMESPAN: convert_to_time_span,
}


# Category type should be converted to its underlying type.
def try_convert_str_by_element_type(scalar, target_type):
    converter = CONVERTERS.get(target_type)
    if converter is None:
        raise NotImplementedError(f"Conversion from str to `{target_type}` is not implemented.")
    try:
        return converter(scalar)
    except BaseException:
        return None


def try_convert_str(scalar: str):
    # Currently we do not try convert it to TIMESPAN since we cannot store this type.
    # TODO: Add TIMESPAN support or remove TIMESPAN
    possible_types = [ElementTypeName.BOOL, ElementTypeName.INT, ElementTypeName.FLOAT, ElementTypeName.DATETIME]
    for possible_type in possible_types:
        val = try_convert_str_by_element_type(scalar, target_type=possible_type)
        if val is not None:
            return val
    return scalar


def convert_scalar_by_element_type(scalar, target_type):

    try:
        if target_type == ElementTypeName.INT:
            return int(scalar)

        elif target_type == ElementTypeName.FLOAT:
            return float(scalar)

        elif target_type == ElementTypeName.STRING:
            return str(scalar)

        elif target_type == ElementTypeName.BOOL:
            if isinstance(scalar, bool):
                return scalar

            # The following logic follows the logic in v1:
            # Microsoft.Numerics.MissingValuesSupport.MissingValuesScrubber.GetReplaceMentValue
            # If the scalar is a string in True/False, return the corresponding value,
            # otherwise try to convert the value to float to handle the case '0.0',
            # bool('0.0') = True
            # bool(float('0.0')) = False
            if isinstance(scalar, str):
                lower = scalar.lower()
                if lower == 'true':
                    return True
                elif lower == 'false':
                    return False

            try:
                return bool(float(scalar))
            except ValueError as e:
                raise ValueError(f"Not a valid boolean value: '{scalar}'") from e

        elif target_type == ElementTypeName.CATEGORY:
            return scalar

        elif target_type == ElementTypeName.DATETIME:
            return convert_to_datetime(scalar)

        elif target_type == ElementTypeName.TIMESPAN:
            return convert_to_time_span(scalar)

        elif target_type == ElementTypeName.NAN:
            # To match V1
            _raise_convert_type_error(
                target_type=target_type,
                error_message=f'Type {ElementTypeName.NAN} is now deprecated. '
                              f'target type must not be {ElementTypeName.NAN} type.'
            )
        else:
            raise ValueError(f'new_type {target_type} is not ElementTypeName')

    except BaseException as e:
        raise RuntimeError(f'Cannot convert to type "{target_type}": {str(e)}') from e


def _raise_convert_type_error(target_type, error_message, base_error=None):
    convert_type_error = TypeError(f'Cannot convert to type "{target_type}": {error_message}')
    if base_error:
        raise convert_type_error from base_error
    else:
        raise convert_type_error


def _convert_column_of_all_missing_values(column, new_type):
    if new_type == ElementTypeName.FLOAT:
        return pd.Series((np.nan,)*len(column))
    elif new_type == ElementTypeName.DATETIME:
        return pd.Series((pd.NaT,)*len(column))
    elif new_type == ElementTypeName.STRING:
        return pd.Series((None,)*len(column))
    elif new_type == ElementTypeName.CATEGORY:
        return column.astype(ElementTypeName.CATEGORY)
    elif new_type == ElementTypeName.UNCATEGORY:
        return _convert_to_uncategory(column)
    else:
        raise ValueError(f'Cannot convert column of all missing values to {new_type} type.')
