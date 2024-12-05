import pandas as pd
import numpy as np

from azureml.studio.common.datatable.data_table import DataTable, DataTableColumnSelection
from azureml.studio.common.error import NoColumnsSelectedError, \
    InvalidColumnTypeError, ParameterParsingError, NotSortedValuesError, InfinityError, ColumnWithAllMissingsError
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.common.types import AutoEnum
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.core.schema import ElementTypeName, ColumnTypeName
from azureml.studio.core.logger import module_logger, TimeProfile

from azureml.studio.core.utils.strutils import add_suffix_number_to_avoid_repetition
from azureml.studio.modulehost.attributes import ItemInfo
from azureml.studio.modules.datatransform.common.base_transform import BaseTransform


class QuantizationMode(AutoEnum):
    Quantiles: ItemInfo(name='Quantiles', friendly_name='Quantiles') = ()
    EqualWidth: ItemInfo(name='Equal Width', friendly_name='Equal Width') = ()
    CustomEdges: ItemInfo(name='Custom Edges', friendly_name='Custom Edges') = ()
    EntropyMDL: ItemInfo(name='Entropy MDL', friendly_name='Entropy MDL', release_state=ReleaseState.Alpha) = ()
    EqualWidthCustomStartAndStop: ItemInfo(
        name='Equal Width With Custom Start and Stop',
        friendly_name='Equal Width With Custom Start and Stop',
        release_state=ReleaseState.Alpha) = ()


class OutputMode(AutoEnum):
    Append: ItemInfo(name='Append', friendly_name='Append') = ()
    Inplace: ItemInfo(name='Inplace', friendly_name='Inplace') = ()
    ResultOnly: ItemInfo(name='Result Only', friendly_name='Result Only') = ()


class BinningNormalization(AutoEnum):
    Percent: ItemInfo(name='Percent', friendly_name='Percent') = ()
    PQuantile: ItemInfo(name='PQuantile', friendly_name='PQuantile') = ()
    QuantileIndex: ItemInfo(name='Quantile Index', friendly_name='Quantile Index') = ()


