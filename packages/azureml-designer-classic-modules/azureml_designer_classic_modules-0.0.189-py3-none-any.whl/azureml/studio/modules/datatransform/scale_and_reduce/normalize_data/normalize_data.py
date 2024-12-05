from azureml.studio.modulehost.attributes import ColumnPickerParameter, ModeParameter, \
    BooleanParameter, DataTableInputPort, ITransformOutputPort, DataTableOutputPort, ModuleMeta, SelectedColumnCategory
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatypes import DataTypes
from azureml.studio.common.error import ErrorMapping, InvalidColumnTypeError
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.core.logger import module_logger
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from .nomalize_transformer import NormalizeTransformer, TransformationMethods


class NormalizeDataModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Normalize Data",
        description="Rescales numeric data to constrain dataset values to a standard range.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="{986DF333-6748-4B85-923D-871DF70D6AAF}",
        release_state=ReleaseState.Release,
        is_deterministic=True
    ))
    def run(
            data_set: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input dataset",
            ),
            method: ModeParameter(
                TransformationMethods,
                name="Transformation method",
                friendly_name="Transformation method",
                description="Choose the mathematical method used for scaling",
                default_value=TransformationMethods.ZScore,
            ),
            column_set: ColumnPickerParameter(
                name="Columns to transform",
                friendly_name="Columns to transform",
                description="Select all columns to which the selected transformation should be applied",
                column_picker_for="Dataset",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.Numeric,),
            ),
            constant_column_option: BooleanParameter(
                name="Use 0 for constant columns when checked",
                friendly_name="Use 0 for constant columns when checked",
                description="Use NaN for constant columns when unchecked or 0 when checked ",
                default_value=True,
                parent_parameter="Transformation method",
                parent_parameter_val=(
                        TransformationMethods.ZScore, TransformationMethods.MinMax, TransformationMethods.LogNormal),
            )
    ) -> (
            DataTableOutputPort(
                data_type=DataTypes.DATASET,
                name="Transformed dataset",
                friendly_name="Transformed dataset",
                description="Transformed dataset",
            ),
            ITransformOutputPort(
                name="Transformation function",
                friendly_name="Transformation function",
                description="Definition of the transformation function, which can be applied to other datasets",
            ),
    ):
        input_values = locals()
        output_values = NormalizeDataModule._run(**input_values)
        return output_values

    @classmethod
    def _check_column_type(cls, data_set: DataTable, column_set):
        """Check the selected column type in data table

        Non-numeric could not be applied numerical normalization operation , so we treat non-numeric as illegal column
        :param data_set: input data set from input input portal
        :param column_set: column selection rule
        :return: None
        Raise error if the selected sub data table contains invalid data type.
        """
        column_indexes = column_set.select_column_indexes(data_set)
        column_names = list(map(data_set.get_column_name, column_indexes))

        illegal_column_names = [n for n in column_names if
                                data_set.get_element_type(n) not in (ElementTypeName.INT, ElementTypeName.FLOAT)]
        if illegal_column_names:
            illegal_column_types = [data_set.get_element_type(n) for n in illegal_column_names]
            ErrorMapping.throw(InvalidColumnTypeError(
                col_name=','.join(illegal_column_names),
                col_type=','.join(illegal_column_types),
                arg_name=cls._args.column_set.friendly_name)
            )

    @staticmethod
    def _run(data_set, method, column_set, constant_column_option):
        module_logger.info("Validating input data.")
        InputParameterChecker.verify_data_table(data_table=data_set, friendly_name="Dataset")
        ErrorMapping.verify_not_null_or_empty(column_set, name="Columns to transform")
        NormalizeDataModule._check_column_type(data_set=data_set, column_set=column_set)
        module_logger.info("Validated input data.")
        module_logger.info(
            f"Data set has {data_set.number_of_rows} Row(s) and {data_set.number_of_columns} Columns.")
        transformer = NormalizeTransformer(data_set, column_set, method, constant_column_option)
        output = transformer.apply(data_set)
        return output, transformer
