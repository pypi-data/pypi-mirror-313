import pandas as pd

from azureml.studio.modulehost.attributes import ItemInfo
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_type_conversion import convert_scalar_by_element_type

from azureml.studio.core.logger import TimeProfile, time_profile, module_logger
from azureml.studio.common.types import AutoEnum
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.core.utils.missing_value_utils import get_number_of_na, is_na, fill_na
from azureml.studio.modules.datatransform.common.base_transform import BaseTransform
from azureml.studio.modules.datatransform.clean_missing_data.pca_predictor import \
    ProbabilisticPcaMissingValuePredictor
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.common.error import ErrorMapping, ColumnNotFoundError, ParameterParsingError


class CleanMissingDataHandlingPolicy(AutoEnum):
    ReplaceUsingMICE: ItemInfo(
        name="Replace using MICE", friendly_name="Replace using MICE", release_state=ReleaseState.Alpha) = ()

    ReplaceWithValue: ItemInfo(
        name="Custom substitution value", friendly_name="Custom substitution value") = ()
    ReplaceWithMean: ItemInfo(
        name="Replace with mean", friendly_name="Replace with mean") = ()
    ReplaceWithMedian: ItemInfo(
        name="Replace with median", friendly_name="Replace with median") = ()
    ReplaceWithMode: ItemInfo(
        name="Replace with mode", friendly_name="Replace with mode") = ()
    RemoveRow: ItemInfo(
        name="Remove entire row", friendly_name="Remove entire row") = ()
    RemoveColumn: ItemInfo(
        name="Remove entire column", friendly_name="Remove entire column") = ()

    ReplaceUsingProbabilisticPca: ItemInfo(
        name="Replace using Probabilistic PCA", friendly_name="Replace using Probabilistic PCA",
        release_state=ReleaseState.Alpha) = ()