class GroupDataIntoBinsTransform(BaseTransform):
    COLUMN_NAME_SUFFIX = '_quantized'
    BIN_EDGE_LIST_DELIMITER = ','

    def __init__(
            self,
            binning_mode: QuantizationMode,
            column_filter: DataTableColumnSelection,
            output_mode: OutputMode,
            categorical: bool,
            bin_count: int,
            normalization: BinningNormalization,
            first_edge: float,
            bin_width: float,
            last_edge: float,
            bin_edge_list: str
    ):
        self._binning_mode = binning_mode
        self._column_filter = column_filter
        self._output_mode = output_mode
        self._categorical = categorical
        self._bin_count = bin_count
        self._normalization = normalization
        self._first_edge = first_edge
        self._bin_width = bin_width
        self._last_edge = last_edge
        self._bin_edge_list = bin_edge_list

    def apply(self, dt: DataTable):
        # Verify input data and column filter
        self._verify_input_data_table_not_empty(dt)
        selected_columns = self._verify_selected_columns_not_empty(dt)
        self._verify_selected_column_types(dt, selected_columns)

        with TimeProfile(f'Apply binning with mode {QuantizationMode.Quantiles.name}.'):
            if self._binning_mode == QuantizationMode.Quantiles:
                dt_output = self._apply_quantiles_quantization(dt, selected_columns)

            elif self._binning_mode == QuantizationMode.EqualWidth:
                dt_output = self._apply_equal_width_quantization(dt, selected_columns)

            elif self._binning_mode == QuantizationMode.CustomEdges:
                dt_output = self._apply_custom_edges_quantization(dt, selected_columns)

            elif self._binning_mode == QuantizationMode.EntropyMDL:
                dt_output = self._apply_entropy_mdl_quantization(dt, selected_columns)

            else:
                dt_output = self._apply_equal_width_custom_quantization(dt, selected_columns)

        if self._categorical:
            module_logger.info('Tag binned columns as categorical.')
            self._handle_categorical(dt_output)

        dt_output = self._handle_output_mode(dt, dt_output)

        return dt_output

    def _apply_quantiles_quantization(self, dt: DataTable, selected_columns: list):
        df_output = pd.DataFrame()
        for column_name in selected_columns:
            # Mark duplicates='drop', in case there are multiple np.inf in bin edges
            column_quantized = pd.qcut(
                dt.get_column(column_name),
                self._bin_count,
                labels=False,
                duplicates='drop'
            )

            # Make sure quantized data starts from 1 instead of 0
            column_quantized += 1

            if self._normalization == BinningNormalization.PQuantile:
                # Values are normalized within the range [0,1]
                column_quantized = column_quantized / (self._bin_count + 1)

            elif self._normalization == BinningNormalization.Percent:
                # Values are normalized within the range [0,100]
                column_quantized = column_quantized / (self._bin_count + 1) * 100

            # For BinningNormalization.QuantileIndex, no normalization is needed
            df_output[column_name] = column_quantized

        return DataTable(df_output)

    def _apply_equal_width_quantization(self, dt: DataTable, selected_columns: list):
        df_output = pd.DataFrame()
        for column_name in selected_columns:
            column = dt.get_column(column_name)

            # Raise error if column contains infinite values, because
            # bin width cannot be determined
            if np.inf in column.values or -np.inf in column.values:
                raise InfinityError(column_name=column_name)

            column_quantized = pd.cut(column, self._bin_count, labels=False)
            # Make sure quantized data starts from 1 instead of 0
            column_quantized += 1
            df_output[column_name] = column_quantized
        return DataTable(df_output)

    def _apply_custom_edges_quantization(self, dt: DataTable, selected_columns: list):
        bin_edges = self._parse_bin_edge_list(self._bin_edge_list)

        df_output = pd.DataFrame()
        for column_name in selected_columns:
            column = dt.get_column(column_name)

            # Insert minimum and maximum data to bin_edges to align with V1
            extended_bin_edges = bin_edges
            if min(bin_edges) > min(column):
                extended_bin_edges = [min(column)-1] + bin_edges
            if max(bin_edges) < max(column):
                extended_bin_edges = extended_bin_edges + [max(column) + 1]

            # Mark include_lowest=True to handle -np.inf, otherwise the value after binning is np.nan
            column_quantized = pd.cut(
                column,
                extended_bin_edges,
                labels=False,
                include_lowest=True
            )
            # Make sure quantized data starts from 1 instead of 0
            column_quantized += 1
            df_output[column_name] = column_quantized
        return DataTable(df_output)

    def _apply_entropy_mdl_quantization(self, dt: DataTable, selected_columns: list):
        raise NotImplementedError()

    def _apply_equal_width_custom_quantization(self, dt: DataTable, selected_columns: list):
        raise NotImplementedError()

    def _verify_selected_columns_not_empty(self, data_table: DataTable):
        selected_column_indexes = self._column_filter.select_column_indexes(data_table)
        if not selected_column_indexes:
            raise NoColumnsSelectedError()
        selected_column_names = list(map(data_table.get_column_name, selected_column_indexes))
        return selected_column_names

    @classmethod
    def _verify_input_data_table_not_empty(cls, data_table: DataTable):
        InputParameterChecker.verify_data_table(data_table, data_table.name)

    @classmethod
    def _verify_selected_column_types(cls, dt: DataTable, column_list: list):
        for column_name in column_list:
            column_type = dt.get_column_type(column_name)
            if dt.is_all_na_column(column_name):
                raise ColumnWithAllMissingsError(col_index_or_name=column_name)

            if column_type != ColumnTypeName.NUMERIC:
                raise InvalidColumnTypeError(col_type=column_type, col_name=column_name)

    def _handle_output_mode(self, dt_input: DataTable, dt_output: DataTable):
        if self._output_mode == OutputMode.Append:
            module_logger.info('Append binned columns to the input dataset.')
            self._append_output_data(dt_input, dt_output)
            return dt_input
        elif self._output_mode == OutputMode.Inplace:
            module_logger.info('Replace columns in input dataset with binned columns.')
            self._replace_input_data_with_output(dt_input, dt_output)
            return dt_input
        else:
            module_logger.info('Return just the binned columns.')
            return dt_output

    def _append_output_data(self, dt_input, dt_output):
        for column_name in dt_output.column_names:
            new_column_name = self._rename_column(dt_input.column_names, column_name)
            dt_input.add_column(new_column_name, dt_output.get_column(column_name))

    @staticmethod
    def _replace_input_data_with_output(dt_input, dt_output):
        for column_name in dt_output.column_names:
            dt_input.set_column(column_name, dt_output.get_column(column_name))

    @staticmethod
    def _handle_categorical(dt: DataTable):
        for column_name in dt.column_names:
            dt.set_column_element_type(column_name, ElementTypeName.CATEGORY)

    @classmethod
    def _rename_column(cls, input_column_names, output_column_name):
        new_name = output_column_name + cls.COLUMN_NAME_SUFFIX
        return add_suffix_number_to_avoid_repetition(
            input_str=new_name,
            existed_str_lst=input_column_names,
            starting_suffix_number=2
        )

    @classmethod
    def _parse_bin_edge_list(cls, bin_edge_list_str):
        try:
            bin_edge_str_list = bin_edge_list_str.split(cls.BIN_EDGE_LIST_DELIMITER)
            bin_edge_list = list(map(float, bin_edge_str_list))
        except Exception:
            raise ParameterParsingError(
                arg_name_or_column='Comma-separated list of bin edges',
                to_type='numeric list',
                from_type='string',
                arg_value=bin_edge_list_str
            )

        # Verify if bin_edge_list is in an ascending order
        interval_list = [y - x for x, y in zip(bin_edge_list, bin_edge_list[1:])]
        if interval_list and min(interval_list) <= 0:
            raise NotSortedValuesError(
                arg_name='Comma-separated list of bin edges',
                sorting_order='ascending'
            )

        return bin_edge_list
