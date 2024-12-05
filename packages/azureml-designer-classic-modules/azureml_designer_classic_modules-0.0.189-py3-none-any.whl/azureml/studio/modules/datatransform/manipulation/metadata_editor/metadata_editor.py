import re

from azureml.studio.core.logger import module_logger
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.attributes import ItemInfo as ItemInfo, DataTableInputPort, ColumnPickerParameter, \
    ModeParameter, StringParameter, ModuleMeta, DataTableOutputPort, SelectedColumnCategory
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.error import ErrorMapping, MultipleLabelColumnsError, InconsistentSizeError, \
    DuplicatedColumnNameError, ErrorConvertingColumnError, CouldNotConvertColumnError, TooFewColumnsInDatasetError, \
    TooFewColumnsSelectedError, ParameterParsingError
from azureml.studio.modulehost.constants import ElementTypeName, ColumnTypeName
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule


class MetadataEditorDataType(AutoEnum):
    Unchanged: ItemInfo(name='Unchanged', friendly_name='Unchanged') = ()
    String: ItemInfo(name='String', friendly_name='String') = ()
    Integer: ItemInfo(name='Integer', friendly_name='Integer') = ()
    Double: ItemInfo(name='Double', friendly_name='Double') = ()
    Boolean: ItemInfo(name='Boolean', friendly_name='Boolean') = ()
    DateTime: ItemInfo(name='DateTime', friendly_name='DateTime') = ()
    TimeSpan: ItemInfo(name='TimeSpan', friendly_name='TimeSpan', release_state=ReleaseState.Alpha) = ()


class MetadataEditorCategorical(AutoEnum):
    Unchanged: ItemInfo(name='Unchanged', friendly_name='Unchanged') = ()
    Categorical: ItemInfo(name='Categorical', friendly_name='Make Categorical') = ()
    NonCategorical: ItemInfo(name='NonCategorical', friendly_name='Make non-categorical') = ()


class MetadataEditorFlag(AutoEnum):
    Unchanged: ItemInfo(name='Unchanged', friendly_name='Unchanged') = ()
    Features: ItemInfo(name='Features', friendly_name='Features') = ()
    Labels: ItemInfo(name='Labels', friendly_name='Label') = ()
    Weights: ItemInfo(name='Weights', friendly_name='Weight', release_state=ReleaseState.Alpha) = ()
    ClearFeatures: ItemInfo(name='ClearFeatures', friendly_name='Clear feature') = ()
    ClearLabels: ItemInfo(name='ClearLabels', friendly_name='Clear label') = ()
    ClearScores: ItemInfo(name='ClearScores', friendly_name='Clear score') = ()
    ClearWeights: ItemInfo(name='ClearWeights', friendly_name='Clear weight', release_state=ReleaseState.Alpha) = ()


class MetadataEditorModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Edit Metadata",
        description="Edits metadata associated with columns in a dataset.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="370B6676-C11C-486F-BF73-35349F842A66",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            table: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input dataset",
            ),
            column_select: ColumnPickerParameter(
                name="Column",
                friendly_name="Column",
                description="Choose the columns to which your changes should apply",
                column_picker_for="Dataset",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.All, ),
            ),
            new_data_type: ModeParameter(
                MetadataEditorDataType,
                name="Data Type",
                friendly_name="Data type",
                description="Specify the new data type of the column",
                default_value=MetadataEditorDataType.Unchanged,
            ),
            new_categorical: ModeParameter(
                MetadataEditorCategorical,
                name="Categorical",
                friendly_name="Categorical",
                description="Indicate whether the column should be flagged as categorical",
                default_value=MetadataEditorCategorical.Unchanged,
            ),
            new_field: ModeParameter(
                MetadataEditorFlag,
                name="Fields",
                friendly_name="Fields",
                description="Specify whether the column should be considered a feature"
                            " or label by learning algorithms",
                default_value=MetadataEditorFlag.Unchanged,
            ),
            new_column_names: StringParameter(
                name="New Column Name",
                friendly_name="New column names",
                is_optional=True,
                description="Type the new names of the columns",
            ),
            date_time_format: StringParameter(
                name="Date and time Format",
                friendly_name="DateTime format",
                is_optional=True,
                description="Specify custom format string for parsing DateTime,"
                            " refer to Python standard library datetime.strftime() for detailed documentation."
                            " Leave empty for default permissive parsing",
                parent_parameter="Data Type",
                parent_parameter_val=(MetadataEditorDataType.DateTime, ),
            ),
            time_span_format: StringParameter(
                name="TimeSpan Format",
                friendly_name="TimeSpan Format",
                is_optional=True,
                description="Specify custom .NET format string for parsing TimeSpan."
                            " Leave empty for default permissive parsing",
                parent_parameter="Data Type",
                parent_parameter_val=(MetadataEditorDataType.TimeSpan, ),
            )
    ) -> (
            DataTableOutputPort(
                name="Results dataset",
                friendly_name="Results dataset",
                description="Dataset with changed metadata",
            ),
    ):
        input_values = locals()
        return MetadataEditorModule._run_impl(**input_values),

    @classmethod
    def _run_impl(
            cls,
            table: DataTable,
            column_select: DataTableColumnSelection,
            new_data_type: MetadataEditorDataType,
            new_categorical: MetadataEditorCategorical,
            new_field: MetadataEditorFlag,
            new_column_names: str,
            date_time_format: str,
            time_span_format: str):

        ErrorMapping.verify_not_null_or_empty(x=table, name=cls._args.table.friendly_name)
        ErrorMapping.verify_not_null_or_empty(x=column_select, name=cls._args.column_select.friendly_name)

        if table.number_of_columns == 0:
            ErrorMapping.throw(TooFewColumnsInDatasetError(
                arg_name=cls._args.table.friendly_name, required_columns_count=1))

        table = table.clone()
        selected_col_indexes = column_select.select_column_indexes(table)

        if len(selected_col_indexes) == 0:
            ErrorMapping.throw(TooFewColumnsSelectedError(
                arg_name=cls._args.table.friendly_name, required_columns_count=1))

        module_logger.info('Change columns element type')
        cls.change_columns_element_type(
            table, selected_col_indexes, new_data_type, date_time_format,
            time_span_format)

        module_logger.info('Change categorical columns')
        cls.change_categorical_columns(
            table, selected_col_indexes, new_categorical)

        module_logger.info('Change feature label columns')
        cls.change_feature_label_columns(
            table, selected_col_indexes, new_field)

        module_logger.info('Change column names')
        cls.change_column_names(table, selected_col_indexes, new_column_names)

        return table

    @classmethod
    def change_columns_element_type(
            cls,
            dt,
            selected_col_indexes,
            new_data_type,
            date_time_format,
            time_span_format):

        if new_data_type != MetadataEditorDataType.Unchanged:
            for selected_col_index in selected_col_indexes:
                cls._change_column_element_type(
                    dt, selected_col_index, new_data_type, date_time_format, time_span_format)
        else:
            return

    @classmethod
    def change_categorical_columns(cls, dt, selected_col_indexes, new_categorical):

        if new_categorical != MetadataEditorCategorical.Unchanged:
            for selected_col_index in selected_col_indexes:
                cls._change_categorical_column(
                    dt, selected_col_index, new_categorical)
        else:
            return

    @classmethod
    def change_feature_label_columns(cls, dt, col_indexes, new_field):
        if new_field == MetadataEditorFlag.Unchanged:
            return

        elif new_field == MetadataEditorFlag.Features:
            for col_index in col_indexes:
                dt.meta_data.set_column_as_feature(col_index)

        elif new_field == MetadataEditorFlag.Labels:
            if len(col_indexes) != 1:
                ErrorMapping.throw(MultipleLabelColumnsError())

            dt.meta_data.label_column_name = col_indexes[0]

        elif new_field == MetadataEditorFlag.Weights:
            raise NotImplementedError('Weights has not been implemented')

        elif new_field == MetadataEditorFlag.ClearFeatures:
            for col_index in col_indexes:
                dt.meta_data.get_column_attribute(col_index).is_feature = False

        elif new_field == MetadataEditorFlag.ClearLabels:
            del dt.meta_data.label_column_name

        elif new_field == MetadataEditorFlag.ClearScores:
            del dt.meta_data.score_column_names

        elif new_field == MetadataEditorFlag.ClearWeights:
            raise NotImplementedError('ClearWeights has not been implemented')

        else:
            ErrorMapping.throw(
                ParameterParsingError(arg_name_or_column=cls._args.new_field.friendly_name))

    @classmethod
    def change_column_names(cls, dt, selected_col_indexes, new_col_names):

        if new_col_names:  # Might need to be changed in the future
            new_name_list = new_col_names.split(',')

            if len(new_name_list) != len(selected_col_indexes):
                ErrorMapping.throw(
                    InconsistentSizeError(
                        friendly_name1=cls._args.new_column_names.friendly_name,
                        friendly_name2=cls._args.column_select.friendly_name
                    )
                )

            # Check if new_name_list contains duplicated names,
            # or new_name_list contains the same name as the existing column names
            # If true, raise Error
            checked_new_names = set()
            for name in new_name_list:
                if name in checked_new_names:
                    ErrorMapping.throw(
                        DuplicatedColumnNameError(
                            duplicated_name=name,
                            arg_name=cls._args.new_column_names.friendly_name
                        )
                    )
                # Fix bug: 444893
                elif name in dt.column_names:
                    ErrorMapping.throw(
                        DuplicatedColumnNameError(
                            duplicated_name=name,
                            arg_name="column names in input dataset"
                        )
                    )
                else:
                    checked_new_names.add(name)

            for index in range(len(selected_col_indexes)):
                dt.rename_column(selected_col_indexes[index], new_name_list[index])
        else:
            return

    @classmethod
    def _change_column_element_type(
            cls,
            dt,
            col_index,
            new_data_type,
            date_time_format,
            time_span_format):

        if new_data_type == MetadataEditorDataType.Unchanged:
            return
        elif new_data_type == MetadataEditorDataType.String:
            new_type = ElementTypeName.STRING
            new_col_type = ColumnTypeName.STRING
        elif new_data_type == MetadataEditorDataType.Integer:
            new_type = ElementTypeName.INT
            new_col_type = ColumnTypeName.NUMERIC
        elif new_data_type == MetadataEditorDataType.Double:
            new_type = ElementTypeName.FLOAT
            new_col_type = ColumnTypeName.NUMERIC
        elif new_data_type == MetadataEditorDataType.Boolean:
            new_type = ElementTypeName.BOOL
            new_col_type = ColumnTypeName.BINARY
        elif new_data_type == MetadataEditorDataType.DateTime:
            new_type = ElementTypeName.DATETIME
            new_col_type = ColumnTypeName.DATETIME
        elif new_data_type == MetadataEditorDataType.TimeSpan:
            new_type = ElementTypeName.TIMESPAN
            new_col_type = ColumnTypeName.TIMESPAN
        else:
            ErrorMapping.throw(
                ParameterParsingError(arg_name_or_column=cls._args.new_data_type.friendly_name))

        try:
            # This is a feature to align with V1.
            if new_data_type in (MetadataEditorDataType.Double, MetadataEditorDataType.Integer) and \
                    dt.get_column_type(col_index) == ColumnTypeName.STRING:
                cls._preprocess_column_before_converting_str_to_numeric(dt, col_index, new_data_type)

            dt.set_column_element_type(col_index, new_type, date_time_format, time_span_format)
        except BaseException as e:
            # For a column of all missing values, if conversion error occurs, only change meta data to
            # the target type.
            if dt.is_all_na_column(col_index):
                dt.meta_data.column_attributes[col_index].column_type = new_col_type
                dt.meta_data.column_attributes[col_index].element_type = new_type
            else:
                ErrorMapping.rethrow(e, CouldNotConvertColumnError(type1=dt.get_column_type(col_index), type2=new_type))
        return

    @classmethod
    def _preprocess_column_before_converting_str_to_numeric(cls, dt, col_index, new_data_type):
        if new_data_type == MetadataEditorDataType.Double:
            preprocess_method = cls._preprocess_element_before_converting_str_to_double
        else:
            preprocess_method = cls._preprocess_element_before_converting_str_to_int

        column = dt.get_column(col_index)
        processed_column = column.apply(preprocess_method)
        # Do not re-compute meta to save computational time. Since the column type is still string.
        dt.set_column(col_index, processed_column, update_meta=False)

    @staticmethod
    def _preprocess_element_before_converting_str_to_int(element):
        # Truncate spaces in the end.
        if isinstance(element, str):
            return element.rstrip()
        return element

    @staticmethod
    def _preprocess_element_before_converting_str_to_double(element):
        if isinstance(element, str):
            if "." in element:
                integer, decimal = element.split(".")
            else:
                integer, decimal = element, ""

            if re.compile("[0-9]+,?").match(integer) and "," not in decimal:
                return element.replace(",", "")

        return element

    @classmethod
    def _change_categorical_column(cls, dt, col_index, new_categorical):
        try:
            if new_categorical == MetadataEditorCategorical.Unchanged:
                return
            elif new_categorical == MetadataEditorCategorical.Categorical:
                dt.set_column_element_type(col_index, ElementTypeName.CATEGORY)
            elif new_categorical == MetadataEditorCategorical.NonCategorical:
                dt.set_column_element_type(col_index, ElementTypeName.UNCATEGORY)
            else:
                ErrorMapping.throw(
                    ParameterParsingError(arg_name_or_column=cls._args.new_categorical.friendly_name))
        except BaseException as e:
            ErrorMapping.rethrow(e, ErrorConvertingColumnError(target_type=cls._args.new_categorical.friendly_name))
