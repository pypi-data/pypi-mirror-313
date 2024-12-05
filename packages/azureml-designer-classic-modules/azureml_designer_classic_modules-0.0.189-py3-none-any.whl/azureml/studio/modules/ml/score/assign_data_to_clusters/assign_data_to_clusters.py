import pandas as pd

import azureml.studio.common.error as error_setting
import azureml.studio.modules.ml.common.ml_utils as ml_utils
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.input_parameter_checker import InputParameterChecker
from azureml.studio.modulehost.attributes import IClusterInputPort, DataTableInputPort, BooleanParameter, ModuleMeta, \
    ReleaseState, DataTableOutputPort
from azureml.studio.modulehost.module_reflector import module_entry, BaseModule
from azureml.studio.modules.ml.initialize_models.cluster.kmeans_cluster.kmeans_cluster import KMeansCluster


class AssignDataToClustersModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name="Assign Data to Clusters",
        description="Assign data to clusters using an existing trained clustering model.",
        category="Model Scoring & Evaluation",
        version="2.0",
        owner="Microsoft Corporation",
        family_id="20A0683A-07F9-4A08-A89B-44B3BBAAE382",
        release_state=ReleaseState.Release,
        is_deterministic=True,
    ))
    def run(
            cluster: IClusterInputPort(
                name="Trained model",
                friendly_name="Trained model",
                description="Trained clustering model",
            ),
            data_table: DataTableInputPort(
                name="Dataset",
                friendly_name="Dataset",
                description="Input data source",
            ),
            append_or_result_only: BooleanParameter(
                name="Check for Append or Uncheck for Result Only",
                friendly_name="Check for append or uncheck for result only",
                description="Whether output dataset must contain input dataset appended by "
                            "assignments column (Checked) or assignments column only (Unchecked)",
                default_value=True
            )
    ) -> (
            DataTableOutputPort(
                name="Results dataset",
                friendly_name="Results dataset",
                description="Input dataset appended by data column of assignments or assignments column only",
            ),
    ):
        input_values = locals()
        output_values = AssignDataToClustersModule._assign_data_to_cluster(**input_values)
        return output_values

    @classmethod
    def _validate_args(cls, cluster, data_table: DataTable):
        if not cluster.is_trained:
            error_setting.ErrorMapping.throw(error_setting.UntrainedModelError())
        InputParameterChecker.verify_data_table(data_table=data_table,
                                                friendly_name=cls._args.data_table.friendly_name)
        required_features = cluster.init_feature_columns_names
        missing_features = [feature for feature in required_features if feature not in data_table.column_names]
        if missing_features:
            error_setting.ErrorMapping.throw(error_setting.MissingFeaturesError(str(missing_features)))

    @classmethod
    def _assign_data_to_cluster(cls, cluster: KMeansCluster, data_table: DataTable, append_or_result_only):
        # ValidateArgs(learner, testData);
        cls._validate_args(cluster, data_table=data_table)

        data_table.data_frame.reset_index(drop=True, inplace=True)

        feature_column_index = [data_table.get_column_index(x) for x in cluster.init_feature_columns_names]
        selected_data = data_table.get_slice_by_column_indexes(feature_column_index)

        valid_row_indexes = ml_utils.collect_notna_numerical_feature_instance_row_indexes(
            data_table=selected_data,
            include_inf=True
        )
        test_data_df = selected_data.data_frame.iloc[valid_row_indexes, :].reset_index(drop=True)
        if test_data_df.empty:
            error_setting.ErrorMapping.throw(
                error_setting.TooFewRowsInDatasetError(arg_name=cls._args.data_table.friendly_name,
                                                       required_rows_count=1,
                                                       actual_rows_count=len(valid_row_indexes),
                                                       row_type='not NA numerical features'))

        assignments, distance_df = cluster.predict(df=test_data_df)
        label_column_name = cluster.label_column_name
        label_column = None

        if label_column_name is not None and label_column_name in data_table.column_names:
            label_column = data_table.get_column(label_column_name)

        new_label_column = cluster.generate_new_label_column(label_column, assignments, valid_row_indexes)

        # rebuild output df
        predict_df = pd.concat([pd.DataFrame(assignments), distance_df], axis=1)
        predict_df.index = valid_row_indexes

        # build score column names dict using predict_df column names
        score_column_names = cluster.generate_score_column_meta(predict_df=predict_df)
        if append_or_result_only:
            result_data = ml_utils.append_predict_result(
                data_table=data_table,
                predict_df=predict_df,
                valid_row_indexes=valid_row_indexes)
        else:
            base_df = pd.DataFrame(index=data_table.data_frame.index)
            result_data = DataTable(pd.concat([base_df, predict_df], axis=1))
        # if new label column is existing, replace the old one.
        if new_label_column is not None:
            result_data = result_data.upsert_column(label_column_name, new_label_column)
        if label_column is not None:
            result_data.meta_data.label_column_name = label_column_name
        result_data.meta_data.score_column_names = score_column_names

        return tuple([result_data])