class CleanMissingValueTransform(BaseTransform):

    INDICATOR_COLUMN_NAME_SUFFIX = '_IsMissing'

    def __init__(self,
                 cleaning_mode: CleanMissingDataHandlingPolicy,
                 replacement_value: str,
                 # if True, remove column with all missing values
                 remove_columns_with_all_missing: bool,
                 # if True, generate extra columns indicating if each element is originally a missing value
                 indicator_columns: bool,
                 column_names: list,
                 min_ratio: float,
                 max_ratio: float,
                 iterations: int = None,
                 column_imputers: dict = None,
                 original_column_element_types: dict = None,
                 pca_predictor: ProbabilisticPcaMissingValuePredictor = None):

        self._cleaning_mode = cleaning_mode
        self._replacement_value = replacement_value
        self._remove_columns_with_all_missing = remove_columns_with_all_missing
        self._indicator_columns = indicator_columns
        self._column_names = column_names
        self._min_ratio = min_ratio
        self._max_ratio = max_ratio
        self._iterations = iterations
        self._column_imputers = column_imputers
        self._original_column_element_types = original_column_element_types
        self._pca_predictor = pca_predictor
        # Record the replacement value for each dict
        self._col2value_dct = {}

    def apply(self, dt: DataTable):
        # Check if self._column_names are included in dt's column name list
        for column_name in self._column_names:
            if column_name not in dt.column_names:
                raise ColumnNotFoundError(
                    column_id=column_name, arg_name_has_column='Transformation', arg_name_missing_column='Dataset')

        column_indexes = [dt.get_column_index(column_name) for column_name in self._column_names]

        module_logger.info('Get column indexes with wanted ratio')
        columns_to_clean = self.get_column_indexes_with_wanted_ratio(
            dt, column_indexes, self._min_ratio, self._max_ratio)

        if self._cleaning_mode is CleanMissingDataHandlingPolicy.ReplaceUsingMICE:
            raise NotImplementedError('ReplaceUsingMICE has not been implemented')

        elif self._cleaning_mode is CleanMissingDataHandlingPolicy.ReplaceUsingProbabilisticPca:
            raise NotImplementedError('ReplaceUsingProbabilisticPca has not been implemented')

        if self._cleaning_mode is CleanMissingDataHandlingPolicy.ReplaceWithValue:
            module_logger.info('Replace with value')
            return self.replace_with_value(
                dt, self._remove_columns_with_all_missing, self._indicator_columns,
                columns_to_clean, self._replacement_value)

        elif self._cleaning_mode is CleanMissingDataHandlingPolicy.ReplaceWithMean:
            module_logger.info('Replace with mean')
            return self.replace_with_mean(
                dt, self._remove_columns_with_all_missing, self._indicator_columns,
                columns_to_clean)

        elif self._cleaning_mode is CleanMissingDataHandlingPolicy.ReplaceWithMedian:
            module_logger.info('Replace with median')
            return self.replace_with_median(
                dt, self._remove_columns_with_all_missing, self._indicator_columns,
                columns_to_clean)

        elif self._cleaning_mode is CleanMissingDataHandlingPolicy.ReplaceWithMode:
            module_logger.info('Replace with mode')
            return self.replace_with_mode(
                dt, self._remove_columns_with_all_missing, self._indicator_columns,
                columns_to_clean)

        elif self._cleaning_mode is CleanMissingDataHandlingPolicy.RemoveRow:
            module_logger.info('Replace row with missing value')
            return self.remove_row(dt, self._remove_columns_with_all_missing, columns_to_clean)

        elif self._cleaning_mode is CleanMissingDataHandlingPolicy.RemoveColumn:
            module_logger.info('Replace column with missing value')
            return self.remove_column(dt, self._indicator_columns, columns_to_clean)

    @staticmethod
    @time_profile
    def get_column_indexes_with_wanted_ratio(
            dt: DataTable, col_indexes: list, min_ratio: float, max_ratio: float):
        """
        Return column indexes of columns, in which missing value ratio is
        between min_ratio and max_ratio
        """

        number_of_na_by_column = (get_number_of_na(dt.get_column(col_index)) for col_index in col_indexes)
        ratio_of_na_by_column = [x/dt.number_of_rows for x in number_of_na_by_column]

        return [col_indexes[i] for i in range(len(col_indexes))
                if min_ratio <= ratio_of_na_by_column[i] <= max_ratio]

    @staticmethod
    def create_mice_transform(
            dt: DataTable,
            columns_to_clean: DataTableColumnSelection,
            indicator_columns: bool,
            remove_columns_with_all_missing: bool,
            min_ratio: float,
            max_ratio: float):
        # TODO
        pass

    @staticmethod
    def create_replace_using_pca_transform(
            dt: DataTable,
            columns_to_clean: DataTableColumnSelection,
            indicator_columns: bool,
            remove_columns_with_all_missing: bool,
            min_ratio: float,
            max_ratio: float):
        # TODO
        pass

    def replace_with_mean(
            self,
            dt: DataTable,
            remove_columns_with_all_missing: bool,
            generate_missing_value_indicator_columns: bool,
            columns_to_clean_indexes: list):

        self._validate_column_types_for_numeric_transforms(dt, columns_to_clean_indexes)

        # Method to compute mean value of a column
        replacement_value_generator = self._compute_mean

        return self._replace_missing_values(
            dt, replacement_value_generator, remove_columns_with_all_missing,
            generate_missing_value_indicator_columns,
            columns_to_clean_indexes)

    def replace_with_median(
            self,
            dt: DataTable,
            remove_columns_with_all_missing: bool,
            generate_missing_value_indicator_columns: bool,
            columns_to_clean_indexes: list):

        self._validate_column_types_for_numeric_transforms(dt, columns_to_clean_indexes)

        # Method to compute median value of a column
        replacement_value_generator = self._compute_median

        return self._replace_missing_values(
            dt, replacement_value_generator, remove_columns_with_all_missing,
            generate_missing_value_indicator_columns,
            columns_to_clean_indexes)

    def replace_with_mode(
            self,
            dt: DataTable,
            remove_columns_with_all_missing: bool,
            generate_missing_value_indicator_columns: bool,
            columns_to_clean_indexes: list):

        # Method to compute mode value of a column
        replacement_value_generator = self._compute_mode

        return self._replace_missing_values(
            dt, replacement_value_generator, remove_columns_with_all_missing,
            generate_missing_value_indicator_columns,
            columns_to_clean_indexes)

    def replace_with_value(
            self,
            dt: DataTable,
            remove_columns_with_all_missing: bool,
            generate_missing_value_indicator_columns: bool,
            columns_to_clean_indexes: list,
            replacement_value: str):

        # No method to compute replacement_value since it is already provided
        replacement_value_generator = None

        return self._replace_missing_values(
            dt, replacement_value_generator, remove_columns_with_all_missing,
            generate_missing_value_indicator_columns,
            columns_to_clean_indexes, replacement_value)

    @classmethod
    @time_profile
    def remove_column(
            cls,
            dt: DataTable,
            generate_missing_value_indicator_columns: bool,
            columns_to_clean_indexes: list):
        """
        remove entire column with any missing values
        """

        column_indexes_to_keep = list()
        indicator_columns = pd.DataFrame()

        for col_index in range(dt.number_of_columns):
            if col_index not in columns_to_clean_indexes:
                column_indexes_to_keep.append(col_index)
            elif dt.get_number_of_missing_value(col_index) == 0:
                column_indexes_to_keep.append(col_index)
                if generate_missing_value_indicator_columns:
                    cls._generate_missing_value_indicator_column(
                        dt, col_index, indicator_columns, has_missing_value=False)

        dt_out = dt.get_slice_by_column_indexes(column_indexes_to_keep, if_clone=True)

        if generate_missing_value_indicator_columns:
            for column_name in indicator_columns.columns.values.tolist():
                dt_out.add_column(column_name, indicator_columns[column_name])

        return dt_out

    @classmethod
    def remove_row(
            cls,
            dt: DataTable,
            remove_columns_with_all_missing: bool,
            columns_to_clean_indexes: list):
        """
        remove entire row with any missing values
        """

        if remove_columns_with_all_missing:
            dt_out, columns_to_clean_indexes = cls._remove_columns_with_all_missing_method(dt, columns_to_clean_indexes)
        else:
            dt_out = dt.clone()

        with TimeProfile("Find row_indexes_to_remove"):
            df = dt_out.data_frame[dt_out.data_frame.iloc[:, columns_to_clean_indexes].isnull().any(axis=1)]
            row_indexes_to_remove = list(df.index)

        with TimeProfile("Remove rows by indexes"):
            dt_out.remove_row(row_indexes_to_remove)

        # Comment column type conversion to save computational cost
        # Make sure the column type of dt_out to be the same as dt
        # for column_index in range(dt_out.number_of_columns):
        #    dt_out.set_column_element_type(column_index, dt.get_element_type(column_index))
        return dt_out

    @time_profile
    def _replace_missing_values(
            self,
            dt: DataTable,
            # Method to compute replacement value from column
            replacement_value_generator,
            # if True, remove column with all missing values
            remove_columns_with_all_missing: bool,
            # If True, generate extra columns indicating if each element is originally a missing value
            generate_missing_value_indicator_columns: bool,
            column_to_clean_indexes: list,
            replacement_value: str = None):
        """
        Engine to compute all replacement methods, except for remove_row and remove_column

        """

        if not any(dt.get_number_of_missing_value(col_index) > 0 for col_index in column_to_clean_indexes):
            return dt.clone()

        if remove_columns_with_all_missing:
            # Remove columns of all missing values. column_to_clean_indexes are also adjusted.
            # dt_out must be used in the following code, instead of dt.
            dt_out, column_to_clean_indexes = self._remove_columns_with_all_missing_method(dt, column_to_clean_indexes)
        else:
            dt_out = dt.clone()

        # To record if element is originally a missing value
        indicator_columns = pd.DataFrame()

        for col_index in column_to_clean_indexes:

            # If no missing value, then does not need to replace, generate indicator if True
            if dt_out.get_number_of_missing_value(col_index) == 0:
                if generate_missing_value_indicator_columns:
                    self._generate_missing_value_indicator_column(
                        dt_out, col_index, indicator_columns, has_missing_value=False)

            else:
                if generate_missing_value_indicator_columns:
                    self._generate_missing_value_indicator_column(
                        dt_out, col_index, indicator_columns, has_missing_value=True)

                column_name = dt.get_column_name(col_index)
                # For backward compatibility
                if not hasattr(self, '_col2value_dct'):
                    self._col2value_dct = {}

                if self._col2value_dct.get(column_name) is not None:
                    # Use previously recorded value to replace missing values
                    replacement_value = self._col2value_dct.get(column_name)
                else:
                    if replacement_value_generator is not None:
                        replacement_value = self._get_replacement_value_from_generator(
                            replacement_value_generator, dt_out, col_index)
                    self._col2value_dct.update({column_name: replacement_value})

                self._replace_missing_values_in_column(
                    dt_out, col_index, replacement_value)

        # Add the indicator columns to the output DataTable if True
        if generate_missing_value_indicator_columns:
            for column_name in indicator_columns.columns.values.tolist():
                dt_out.add_column(column_name, indicator_columns[column_name])

        return dt_out

    @staticmethod
    def _remove_columns_with_all_missing_method(dt, column_indexes):
        # Record columns index to keep in dt.
        column_indexes_to_keep = list()
        column_indexes_new = list()
        remove_offset = 0

        for col_index in range(dt.number_of_columns):
            if col_index in column_indexes:
                if dt.get_number_of_missing_value(col_index) == dt.number_of_rows:
                    remove_offset += 1
                else:
                    # Keep columns which not only contain missing values.
                    column_indexes_to_keep.append(col_index)
                    # New column indexes must be adjusted because {remove_offset} columns have been excluded.
                    column_indexes_new.append(col_index - remove_offset)
            else:
                # Keep columns which are not selected.
                column_indexes_to_keep.append(col_index)

        dt_out = dt.get_slice_by_column_indexes(column_indexes_to_keep, if_clone=True)
        return dt_out, column_indexes_new

    @classmethod
    def _generate_missing_value_indicator_column(cls, dt, col_index, indicator_columns, has_missing_value=True):
        indicator_column = pd.Series(pd.np.zeros(dt.number_of_rows, dtype=bool))

        if has_missing_value:
            indicator_column = dt.data_frame.iloc[:, col_index].isna()

        # Make sure the indicator column name does not coincide with any existing column name
        name_already_exists = indicator_columns.columns.values.tolist() + dt.column_names
        indicator_column_name = cls._generate_indicator_column_name(name_already_exists, dt.get_column_name(col_index))

        indicator_columns[indicator_column_name] = indicator_column

    @classmethod
    def _generate_indicator_column_name(cls, name_already_exists, column_name):
        indicator_name_base = column_name + cls.INDICATOR_COLUMN_NAME_SUFFIX
        indicator_name = indicator_name_base
        count = 0
        while indicator_name in name_already_exists:
            count += 1
            indicator_name = indicator_name_base + f' ({count})'
        return indicator_name

    @classmethod
    def _get_replacement_value_from_generator(cls, replacement_value_generator, dt, col_index):
        if dt.get_number_of_missing_value(col_index) == dt.number_of_rows:
            return None
        try:
            return replacement_value_generator(dt.get_column(col_index))
        except Exception as e:
            raise RuntimeError(f'Error generating replacement value for column name'
                               f' "{dt.get_column_name(col_index)}": {str(e)}')

    @classmethod
    def _replace_missing_values_in_column(
            cls, dt, col_index, replacement_value):
        if not is_na(replacement_value):
            # Convert the type of replacement_value to match the element type of the column
            replacement_value = cls._convert_replacement_value(dt, col_index, replacement_value)
            column_new = fill_na(dt.get_column(col_index), replacement_value)
            dt.set_column(col_index, column_new)

    @staticmethod
    def _compute_mean(column):
        return column.mean(skipna=True)

    @staticmethod
    def _compute_median(column):
        return column.median(skipna=True)

    @staticmethod
    def _compute_mode(column):
        computed_series = column.mode()
        if len(computed_series) > 0:
            # computed_series might be non-numeric type, in such case the first value is returned
            try:
                compute_value = computed_series.mean()
            except BaseException as e:
                module_logger.warning(f"Failed to calculate the mean value, use the first value instead. Error: {e}")
                compute_value = computed_series[0]

            return compute_value
        else:
            return None

    @staticmethod
    def _convert_replacement_value(dt, col_index, replacement_value):
        # Bug 592585: we should convert the value to underlying type when it is category type.
        element_type = dt.get_underlying_element_type(col_index)
        try:
            return convert_scalar_by_element_type(replacement_value, element_type)
        except RuntimeError as e:
            new_error = ParameterParsingError(arg_name_or_column=dt.column_names[col_index],
                                              to_type=element_type,
                                              from_type=type(replacement_value).__name__,
                                              arg_value=replacement_value,
                                              )
            ErrorMapping.rethrow(e, new_error)

    @staticmethod
    def _validate_column_types_for_numeric_transforms(dt, column_indexes: list):
        for column_index in column_indexes:
            element_type = dt.get_element_type(column_index)
            if element_type not in ElementTypeName.NUMERIC_LIST and not dt.is_all_na_column(column_index):
                ErrorMapping.throw_invalid_column_type(
                    type_=element_type, column_name=dt.get_column_name(column_index), arg_name='Dataset')
