import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTENC, SMOTE

import azureml.studio.common.utils.datetimeutils as datetimeutils
from azureml.studio.common.datatable.data_table import DataTable, DataTableColumnSelection
from azureml.studio.common.error import ErrorMapping, NotExpectedLabelColumnError, FailedToCompleteOperationError, \
    InvalidDatasetError, LessThanOrEqualToError, UnexpectedNumberOfColumnsError, TooFewFeatureColumnsInDatasetError
from azureml.studio.core.logger import module_logger, TimeProfile
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.attributes import ModuleMeta, DataTableInputPort, \
    ColumnPickerParameter, SelectedColumnCategory, IntParameter, DataTableOutputPort
from azureml.studio.modulehost.constants import ElementTypeName, UINT32_MAX
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from sklearn.utils.multiclass import type_of_target


class SMOTEModule(BaseModule):
    _TRANSFORM_CONVERTERS = {
        ElementTypeName.DATETIME: datetimeutils.convert_to_ns,
        ElementTypeName.TIMESPAN: datetimeutils.convert_to_ns,
    }

    _RESTORE_CONVERTERS = {
        # category features are converted to UNCATEGORY by SMOTENC, so we define a restore operation manually.
        ElementTypeName.CATEGORY: lambda x: x.astype('category'),
        ElementTypeName.DATETIME: datetimeutils.convert_to_datetime,
        ElementTypeName.TIMESPAN: datetimeutils.convert_to_time_span,
    }

    @staticmethod
    @module_entry(
        ModuleMeta(
            name="SMOTE",
            description="Increases the number of low incidence examples in a dataset.",
            category="Data Transformation",
            version="2.0",
            owner="Microsoft Corporation",
            family_id="9F3FE1C4-520E-49AC-A152-2E104169912A",
            release_state=ReleaseState.Release,
            is_deterministic=True,
            pass_through_in_real_time_inference=True,
        ))
    def run(
            samples: DataTableInputPort(
                name="Samples",
                friendly_name="Samples",
                description="A DataTable of samples",
            ),
            label_column_index_or_name: ColumnPickerParameter(
                name="Label column",
                friendly_name="Label column",
                description="Select the column that contains the label or outcome column",
                column_picker_for="Samples",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            smote_percent: IntParameter(
                name="SMOTE percentage",
                friendly_name="SMOTE percentage",
                description="Amount of oversampling."
                            "If not in integral multiples of 100, "
                            "the minority class will be randomized and downsampled "
                            "from the next integral multiple of 100.",
                default_value=100,
                min_value=0,
            ),
            neighbors: IntParameter(
                name="Number of nearest neighbors",
                friendly_name="Number of nearest neighbors",
                description="The number of nearest neighbors",
                default_value=1,
                min_value=1,
            ),
            seed: IntParameter(
                name="Random seed",
                friendly_name="Random seed",
                min_value=0,
                max_value=UINT32_MAX,
                description="Random number generator seed",
                default_value=0,
            )
    ) -> (
            DataTableOutputPort(
                name="Table",
                friendly_name="Results dataset",
                description="A DataTable containing original samples "
                            "plus an additional synthetic minority class samples, "
                            "where T is the number of minority class samples",
            ),
    ):
        input_values = locals()
        return SMOTEModule._run_impl(**input_values)

    @classmethod
    def _check_label_column(cls, label_column: DataTable):
        """Check the label column in data table

        1.The label column num must be one.
        2.SMOTE only accepts binary labels, not continuous.
        3.The label column must have 2 classes.
        :param label_column: input label data
        :return: None
        """
        actual_label_column_count = label_column.number_of_columns
        if actual_label_column_count != 1:
            ErrorMapping.throw(
                UnexpectedNumberOfColumnsError(
                    expected_column_count=1,
                    actual_column_count=actual_label_column_count))

        if type_of_target(label_column.data_frame) != 'binary':
            ErrorMapping.throw(
                NotExpectedLabelColumnError(
                    dataset_name=cls._args.samples.friendly_name,
                    reason='SMOTE only accepts binary labels.'))

        categories = label_column.data_frame.iloc[:, 0].dropna().unique()
        if len(categories) != 2:
            ErrorMapping.throw(
                NotExpectedLabelColumnError(
                    dataset_name=cls._args.samples.friendly_name,
                    reason=f'SMOTE label column must have 2 classes, got {len(categories)} class(es).'))

    @classmethod
    def _check_no_missing_value(cls, data_set: DataTable):
        if data_set.has_na(include_inf=True):
            ErrorMapping.throw(InvalidDatasetError(
                dataset1=cls._args.samples.friendly_name,
                invalid_data_category='missing or infinity values',
                troubleshoot_hint="Please remove missing and infinity values."))

    @classmethod
    def _transform_columns(cls, dataset: DataTable):
        for column_name in dataset.column_names:
            func = cls._TRANSFORM_CONVERTERS.get(dataset.get_element_type(column_name), None)
            if func:
                dataset.set_column(column_name, func(dataset.get_column(column_name)))
        return dataset

    @classmethod
    def _restore_origin_data_types(cls, result_df, input_data_types):
        for column_name in result_df.columns:
            func = cls._RESTORE_CONVERTERS.get(input_data_types[column_name], None)
            if func:
                result_df[column_name] = func(result_df[column_name])
        return result_df

    @classmethod
    def _get_categorical_column_list(cls, data_set: DataTable, column_to_exclude):
        """Get the categorical feature columns list of the input dataset.

        Due to the known limitation of SMOTE and SMOTENC, all categorical dataset could not be handled.
        :param data_set: input data set
        :param column_to_exclude: selected label column name, which would be excluded from the result.
        :return: a list of indices specifying the categorical features;
        Raise error if all feature columns are categorical.
        """
        column_names = [x for x in data_set.column_names if x != column_to_exclude]
        # refer to V1, bool type is treated the same as string type, in other words,
        # we should treat bool type as categorical type. Besides, if we don't take bool as categorical type, the
        # bool columns would be converted to be float, then generated samples would not keep original bool type.
        categorical_column_list = [i for i, n in enumerate(column_names) if
                                   data_set.get_element_type(n) not in [ElementTypeName.INT, ElementTypeName.FLOAT]]
        if len(column_names) == len(categorical_column_list):
            ErrorMapping.throw(FailedToCompleteOperationError(
                failed_operation="Performing SMOTE on dataset, "
                                 "the input dataset should contain at least one numerical feature column. "))
        return categorical_column_list

    @classmethod
    def _run_impl(cls, samples: DataTable,
                  label_column_index_or_name: DataTableColumnSelection,
                  smote_percent: int = None,
                  neighbors: int = None, seed: int = None):

        # Table cannot be empty
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=samples.number_of_rows,
                                                                    required_row_count=1,
                                                                    arg_name=cls._args.samples.friendly_name)
        # Dataset could not contain any missing value.
        cls._check_no_missing_value(samples)
        # Check the label column
        label_column = label_column_index_or_name.select(samples)
        cls._check_label_column(label_column)
        label_column_index = label_column_index_or_name.select_column_indexes(samples)
        label_column_name = samples.get_column_name(label_column_index[0])

        # Record input data types
        input_data_types = samples.element_types

        # Convert all date time and time span column to ns
        samples = cls._transform_columns(samples)
        # The number of feature columns must be greater than or equal to one
        feature_columns = samples.data_frame.drop(label_column_name, axis=1)
        if feature_columns.shape[1] < 1:
            ErrorMapping.throw(
                TooFewFeatureColumnsInDatasetError(required_columns_count=1, arg_name=cls._args.samples.friendly_name))

        categorical_column_list = cls._get_categorical_column_list(samples, label_column_name)

        # Calculate the number of minority label and the number of majority label
        label_to_num = pd.value_counts(label_column.data_frame[label_column_name])
        small_class_num = min(label_to_num)

        # Neighbors should be smaller than the rows num of majority label
        if neighbors > small_class_num - 1:
            expect = small_class_num - 1
            ErrorMapping.throw(
                LessThanOrEqualToError(arg_name=cls._args.neighbors.friendly_name,
                                       actual_value=neighbors,
                                       upper_boundary=expect))

        # Calculate the ratio of the number of minority label to the number of majority label after smote
        if smote_percent == 0:
            return samples,

        expected_minority_num = int((100 + smote_percent) / 100 * small_class_num)
        # pd.value_counts sort values by frequency, so the last label is minority label
        sampling_strategy = {label_to_num.index[-1]: expected_minority_num}

        module_logger.info("Create a smote generator.")
        if categorical_column_list:
            # If categorical column list is not empty, SMOTENC algo should be used.
            smote_generator = SMOTENC(categorical_features=np.array(categorical_column_list),
                                      sampling_strategy=sampling_strategy, random_state=seed,
                                      k_neighbors=neighbors)
        else:
            # If input data does not contain categorical feature,
            # SMOTE algo should be used due to the limitation of SMOTENC algo.
            # It requires that the input data should contain both numerical and categorical features.
            smote_generator = SMOTE(sampling_strategy=sampling_strategy, random_state=seed,
                                    k_neighbors=neighbors)
        feature_columns_name = feature_columns.columns.values.tolist()
        with TimeProfile("Fit and transform train dataset"):
            new_features_columns, new_label_column = smote_generator.fit_resample(feature_columns, np.array(
                label_column.data_frame[label_column_name]))

        # Concat the feature part and the label part
        new_features_df = pd.DataFrame(new_features_columns, columns=feature_columns_name)
        new_label_df = pd.DataFrame(new_label_column, columns=[label_column_name])
        # In order to improve the user experience, don't change the order of new_label_df and new_features_df
        # Reason: only the visualization results of the first 100 columns can be viewed.
        # If any string or category feature is included in the input data, new_features_columns would be an object
        # np.ndarray, infer_objects would be necessary to retain the input date types.
        result_df = pd.concat([new_label_df, new_features_df], axis=1).infer_objects()
        result_df = cls._restore_origin_data_types(result_df, input_data_types)
        output_data = DataTable(result_df)
        return output_data,
