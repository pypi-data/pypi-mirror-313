import pandas as pd

from azureml.studio.modulehost.attributes import DataTableInputPort, ModuleMeta, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.core.logger import module_logger as logger, time_profile
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule


class AddColumnsModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Add Columns",
        description="Adds a set of columns from one dataset to another.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="5714a225-befd-438a-9bb5-f6fdc50a4efb",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            table1: DataTableInputPort(
                name="Left dataset",
                friendly_name="Left dataset",
                description="Left dataset",
            ),
            table2: DataTableInputPort(
                name="Right dataset",
                friendly_name="Right dataset",
                description="Right dataset",
            )
    ) -> (
            DataTableOutputPort(
                name="Combined dataset",
                friendly_name="Combined dataset",
                description="Combined dataset",
            ),
    ):
        input_values = locals()

        return AddColumnsModule._run_impl(**input_values),

    @classmethod
    def _run_impl(cls, table1: DataTable, table2: DataTable):
        with ColumnNameResolver(table1, table2):
            logger.info(f"Concat '{cls._args.table1.name}' and '{cls._args.table2.name}' into one.")
            if not _check_input_data_have_same_index_level(table1, table2):
                logger.warning("Reset row indexes of input datasets.")
                table1.data_frame.reset_index(drop=True, inplace=True)
                table2.data_frame.reset_index(drop=True, inplace=True)

            if _check_input_data_have_duplicated_indexes(table1) or \
                    _check_input_data_have_duplicated_indexes(table2):
                logger.warning("Drop row indexes of input datasets because duplicated row indexes were found "
                               "in input datasets. ")
                table1.data_frame.reset_index(drop=True, inplace=True)
                table2.data_frame.reset_index(drop=True, inplace=True)

            combined_data_table = DataTable(pd.concat([table1.data_frame, table2.data_frame], axis=1))

            logger.info(f"Update combined data schema.")
            _merge_table_metadata(combined_data_table.meta_data, table1.meta_data, table2.meta_data)
            return combined_data_table


@time_profile
def _merge_table_metadata(
        combined_meta_data: DataFrameSchema,
        meta_data_1: DataFrameSchema,
        meta_data_2: DataFrameSchema):
    combined_meta_data.score_column_names = meta_data_2.score_column_names
    combined_meta_data.score_column_names = meta_data_1.score_column_names

    if meta_data_2.label_column_name:
        combined_meta_data.label_column_name = meta_data_2.label_column_name
    if meta_data_1.label_column_name:
        combined_meta_data.label_column_name = meta_data_1.label_column_name

    # TODO: add deep update on feature_channels if necessary
    import copy
    combined_meta_data.feature_channels.update(copy.deepcopy(meta_data_2.feature_channels))
    combined_meta_data.feature_channels.update(copy.deepcopy(meta_data_1.feature_channels))


def _check_input_data_have_same_index_level(dt1: DataTable, dt2: DataTable) -> bool:
    return dt1.data_frame.index.nlevels == dt2.data_frame.index.nlevels


def _check_input_data_have_duplicated_indexes(dt: DataTable) -> bool:
    return any(dt.data_frame.index.duplicated())


class ColumnNameResolver:
    def __init__(self, table1: DataTable, table2: DataTable):
        self.table1 = table1
        self.table2 = table2
        self.conflicted_column_names = [value for value in table1.column_names if value in table2.column_names]
        self.column_names_set = set(table1.column_names + table2.column_names)
        self.column_rename_mapping = dict()

    def __enter__(self):
        self._rename_columns(self.table1, self.table2, self.conflicted_column_names)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._revert_columns_rename(self.table1, self.table2, self.conflicted_column_names)

    def _rename_columns(self, table1: DataTable, table2: DataTable, column_names):
        for column_name in column_names:
            suffix_1, new_column_name_1 = self._rename_column_with_suffix(table1, column_name, 1)
            _, new_column_name_2 = self._rename_column_with_suffix(table2, column_name, suffix_1 + 1)
            # Record suffix
            self.column_rename_mapping.update({column_name: (new_column_name_1, new_column_name_2)})

    def _rename_column_with_suffix(self, table: DataTable, column_name, suffix):
        new_column_name = f"{column_name}_{suffix}"
        while new_column_name in self.column_names_set:
            suffix += 1
            new_column_name = f"{column_name}_{suffix}"
        table.rename_column(column_name, new_column_name)
        # Update column_names_set
        self.column_names_set.add(new_column_name)
        return suffix, new_column_name

    def _revert_columns_rename(self, table1: DataTable, table2: DataTable, column_names):
        for column_name in column_names:
            new_column_name_1 = self.column_rename_mapping.get(column_name)[0]
            new_column_name_2 = self.column_rename_mapping.get(column_name)[1]
            table1.rename_column(new_column_name_1, column_name)
            table2.rename_column(new_column_name_2, column_name)
