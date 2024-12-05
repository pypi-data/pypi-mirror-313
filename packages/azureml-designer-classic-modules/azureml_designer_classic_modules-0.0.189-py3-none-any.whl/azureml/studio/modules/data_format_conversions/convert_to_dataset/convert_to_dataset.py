import numpy as np
from pandas.api.types import is_categorical_dtype

from azureml.studio.modulehost.attributes import ItemInfo, DataTableInputPort, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import StringParameter, ModeParameter
from azureml.studio.common.datatable.constants import ElementTypeName
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_type_conversion import try_convert_str_by_element_type, try_convert_str
from azureml.studio.common.types import AutoEnum
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule, ModuleMeta
from azureml.studio.core.utils.missing_value_utils import fill_na, has_na, is_na


class ConvertToDatasetActionMethod(AutoEnum):
    NONE: ItemInfo(name="None", friendly_name="None") = ()
    SetMissingValues: ItemInfo(name="SetMissingValues", friendly_name="SetMissingValues") = ()
    ReplaceValues: ItemInfo(name="ReplaceValues", friendly_name="ReplaceValues") = ()


class ConvertToDatasetReplaceMethod(AutoEnum):
    Missing: ItemInfo(name="Missing", friendly_name="Missing") = ()
    Custom: ItemInfo(name="Custom", friendly_name="Custom") = ()


class ConvertToDatasetModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name="Convert to Dataset",
        description="Converts data input to the internal Dataset format used by Azure Machine Learning designer.",
        category="Data Transformation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="72BF58E0-FC87-4BB1-9704-F1805003B975",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            table: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input dataset",
            ),
            action: ModeParameter(
                ConvertToDatasetActionMethod,
                name="Action",
                friendly_name="Action",
                description="Action to apply to input dataset",
                default_value=ConvertToDatasetActionMethod.NONE,
            ),
            custom_missing_value: StringParameter(
                name="Custom Missing Value",
                friendly_name="Custom missing value",
                description="Value indicating missing value token",
                default_value="?",
                parent_parameter="Action",
                parent_parameter_val=(ConvertToDatasetActionMethod.SetMissingValues, ),
            ),
            to_remove: ModeParameter(
                ConvertToDatasetReplaceMethod,
                name="Replace",
                friendly_name="Replace",
                description="Specifies type of replacement for values",
                default_value=ConvertToDatasetReplaceMethod.Missing,
                parent_parameter="Action",
                parent_parameter_val=(ConvertToDatasetActionMethod.ReplaceValues, ),
            ),
            from_custom_remove: StringParameter(
                name="Custom Value",
                friendly_name="Custom value",
                description="Value to be replaced",
                default_value="obs",
                parent_parameter="Replace",
                parent_parameter_val=(ConvertToDatasetReplaceMethod.Custom, ),
            ),
            replace_with: StringParameter(
                name="New Value",
                friendly_name="New value",
                description="Replacement value",
                default_value="0",
                parent_parameter="Action",
                parent_parameter_val=(ConvertToDatasetActionMethod.ReplaceValues, ),
            ),
    ) -> (
            DataTableOutputPort(
                name="Results dataset",
                friendly_name="Results dataset",
                description="Output dataset",
            ),
    ):
        input_values = locals()
        output_values = ConvertToDatasetModule.run_impl(**input_values)
        return output_values

    @classmethod
    def run_impl(
            cls,
            table: DataTable,
            action: ConvertToDatasetActionMethod = ConvertToDatasetActionMethod.NONE,
            custom_missing_value: str = '?',
            to_remove: ConvertToDatasetReplaceMethod = ConvertToDatasetReplaceMethod.Missing,
            from_custom_remove: str = 'obs',
            replace_with: str = '0',
    ):
        if action == ConvertToDatasetActionMethod.NONE:
            return table,
        elif action == ConvertToDatasetActionMethod.SetMissingValues:
            return cls.set_missing_values(table, custom_missing_value)
        elif action == ConvertToDatasetActionMethod.ReplaceValues:
            return cls.replace_values(table, to_remove, from_custom_remove, replace_with)
        raise NotImplementedError(f"The action {action} is not implemented in module {cls.__name__}")

    @staticmethod
    def replace_values(
            table: DataTable,
            to_remove: ConvertToDatasetReplaceMethod,
            from_custom_remove: str,
            replace_with: str
    ):
        if to_remove == ConvertToDatasetReplaceMethod.Custom:
            return ConvertToDatasetModule.replace_custom_values(table, from_custom_remove, replace_with)
        elif to_remove == ConvertToDatasetReplaceMethod.Missing:
            return ConvertToDatasetModule.replace_missing_values(table, replace_with)
        raise NotImplementedError(f"The replace method {to_remove} is not implemented.")

    @staticmethod
    def indexes_could_update(table: DataTable, str_vals: tuple, include_nan=False):
        """Compute which columns could be updated according the column types and the values."""
        index_with_values = []
        # For NAN types, directly replace the str vals.
        # This is a fix for bug 548645
        type2values = {}
        if include_nan:
            # If we need to update the column with only NAN values,
            # we will try convert the str_val to a valid scalar according to the following order:
            # BOOL, INT, FLOAT, DATETIME, STR
            # This behavior is following v1.
            type2values[ElementTypeName.NAN] = tuple((try_convert_str(val) for val in str_vals))
        for i in range(table.number_of_columns):
            is_all_na_column = table.is_all_na_column(i)
            if is_all_na_column and \
                    not include_nan:
                continue

            # We should get the underlying element type so category type can also be correctly updated.
            elm_type = table.get_underlying_element_type(i)
            vals = []
            if is_all_na_column:
                vals = type2values[ElementTypeName.NAN]
            elif elm_type in type2values:
                # For the type that we have tried, use the existing values to avoid redundant computation.
                vals = type2values[elm_type]
            else:
                # Otherwise, try whether all the values could be converted to a valid value.
                for str_val in str_vals:
                    val = try_convert_str_by_element_type(str_val, elm_type)
                    if is_na(val):
                        break
                    vals.append(val)
                type2values[elm_type] = vals

            # If len(vals) == len(str_vals), all the values are correctly converted, this column could be updated.
            if len(vals) == len(str_vals):
                index_with_values.append((i, vals))

        return index_with_values

    @staticmethod
    def replace_custom_values(table: DataTable, from_custom_remove: str, replace_with: str):
        index_with_values = ConvertToDatasetModule.indexes_could_update(table, (from_custom_remove, replace_with))
        for i, values in index_with_values:
            custom_val, replace_val = values
            column = table.get_column(i)
            column.replace(custom_val, replace_val, inplace=True)
            # After replacement, the dataframe will be changed to underlying dtype, so we should update it.
            if table.get_element_type(i) is ElementTypeName.CATEGORY:
                column = column.astype('category')
            table.set_column(i, column)
        return table,

    @staticmethod
    def replace_missing_values(table: DataTable, replace_with: str):
        index_with_values = ConvertToDatasetModule.indexes_could_update(table, (replace_with,), include_nan=True)
        for i, values in index_with_values:
            val, = values
            column = table.get_column(i)
            # If column is category type, when we call fill_na with a non-exist category,
            # the categories of the column will be updated, which is not expected.
            if not has_na(column):
                continue
            fill_na(column, val, inplace=True)
            table.set_column(i, column)
        return table,

    @staticmethod
    def set_missing_values(table: DataTable, custom_missing_value: str):
        index_with_values = ConvertToDatasetModule.indexes_could_update(table, (custom_missing_value,))
        for i, values in index_with_values:
            val, = values
            column = table.get_column(i)
            column.replace(to_replace=val, value=np.nan, inplace=True)
            if is_categorical_dtype(column) and val in column.cat.categories:
                column.cat.remove_categories([val], inplace=True)
            table.set_column(i, column)
        return table,
