from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.error import ErrorMapping
from azureml.studio.common.error import TooFewColumnsSelectedError, InvalidColumnCategorySelectedError
from azureml.studio.core.logger import module_logger
from azureml.studio.modulehost.attributes import ColumnPickerParameter, \
    BooleanParameter, DataTableInputPort, \
    ITransformOutputPort, DataTableOutputPort, SelectedColumnCategory
from azureml.studio.modulehost.attributes import ModuleMeta, ReleaseState
from azureml.studio.modulehost.constants import ColumnTypeName
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.datatransform.common.named_encoder import NamedOneHotEncoder
from azureml.studio.modules.datatransform.manipulation.convert_to_indicator_values. \
    convert_to_indicator_values_transform import ConvertToIndicatorValuesTransform


class ConvertToIndicatorValuesModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Convert to Indicator Values",
        description="Converts categorical values in columns to indicator values.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="6EA59C36-F283-410E-B34C-EDFABFAC39B0",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            table: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Dataset with categorical columns",
            ),
            column_select: ColumnPickerParameter(
                name="Categorical columns to convert",
                friendly_name="Categorical columns to convert",
                description="Select categorical columns to convert to indicator matrices.",
                column_picker_for="Dataset",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            overwrite: BooleanParameter(
                name="Overwrite categorical columns",
                friendly_name="Overwrite categorical columns",
                description="If True, overwrite the selected categorical columns, "
                            "otherwise append the resulting indicator matrices to the dataset",
                is_optional=True,
                default_value=False,
            ),
    ) -> (
            DataTableOutputPort(
                name="Results dataset",
                friendly_name="Results dataset",
                description="Dataset with categorical columns converted to indicator matrices.",
            ),
            ITransformOutputPort(
                name="Indicator values transformation",
                friendly_name="Indicator values transformation",
                description="Transformation to be passed to Apply Transformation module to convert "
                            "indicator values for new data",
            ),
    ):
        input_values = locals()
        return ConvertToIndicatorValuesModule._run_impl(**input_values)

    @classmethod
    def _run_impl(
            cls,
            table: DataTable,
            column_select: DataTableColumnSelection,
            overwrite: bool = False):
        """Generate indicator values of selected categorical columns with correct meta data

        :param table: DataTable
        :param column_select: ColumnSelection
        :param overwrite: bool
        :return: DataTable
        """
        ErrorMapping.verify_not_null_or_empty(x=table, name=cls._args.table.friendly_name)
        ErrorMapping.verify_not_null_or_empty(x=column_select, name=cls._args.column_select.friendly_name)
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=table.number_of_columns, required_column_count=1, arg_name=cls._args.table.friendly_name)
        selected_col_indices = column_select.select_column_indexes(table)
        if len(selected_col_indices) == 0:
            ErrorMapping.throw(TooFewColumnsSelectedError(
                arg_name=cls._args.table.friendly_name, required_columns_count=1))

        module_logger.info('Get target categorical column indices')
        # Need to get target categorical column indices in case we have to overwrite them
        target_category_col_indices = []
        target_category_col_names = []
        for index in sorted(selected_col_indices):
            if table.get_column_type(index) == ColumnTypeName.CATEGORICAL:
                target_category_col_indices.append(index)
                target_category_col_names.append(table.get_column_name(index))
            else:
                col_name = table.get_column_name(index)
                # Will throw InvalidColumnCategorySelectedError if any selected column is not categorical
                ErrorMapping.throw(InvalidColumnCategorySelectedError(
                    col_name=col_name,
                    troubleshoot_hint=f'See https://aka.ms/aml/edit-metadata and make column "{col_name}" '
                                      'categorical in advance.'))

        # Record encoder for transformation
        named_encoder_dict = {}
        for cur_col_name in target_category_col_names:
            module_logger.info(f'For categorical column {cur_col_name}, generate indicator dataframe')
            cur_col_series = table.data_frame[cur_col_name]
            cur_named_encoder = cls.generate_encoder(cur_col_series, cur_col_name)
            named_encoder_dict[cur_named_encoder.column_name] = cur_named_encoder

        transform = ConvertToIndicatorValuesTransform(
            named_encoder_dict=named_encoder_dict,
            target_category_col_names=target_category_col_names,
            overwrite=overwrite
        )
        output_data = transform.apply(table)
        return output_data, transform

    @staticmethod
    def generate_encoder(series, col_name):
        """Generate named one hot encoder by fitting on series.

        :param series: pd.Series
        :param col_name: str
        :return:
        """
        named_encoder = NamedOneHotEncoder(col_name)
        named_encoder.fit(series)
        return named_encoder
