import pandas as pd

from azureml.studio.common.datatable.data_table import DataTable, DataTableColumnSelection
from azureml.studio.common.error import ErrorMapping, InvalidColumnTypeError, _raise_deprecated_error
from azureml.studio.core.logger import TimeProfile
from azureml.studio.modulehost.attributes import ModuleMeta, DataTableInputPort, \
    ColumnPickerParameter, SelectedColumnCategory, IntParameter, DataTableOutputPort
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule


class FeatureHashingModule(BaseModule):
    MAX_COLUMN = 100000
    HASHING_FEATURE_POSTFIX = '_HashingFeature'

    @staticmethod
    @module_entry(ModuleMeta(
        name="Feature Hashing",
        description="""IMPORTANT NOTICE: This component HAS BEEN DEPRECATED because its dependency, the NimbusML project (https://github.com/microsoft/NimbusML), is no longer actively maintained. As a result, this component will not receive future updates or security patches.
We plan to remove this component in upcoming releases. Users are recommended to migrate to alternative solutions to ensure continued support and security.
Convert text data to numeric features using the nimbusml.""", # noqa
        category="Text Analytics",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="C9A82660-2D9C-411D-8122-4D9E0B3CE92A",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            dataset: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input dataset",
            ),
            target_column: ColumnPickerParameter(
                name="Target column",
                friendly_name="Target column",
                description="Choose the columns to which hashing will be applied",
                column_picker_for="Dataset",
                single_column_selection=False,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            bits: IntParameter(
                name="Hashing bitsize",
                friendly_name="Hashing bitsize",
                description="Type the number of bits used to hash the selected columns",
                default_value=10,
                min_value=1,
                max_value=31,
            ),
            ngrams: IntParameter(
                name="N-grams",
                friendly_name="N-grams",
                description="Specify the number of N-grams generated during hashing",
                default_value=2,
                min_value=0,
                max_value=10,
            )
    ) -> (
            DataTableOutputPort(
                name="Transformed dataset",
                friendly_name="Transformed dataset",
                description="Output dataset with hashed columns,"
                            "the number of feature columns generated is related to the parameters(Hashing bitsize).",
            ),
    ):
        input_values = locals()
        output_values = FeatureHashingModule.create_feature_hashing_module(**input_values)
        return output_values

    @classmethod
    def _check_column_type(cls, data_set: DataTable, column_set):
        """Check the selected column type in data table

        Non-string data cannot be performed to do feature hashing, so we treat non-string as illegal column
        :param data_set: input data set
        :param column_set: column selection rule
        :return: None
        Raise error if the selected sub data table contains invalid data type.
        """
        column_indexes = column_set.select_column_indexes(data_set)
        column_names = list(map(data_set.get_column_name, column_indexes))

        illegal_column_names = [n for n in column_names if
                                data_set.get_element_type(n) != ElementTypeName.STRING]
        if illegal_column_names:
            illegal_column_types = [data_set.get_element_type(n) for n in illegal_column_names]
            ErrorMapping.throw(InvalidColumnTypeError(
                col_name=','.join(illegal_column_names),
                col_type=','.join(illegal_column_types))
            )

    @classmethod
    def _generate_replace_column_name(cls, hashed_column_name, original_column_names):
        """Modify hashed column names by adding hashing feature postfix.

        :param hashed_column_name: str
        :param original_column_names: set, input dataset column names
        :return: str
        For example,
        1. 'text.0' -> 'text_HashingFeature.0'.
        2. If there is an already existed column name 'text_HashingFeature.0' in original_column_names,
        'text.0' -> 'text_HashingFeature2.0'. The rename rule is based on V1.
        """
        # separator '.' is designed by nimbusml NgramHash.
        sep_pos = hashed_column_name.rfind('.')
        name = hashed_column_name[: sep_pos]
        hashed_index = hashed_column_name[sep_pos + 1:]
        hashed_name = f'{name}{cls.HASHING_FEATURE_POSTFIX}.{hashed_index}'
        # Postfix starts from 2 if there is a column name conflict based on V1.
        count = 2
        while (hashed_name in original_column_names):
            hashed_name = f'{name}{cls.HASHING_FEATURE_POSTFIX}{count}.{hashed_index}'
            count += 1
        return hashed_name

    @classmethod
    def _concat_and_rename(cls, all_hashed_features_list, original_column_names):
        """Concat hashed feature list and rename hashed column names.

        :param all_hashed_features_list: input the all hashed feature through a list
        :param original_column_names: set, input dataset column names
        :return: all_hashed_features
        """
        all_hashed_features = pd.concat(all_hashed_features_list, axis=1)
        with TimeProfile("Rename all hashed feature column names."):
            new_dict = {
                key: cls._generate_replace_column_name(key, original_column_names)
                for key in all_hashed_features.columns
            }
        all_hashed_features.rename(columns=new_dict, inplace=True)

        return all_hashed_features

    @classmethod
    def create_feature_hashing_module(cls, dataset: DataTable,
                                      target_column: DataTableColumnSelection,
                                      bits: int = None,
                                      ngrams: int = None,
                                      ):
        # Remove feature hashing code to avoid dependency on NimbusML
        _raise_deprecated_error("Feature Hashing")
