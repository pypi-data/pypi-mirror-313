import pandas as pd

from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.datatable.data_table import DataTableColumnSelection
from azureml.studio.common.error import UnsupportedParameterTypeError, ErrorMapping, \
    GreaterThanOrEqualToError
from azureml.studio.common.types import AutoEnum
from azureml.studio.core.logger import module_logger as logger
from azureml.studio.modulehost.attributes import ItemInfo, ModuleMeta, DataTableInputPort, IntParameter, \
    ModeParameter, BooleanParameter, ColumnPickerParameter, DataTableOutputPort, SelectedColumnCategory
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.feature_selection.filter_based_feature_selection.feature_scoring_method import \
    PearsonCorrelation, ChiSquared


class FilterBasedFeatureSelectionScoringMethod(AutoEnum):
    PearsonCorrelation: ItemInfo(name="PearsonCorrelation", friendly_name="Pearson Correlation") = ()
    ChiSquared: ItemInfo(name="ChiSquared", friendly_name="Chi Squared") = ()


class FilterBasedFeatureSelectionModule(BaseModule):

    @staticmethod
    @module_entry(ModuleMeta(
        name="Filter Based Feature Selection",
        description="Identifies the features in a dataset with the greatest predictive power.",
        category="Feature Selection",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="818b356b-045c-412b-aa12-94a1d2dad90f",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            dataset: DataTableInputPort(
                name="Dataset",
                friendly_name="Input dataset",
                description="Input dataset",
            ),
            feature_only: BooleanParameter(
                name="Operate on feature columns only",
                friendly_name="Operate on feature columns only",
                description="Indicate whether to use only feature columns in the scoring process",
                is_optional=True,
                default_value=True,
            ),
            column_select: ColumnPickerParameter(
                name="Target column",
                friendly_name="Target column",
                description="Specify the target column",
                column_picker_for="Dataset",
                single_column_selection=True,
                column_selection_categories=(SelectedColumnCategory.All,),
            ),
            req_feature_count: IntParameter(
                name="Number of desired features",
                friendly_name="Number of desired features",
                description="Specify the number of features to output in results",
                default_value=1,
            ),
            method: ModeParameter(
                FilterBasedFeatureSelectionScoringMethod,
                name="Feature scoring method",
                friendly_name="Feature scoring method",
                description="Choose the method to use for scoring",
                default_value=FilterBasedFeatureSelectionScoringMethod.PearsonCorrelation,
            )
    ) -> (
            DataTableOutputPort(
                name="Filtered dataset",
                friendly_name="Filtered dataset",
                description="Filtered dataset",
            ),
            DataTableOutputPort(
                name="Features",
                friendly_name="Features",
                description="Names of output columns and feature selection scores",
            ),
    ):
        input_values = locals()
        output_values = FilterBasedFeatureSelectionModule.run_impl(**input_values)
        return output_values

    @classmethod
    def run_impl(
            cls,
            dataset: DataTable,
            feature_only: bool,
            column_select: DataTableColumnSelection,
            req_feature_count: int,
            method: FilterBasedFeatureSelectionScoringMethod
    ):
        ErrorMapping.verify_not_null_or_empty(x=dataset, name=cls._args.dataset.friendly_name)
        ErrorMapping.verify_not_null_or_empty(x=column_select, name=cls._args.column_select.friendly_name)
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=dataset.number_of_columns, required_column_count=1,
            arg_name=cls._args.dataset.friendly_name)
        # Get the target column index, only single column is allowed
        target_col_index_list = column_select.select_column_indexes(dataset)
        ErrorMapping.verify_number_of_columns_equal_to(
            curr_column_count=len(target_col_index_list), required_column_count=1,
            arg_name=cls._args.dataset.friendly_name)
        target_col_index, = target_col_index_list
        # Exception occurs if parameter is less than or equal to specific value.
        if req_feature_count < 1:
            ErrorMapping.throw(GreaterThanOrEqualToError(arg_name=cls._args.req_feature_count.friendly_name,
                                                         lower_boundary=1,
                                                         value=req_feature_count))

        # Construct scoring methods
        target_col_series = dataset.get_column(target_col_index)
        target_col_type = dataset.get_column_type(target_col_index)
        logger.info(f'Scoring method: {method.name}')
        if method is FilterBasedFeatureSelectionScoringMethod.PearsonCorrelation:
            scoring_method = PearsonCorrelation(target_col_series, target_col_type)
        elif method is FilterBasedFeatureSelectionScoringMethod.ChiSquared:
            scoring_method = ChiSquared(target_col_series, target_col_type,
                                        target_col_name=dataset.get_column_name(target_col_index),
                                        dataset_name=dataset.name)
        else:
            # Will never throw due to UI constraint
            ErrorMapping.throw(UnsupportedParameterTypeError(
                parameter_name=cls._args.method.friendly_name,
                reason="The scoring method isn't supported"
            ))

        # Get scoring column indices
        scoring_col_indices = cls._get_scoring_column_indices(dataset, target_col_index_list, feature_only)
        # Get feature rank list
        ranked_fea_df = cls._rank_features(scoring_method, dataset, scoring_col_indices)
        # Output features
        target_col_name = dataset.get_column_name(target_col_index)
        features = cls._output_features(ranked_fea_df, target_col_name)
        # Output filtered dataset
        n_req_features = min(req_feature_count, len(scoring_col_indices))
        filtered_indices = target_col_index_list + [dataset.get_column_index(ranked_fea_df['fea_name'][i])
                                                    for i in range(n_req_features)]
        filtered_dataset = dataset.get_slice_by_column_indexes(filtered_indices)
        return filtered_dataset, features

    @classmethod
    def _get_scoring_column_indices(cls, dataset, target_col_index_list, feature_only):
        num_cols = dataset.number_of_columns
        scoring_col_indices = set(range(num_cols))
        # We will score all the columns in input dataset except
        # the target column, label columns, score columns
        label_col_name = dataset.meta_data.label_column_name
        label_col_index = {dataset.get_column_index(label_col_name)} if label_col_name else set()
        score_col_names = dataset.meta_data.score_column_names.values()
        score_col_indices = {dataset.get_column_index(name) for name in score_col_names}
        exclude_col_indices = set(target_col_index_list) | label_col_index | score_col_indices
        scoring_col_indices = scoring_col_indices - exclude_col_indices
        if feature_only:
            # Exclude columns with attribute 'IsFeature' equal to False
            feature_col_indices = {cur_col_index for cur_col_index in range(num_cols)
                                   if dataset.meta_data.column_attributes[cur_col_index].is_feature}
            scoring_col_indices = scoring_col_indices.intersection(feature_col_indices)
        return scoring_col_indices

    @classmethod
    def _rank_features(cls, scoring_method, dataset, scoring_col_indices):
        fea_score_list = []
        for index in scoring_col_indices:
            scoring_col_series = dataset.data_frame.iloc[:, index]
            score = scoring_method.score(scoring_col_series, dataset.get_column_type(index),
                                         scoring_col_name=dataset.get_column_name(index))
            fea_score_list.append([scoring_col_series.name, score])
        fea_df = pd.DataFrame(fea_score_list, columns=['fea_name', 'fea_score'])
        ranked_fea_df = fea_df.sort_values(by='fea_score', ascending=False).reset_index()
        return ranked_fea_df

    @classmethod
    def _output_features(cls, ranked_fea_df, target_col_name):
        # Add target column itself as first column to output features
        # 1 is self coefficient for target column
        fea_scores = [[1] + ranked_fea_df['fea_score'].tolist()]
        fea_names = [target_col_name] + ranked_fea_df['fea_name'].tolist()
        features_df = pd.DataFrame(fea_scores, columns=fea_names)
        return DataTable(features_df)
