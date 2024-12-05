from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import ErrorMapping
from azureml.studio.core.logger import module_logger as logger
from azureml.studio.modulehost.attributes import ModuleMeta, DataTableInputPort, ITransformOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.module_reflector import BaseModule, module_entry
from azureml.studio.modules.datatransform.common.base_transform import BaseTransform


class SelectColumnsTransformModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Select Columns Transform",
        description="Create a transformation that selects the same subset of columns as in the given dataset.",
        category="Data Transformation",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="AA517DA1-4978-43ED-960F-F26CF55BFA95",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            table: DataTableInputPort(
                name="Dataset with desired columns",
                friendly_name="Dataset with desired columns",
                description="Dataset containing desired set of columns",
            )
    ) -> (
            ITransformOutputPort(
                name="Columns selection transformation",
                friendly_name="Columns selection transformation",
                description="Transformation that selects the same subset of columns as in the given dataset.",
            ),
    ):
        return SelectColumnsTransformModule._run_impl(table)

    @classmethod
    def _run_impl(cls, dt: DataTable):
        logger.info('Initialize SelectColumnsTransform instance')
        column_names = dt.column_names
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=len(column_names),
            required_column_count=1,
            arg_name=cls._args.table.friendly_name
        )

        transform = SelectColumnsTransform(column_names)
        return transform,


class SelectColumnsTransform(BaseTransform):
    def __init__(self, column_names):
        self.columns_to_select = set(column_names)

    def apply(self, dt: DataTable):
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=len(dt.column_names),
            required_column_count=1,
            arg_name='Dataset'
        )

        meta_data = dt.meta_data
        score_column_names = set(meta_data.score_column_names.values())
        label_column_name = meta_data.label_column_name
        logger.info(f"Found {len(score_column_names)} score columns and {1 if label_column_name else 0} label column")

        def should_be_transformed(col_name):
            return col_name in self.columns_to_select \
                   or col_name in score_column_names \
                   or col_name == label_column_name

        selected_column_indexes = [
            dt.get_column_index(col_name) for col_name in dt.column_names if should_be_transformed(col_name)]

        return dt.get_slice_by_column_indexes(
            column_indexes=selected_column_indexes,
            if_clone=True
        )
