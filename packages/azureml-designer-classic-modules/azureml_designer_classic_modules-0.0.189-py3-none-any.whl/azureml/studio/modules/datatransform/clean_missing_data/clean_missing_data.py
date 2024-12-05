from azureml.studio.modulehost.attributes import ItemInfo, ColumnPickerParameter, \
    FloatParameter, StringParameter, ModeParameter, BooleanParameter, IntParameter, DataTableInputPort, \
    ITransformOutputPort, DataTableOutputPort, SelectedColumnCategory
from azureml.studio.modulehost.attributes import ModuleMeta
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.core.logger import module_logger
from azureml.studio.common.types import AutoEnum
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.error import ErrorMapping
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.datatransform.clean_missing_data.clean_missing_transform import \
    CleanMissingValueTransform, CleanMissingDataHandlingPolicy


class ColumnsWithAllValuesMissing(AutoEnum):
    Propagate: ItemInfo(name="Propagate", friendly_name="Propagate") = ()
    Remove: ItemInfo(name="Remove", friendly_name="Remove") = ()


class CleanMissingDataModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name="Clean Missing Data",
        description="Specifies how to handle the values missing from a dataset.",
        category="Data Transformation",
        version="0.1",
        owner="Microsoft Corporation",
        family_id="d2c5ca2f732341a39b7eda917c99f0c4",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            input_data: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                is_optional=False,
                description="Dataset to be cleaned",
            ),
            columns_to_clean: ColumnPickerParameter(
                name="Columns to be cleaned",
                is_optional=False,
                column_picker_for="Dataset",
                single_column_selection=False,
                description="Columns for missing values clean operation",
                column_selection_categories=(SelectedColumnCategory.All,)
            ),
            min_ratio: FloatParameter(
                name="Minimum missing value ratio",
                is_optional=False,
                min_value=0.0,
                max_value=1.0,
                default_value=0.0,
                description="Clean only column with missing value ratio above specified value, "
                            "out of set of all selected columns",
            ),
            max_ratio: FloatParameter(
                name="Maximum missing value ratio",
                is_optional=False,
                min_value=0.0,
                max_value=1.0,
                default_value=1.0,
                description="Clean only columns with missing value ratio below specified value, "
                            "out of set of all selected columns",
            ),
            cleaning_mode: ModeParameter(
                CleanMissingDataHandlingPolicy,
                name="Cleaning mode",
                is_optional=False,
                default_value=CleanMissingDataHandlingPolicy.ReplaceWithValue,
                description="Algorithm to clean missing values",
            ),
            replacement_value: StringParameter(
                name="Replacement value",
                is_optional=True,
                parent_parameter="Cleaning mode",
                parent_parameter_val=[CleanMissingDataHandlingPolicy.ReplaceWithValue],
                default_value="0",
                description="Type the value that takes the place of missing values",
            ),
            cols_with_all_missing: ModeParameter(
                ColumnsWithAllValuesMissing,
                name="Cols with all missing values",
                is_optional=False,
                parent_parameter="Cleaning mode",
                parent_parameter_val=[
                    CleanMissingDataHandlingPolicy.ReplaceUsingMICE,
                    CleanMissingDataHandlingPolicy.ReplaceWithMean,
                    CleanMissingDataHandlingPolicy.ReplaceWithMedian,
                    CleanMissingDataHandlingPolicy.ReplaceWithMode,
                ],
                default_value=ColumnsWithAllValuesMissing.Remove,
                description="Cols with all missing values"),
            generate_missing_value_indicator_column: BooleanParameter(
                name="Generate missing value indicator column",
                is_optional=False,
                parent_parameter="Cleaning mode",
                parent_parameter_val=[
                    CleanMissingDataHandlingPolicy.ReplaceUsingMICE,
                    CleanMissingDataHandlingPolicy.ReplaceUsingProbabilisticPca,
                    CleanMissingDataHandlingPolicy.ReplaceWithMean,
                    CleanMissingDataHandlingPolicy.ReplaceWithMedian,
                    CleanMissingDataHandlingPolicy.ReplaceWithMode,
                    CleanMissingDataHandlingPolicy.ReplaceWithValue,
                ],
                default_value=False,
                description="Generate a column that indicates which rows were cleaned"),
            number_of_iterations: IntParameter(
                name="Number of Iterations",
                is_optional=False,
                parent_parameter="Cleaning mode",
                parent_parameter_val=[CleanMissingDataHandlingPolicy.ReplaceUsingMICE],
                min_value=1,
                max_value=10,
                default_value=5,
                description="Specify the number of iterations when using MICE",
            ),
            number_of_iterations_for_pca_prediction: IntParameter(
                name="Number of Iterations for PCA Prediction",
                is_optional=False,
                parent_parameter="Cleaning mode",
                parent_parameter_val=[CleanMissingDataHandlingPolicy.ReplaceUsingProbabilisticPca],
                min_value=1,
                max_value=50,
                default_value=10,
                description="Specify the number of iterations when using PCA prediction",
            ),
    ) -> (
        DataTableOutputPort(
            name="Cleaned dataset",
            friendly_name="Cleaned dataset",
            description="Cleaned dataset",
        ),
        ITransformOutputPort(
            name="Cleaning transformation",
            friendly_name="Cleaning transformation",
            description="Transformation to be passed to Apply Transformation module to clean new data",
        ),
    ):
        input_values = locals()
        return CleanMissingDataModule._run_impl(**input_values)

    @classmethod
    def _run_impl(
            cls,
            input_data: DataTable,
            columns_to_clean: DataTableColumnSelection,
            min_ratio: float,
            max_ratio: float,
            cleaning_mode: CleanMissingDataHandlingPolicy,
            replacement_value: str,
            cols_with_all_missing: ColumnsWithAllValuesMissing,
            generate_missing_value_indicator_column: bool,
            number_of_iterations: int,
            number_of_iterations_for_pca_prediction: int):

        ErrorMapping.verify_not_null_or_empty(x=input_data, name=cls._args.input_data.friendly_name)

        remove_columns_with_all_missing = (cols_with_all_missing is ColumnsWithAllValuesMissing.Remove)
        if remove_columns_with_all_missing:
            module_logger.info('Remove columns with all missing values')

        module_logger.info('Select column indexes')
        selected_column_indexes = columns_to_clean.select_column_indexes(input_data)

        module_logger.info('Initialize CleanMissingValueTransform instance')

        transform = CleanMissingValueTransform(
            cleaning_mode=cleaning_mode,
            replacement_value=replacement_value,
            remove_columns_with_all_missing=remove_columns_with_all_missing,
            indicator_columns=generate_missing_value_indicator_column,
            column_names=list(map(input_data.get_column_name, selected_column_indexes)),
            min_ratio=min_ratio,
            max_ratio=max_ratio)

        module_logger.info('Apply CleanMissingValueTransform')
        output_data = transform.apply(input_data)
        return output_data, transform
