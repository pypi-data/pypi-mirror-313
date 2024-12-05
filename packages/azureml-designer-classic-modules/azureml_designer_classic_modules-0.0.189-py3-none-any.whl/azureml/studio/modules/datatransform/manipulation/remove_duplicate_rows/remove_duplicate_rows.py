from azureml.studio.modulehost.attributes import ModuleMeta, DataTableInputPort, ColumnPickerParameter, \
    SelectedColumnCategory, BooleanParameter, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import ErrorMapping
from azureml.studio.core.logger import TimeProfile, module_logger
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.core.utils.missing_value_utils import df_isnull


class RemoveDuplicateRowsModule(BaseModule):
    _param_keys = {
        "data_table": "Dataset",
        "key_columns": "Key column selection filter expression",
        "take_first_otherwise_last": "Retain first duplicate row"
    }

    @staticmethod
    @module_entry(ModuleMeta(
        name="Remove Duplicate Rows",
        description="Removes the duplicate rows from a dataset.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="02016f47-e4c3-4a06-9ae5-16c747389e34",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            data_table: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input dataset",
            ),
            key_columns: ColumnPickerParameter(
                name="Key column selection filter expression",
                friendly_name="Key column selection filter expression",
                description="Choose the key columns to use when searching for duplicates",
                column_picker_for="Dataset",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            take_first_otherwise_last: BooleanParameter(
                name="Retain first duplicate row",
                friendly_name="Retain first duplicate row",
                description="indicate whether to keep the first row of a set of duplicates and discard others. "
                            "if false, the last duplicate row encountered will be kept.",
                default_value=True,
            )
    ) -> (
            DataTableOutputPort(
                name="Results dataset",
                friendly_name="Results dataset",
                description="Filtered dataset",
            ),
    ):
        input_values = locals()
        output_values = RemoveDuplicateRowsModule._run_impl(**input_values)

        return output_values

    @classmethod
    def _run_impl(cls, data_table: DataTable, key_columns: DataTableColumnSelection, take_first_otherwise_last: bool):
        cls._validate_arguments(data_table, key_columns)

        min_rows = 2
        if data_table.number_of_rows < min_rows:
            # Always return a clone
            module_logger.warning('Always return a clone of DataTable')
            return data_table.clone(),

        key_include_indices = key_columns.select_column_indexes(data_table)
        key_names = [data_table.get_column_name(idx) for idx in key_include_indices]
        df = data_table.data_frame
        keep = "first" if take_first_otherwise_last else "last"

        # check if any column is selected as key columns
        ErrorMapping.verify_are_columns_selected(curr_selected_num=len(key_names),
                                                 required_selected_num=1,
                                                 arg_name=cls._param_keys['key_columns'])

        with TimeProfile('Remove duplicated rows'):
            # we keep all rows with missing values
            rows_is_null = df_isnull(df, column_names=key_names)
            rows_is_duplicated = df.duplicated(subset=key_names, keep=keep)
            df = df[rows_is_null | ~rows_is_duplicated]
            df.reset_index(drop=True, inplace=True)

        result_table = DataTable(df, data_table.get_meta_data(True))
        return result_table,

    @classmethod
    def _validate_arguments(cls, data_table: DataTable, key_columns: DataTableColumnSelection):
        # check if input dataset is null
        ErrorMapping.verify_not_null_or_empty(data_table, cls._param_keys["data_table"])
        # check if input dataset has columns
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(curr_column_count=data_table.number_of_columns,
                                                                       required_column_count=1,
                                                                       arg_name=cls._param_keys["data_table"])
        # check if key columns is null
        ErrorMapping.verify_not_null_or_empty(key_columns, cls._param_keys["key_columns"])
