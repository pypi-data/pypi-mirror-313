from azureml.studio.common.datatable.data_table import DataTableColumnSelection, DataTable
from azureml.studio.modulehost.attributes import DataTableInputPort, ColumnPickerParameter, \
    DataTableOutputPort, SelectedColumnCategory
from azureml.studio.modulehost.attributes import ModuleMeta
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.core.logger import module_logger as logger
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule


class SelectColumnsModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Select Columns in Dataset",
        description="Selects columns to include or exclude from a dataset in an operation.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="{1ec722fa-b623-4e26-a44e-a50c6d726223}",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            table: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input dataset",
            ),
            feature_list: ColumnPickerParameter(
                name="Select Columns",
                friendly_name="Select columns",
                description="Select columns to keep in the projected dataset",
                column_picker_for="Dataset",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.All,),
            )
    ) -> (
            DataTableOutputPort(
                name="Results dataset",
                friendly_name="Results dataset",
                description="Output dataset",
            ),
    ):
        input_values = locals()
        return SelectColumnsModule._run_impl(table, feature_list)

    @classmethod
    def _run_impl(cls, dt: DataTable, column_select: DataTableColumnSelection):
        logger.info(f"Select column indexes from {cls._args.table.name}")
        return column_select.select(dt, if_clone=False),
