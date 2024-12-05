import math
import pandas as pd
from azureml.studio.modulehost.module_reflector import BaseModule, module_entry
from azureml.studio.modulehost.attributes import ModuleMeta, DataTableOutputPort, IRecommenderInputPort, \
    DataTableInputPort, ItemInfo, ModeParameter, IntParameter, BooleanParameter
from azureml.studio.internal.attributes.release_state import ReleaseState
from azureml.studio.common.types import AutoEnum
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import ErrorMapping, InvalidLearnerError
from azureml.studio.modules.recommendation.train_svd_recommender.svd_recommender import SVDRecommender
from azureml.studio.modules.recommendation.common.recommender_utils import get_user_column_name, get_item_column_name, \
    preprocess_tuples, preprocess_id_columns
from azureml.studio.modules.recommendation.common.score_column_names import build_ranking_column_names, PortScheme, \
    build_rated_ranking_column_names, build_regression_column_names, build_rated_ranking_column_name_keys, \
    build_ranking_column_name_keys
from azureml.studio.core.logger import module_logger, TimeProfile


class RecommenderPredictionKind(AutoEnum):
    RatingPrediction: ItemInfo(name="Rating Prediction", friendly_name="Rating prediction") = ()
    ItemRecommendation: ItemInfo(name="Item Recommendation", friendly_name="Item recommendation") = ()


class RecommendedItemSelection(AutoEnum):
    FromAllItems: ItemInfo(name="From All Items", friendly_name="From all items") = ()
    FromRatedItems: ItemInfo(name="From Rated Items (for model evaluation)",
                             friendly_name="From rated items (for model evaluation)") = ()
    FromUnratedItems: ItemInfo(name="From Unrated Items (to suggest new items to users)",
                               friendly_name="From unrated items (to suggest new items to users)") = ()


class ScoreSVDRecommenderModule(BaseModule):
    @staticmethod
    @module_entry(ModuleMeta(
        name="Score SVD Recommender",
        description="Score a dataset using the SVD recommendation.",
        category="Recommendation",
        version="1.0",
        owner="Microsoft Corporation",
        family_id="{D8552796-32BC-4110-8E6D-6738D93420D2}",
        release_state=ReleaseState.Release,
        is_deterministic=True
    ))
    def run(
            learner: IRecommenderInputPort(
                name="Trained SVD recommendation",
                friendly_name="Trained SVD recommendation",
                description="Trained SVD recommendation",
            ),
            test_data: DataTableInputPort(
                name="Dataset to score",
                friendly_name="Dataset to score",
                description="Dataset to score",
            ),
            training_data: DataTableInputPort(
                name="Training data",
                friendly_name="Training data",
                description="Dataset containing the training data. "
                            "(Used to filter out already rated items from prediction)",
                is_optional=True,
            ),
            prediction_kind: ModeParameter(
                RecommenderPredictionKind,
                name="Recommender prediction kind",
                friendly_name="Recommender prediction kind",
                description="Specify the type of prediction the recommendation should output",
                default_value=RecommenderPredictionKind.ItemRecommendation,
            ),
            recommended_item_selection: ModeParameter(
                RecommendedItemSelection,
                name="Recommended item selection",
                friendly_name="Recommended item selection",
                description="Select the set of items to make recommendations from",
                default_value=RecommendedItemSelection.FromRatedItems,
                parent_parameter="Recommender prediction kind",
                parent_parameter_val=(RecommenderPredictionKind.ItemRecommendation,),
            ),
            max_recommended_item_count: IntParameter(
                name="Maximum number of items to recommend to a user",
                friendly_name="Maximum number of items to recommend to a user",
                description="Specify the maximum number of items to recommend to a user",
                default_value=5,
                min_value=1,
                parent_parameter="Recommender prediction kind",
                parent_parameter_val=(RecommenderPredictionKind.ItemRecommendation,),
            ),
            min_recommendation_pool_size: IntParameter(
                name="Minimum size of the recommendation pool for a single user",
                friendly_name="Minimum size of the recommendation pool for a single user",
                description="Specify the minimum size of the recommendation pool for each user",
                default_value=2,
                min_value=1,
                parent_parameter="Recommended item selection",
                parent_parameter_val=(RecommendedItemSelection.FromRatedItems,),
            ),
            return_ratings: BooleanParameter(
                name="Whether to return the predicted ratings of the items along with the labels",
                friendly_name="Whether to return the predicted ratings of the items along with the labels",
                description="Specify whether to return the predicted ratings of the items along with the labels",
                default_value=False,
                parent_parameter="Recommender prediction kind",
                parent_parameter_val=(RecommenderPredictionKind.ItemRecommendation,),
            ),
    ) -> (
            DataTableOutputPort(
                name="Scored dataset",
                friendly_name="Scored dataset",
                description="Scored dataset",
            ),
    ):
        input_values = locals()
        output_values = ScoreSVDRecommenderModule.score_svd_recommender(**input_values)
        return output_values

    @classmethod
    def score_svd_recommender(cls,
                              learner,
                              test_data,
                              prediction_kind,
                              recommended_item_selection,
                              max_recommended_item_count,
                              min_recommendation_pool_size,
                              return_ratings,
                              training_data=None):
        cls._validate_common_parameters(learner, test_data)
        if prediction_kind == RecommenderPredictionKind.RatingPrediction:
            return cls._predict_rating_internal(learner, test_data)
        else:
            if recommended_item_selection == RecommendedItemSelection.FromRatedItems:
                return cls._recommend_rated_items_internal(learner, test_data, max_recommended_item_count,
                                                           min_recommendation_pool_size, return_ratings)
            elif recommended_item_selection == RecommendedItemSelection.FromAllItems:
                return cls._recommend_all_items_internal(learner, test_data, max_recommended_item_count, return_ratings)
            elif recommended_item_selection == RecommendedItemSelection.FromUnratedItems:
                return cls._recommend_unrated_items_internal(learner, test_data, training_data,
                                                             max_recommended_item_count,
                                                             return_ratings)

    @classmethod
    def _validate_common_parameters(cls, learner: SVDRecommender, test_data: DataTable):
        if not isinstance(learner, SVDRecommender):
            ErrorMapping.throw(InvalidLearnerError(arg_name=cls._args.learner.friendly_name))
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=test_data.number_of_rows,
                                                                    required_row_count=1,
                                                                    arg_name=test_data.name)
        # test dataset is not expected to contain more than 3 columns
        test_data_column_number = test_data.number_of_columns
        ErrorMapping.verify_number_of_columns_less_than_or_equal_to(curr_column_count=test_data_column_number,
                                                                    required_column_count=3,
                                                                    arg_name=test_data.name)

    @classmethod
    def _predict_rating_internal(cls, learner: SVDRecommender, test_data: DataTable):
        # For rating prediction, test dataset is expected to have at least 2 columns,
        # corresponding to (user,item) pair
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=test_data.number_of_columns, required_column_count=2,
            arg_name=test_data.name)
        module_logger.info(f"Test data contains {test_data.number_of_rows} samples.")
        test_df = preprocess_tuples(test_data.data_frame)
        module_logger.info(f"After preprocess, test data contains {test_df.shape[0]} valid samples.")
        with TimeProfile("Predicting ratings for user-item pairs"):
            users, items, ratings = learner.predict(test_df)
        result_df = pd.DataFrame(dict(zip(build_regression_column_names(port_scheme=PortScheme.TwoPort),
                                          [users, items, ratings])))
        result_dt = DataTable(result_df)
        # for the columns in dataset are fixed,
        # it is not necessary to set label column name and scored column name
        return result_dt,

    @classmethod
    def _recommend_rated_items_internal(cls, learner: SVDRecommender, test_data: DataTable, max_recommended_item_count,
                                        min_recommendation_pool_size, return_ratings):
        # For recommend items from rated items task, test dataset is expected to have at least 2 columns,
        # corresponding to (user,item) pair.
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=test_data.number_of_columns, required_column_count=2,
            arg_name=test_data.name)
        test_data_df = test_data.data_frame
        user_column = get_user_column_name(test_data_df)
        item_column = get_item_column_name(test_data_df)
        module_logger.info(f"Test data contains {test_data.number_of_rows} samples.")
        test_data_df = preprocess_tuples(test_data_df)
        module_logger.info(f"After preprocess, test data contains {test_data_df.shape[0]} valid samples.")
        user_group_items = test_data_df.groupby(user_column)[item_column]
        rated_items = user_group_items.apply(list)[user_group_items.size() >= min_recommendation_pool_size]
        module_logger.info(f"Get {len(rated_items)} valid users, whose rated items number is equal or "
                           f"greater than {min_recommendation_pool_size}")
        users = list(rated_items.index)
        rated_items = rated_items.values
        with TimeProfile("Generating recommended items"):
            users, recommended_items, recommended_item_ratings = (
                learner.recommend(users=users,
                                  max_recommended_item_count=max_recommended_item_count,
                                  included_items=rated_items)
            )
        score_column_keys_build_method = build_rated_ranking_column_name_keys
        return cls._format_recommend_result(users, recommended_items, recommended_item_ratings,
                                            max_recommended_item_count, return_ratings,
                                            score_column_names_build_method=build_rated_ranking_column_names,
                                            score_column_keys_build_method=score_column_keys_build_method)

    @classmethod
    def _recommend_all_items_internal(cls, learner: SVDRecommender, test_data: DataTable, max_recommended_item_count,
                                      return_ratings):
        # For recommend items from all items task, test dataset is expected to have at least one user column
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=test_data.number_of_columns, required_column_count=1,
            arg_name=test_data.name)
        test_data_df = test_data.data_frame
        user_column = get_user_column_name(test_data_df)
        module_logger.info(f"Test data contains {test_data.number_of_rows} samples.")
        test_data_df = preprocess_id_columns(test_data_df, column_subset=[user_column])
        users = test_data_df[user_column].unique()
        module_logger.info(f"After preprocess, test data contains {users.shape[0]} valid samples.")
        with TimeProfile("Generating recommended items"):
            users, recommended_items, recommended_item_ratings = (
                learner.recommend(users=users,
                                  max_recommended_item_count=max_recommended_item_count)
            )
        score_column_keys_build_method = build_ranking_column_name_keys
        return cls._format_recommend_result(users, recommended_items, recommended_item_ratings,
                                            max_recommended_item_count, return_ratings,
                                            score_column_names_build_method=build_ranking_column_names,
                                            score_column_keys_build_method=score_column_keys_build_method)

    @classmethod
    def _validate_unrated_items_parameters(cls, test_data: DataTable, training_data: DataTable):
        # For recommend items from unrated items task, test dataset is expected to have at least one user column,
        # and training dataset is expected to have at least 2 columns, corresponding to (user,item) pair.
        ErrorMapping.verify_not_null_or_empty(training_data, name=cls._args.training_data.friendly_name)
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=training_data.number_of_rows,
                                                                    required_row_count=1,
                                                                    arg_name=training_data.name)
        training_data_column_number = training_data.number_of_columns
        ErrorMapping.verify_number_of_columns_less_than_or_equal_to(
            curr_column_count=training_data_column_number, required_column_count=3,
            arg_name=training_data.name)
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=training_data_column_number, required_column_count=2,
            arg_name=training_data.name)
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(
            curr_column_count=test_data.number_of_columns, required_column_count=1,
            arg_name=test_data.name)

    @classmethod
    def _recommend_unrated_items_internal(cls, learner: SVDRecommender, test_data: DataTable, training_data: DataTable,
                                          max_recommended_item_count, return_ratings):
        cls._validate_unrated_items_parameters(test_data, training_data)
        test_data_df = test_data.data_frame
        test_user_column = get_user_column_name(test_data_df)
        module_logger.info(f"Test data contains {test_data.number_of_rows} samples.")
        test_data_df = preprocess_id_columns(test_data_df, column_subset=[test_user_column])
        test_users = test_data_df[test_user_column].unique()
        module_logger.info(f"After preprocess, test data contains {test_users.shape[0]} valid samples.")

        training_data_df = training_data.data_frame
        training_user_column = get_user_column_name(training_data_df)
        training_item_column = get_item_column_name(training_data_df)
        training_data_df = preprocess_tuples(training_data_df)

        rated_items = training_data_df.groupby(training_user_column)[training_item_column].apply(list).reindex(
            test_users)
        rated_items = rated_items.apply(lambda items: [] if type(items) != list and math.isnan(items) else items)
        with TimeProfile("Generating recommended items"):
            users, recommended_items, recommended_item_ratings = (
                learner.recommend(users=test_users,
                                  max_recommended_item_count=max_recommended_item_count,
                                  excluded_items=rated_items)
            )
        score_column_keys_build_method = build_ranking_column_name_keys
        return cls._format_recommend_result(users, recommended_items, recommended_item_ratings,
                                            max_recommended_item_count, return_ratings,
                                            score_column_names_build_method=build_ranking_column_names,
                                            score_column_keys_build_method=score_column_keys_build_method)

    @staticmethod
    def _format_recommend_result(users, recommended_items, recommended_item_ratings, max_recommended_item_count,
                                 return_ratings, score_column_names_build_method, score_column_keys_build_method):
        """Format item recommendation result. This format for 'from rated items' and 'from all/undated items'
        is different, that item columns names of 'from rated items' is 'Rated Item k', and item column names of
        'from all/unrated items' is 'Recommended Item k'.

        Format of recommendation results based on V1. According to the value of return_ratings, the results contains
        each item ratings or not. For example, if return_ratings is True,
            User    Recommended/Rated Item 1        Rating 1    Recommended/Rated Item 2            Rating 2
        0   25546   Forrest Gump (1994)             9.03        Schindlers List (1993)              9.21
        1   338     Schindlers List (1993)          9.14        The Shawshank Redemption (1994)     9.23
        2   5118    The Green Mile (1999)           8.95        The Shawshank Redemption (1994)     8.97
        3   931     Schindlers List (1993)          9.91        Saving Private Ryan (1998)          9.98
        4   9749    The Godfather (1972)            9.13        The Shawshank Redemption (1994)     9.31
        5   5050    The Godfather Part II (1974)    8.70        The Godfather (1972)                8.73
        if return_rating is False,
            User    Recommended/Rated Item 1      Recommended/Rated Item              Recommended/Rated Item 3
        0   25546   Forrest Gump (1994)           The Godfather (1972)                The Dark Knight (2008)
        1   338     Schindlers List (1993)        The Shawshank Redemption (1994)     The Godfather Part II (1974)
        2   21640   The Dark Knight (2008)        Schindlers List (1993)              The Shawshank Redemption (1994)
        3   14829   Il buono il brutto            The Godfather (1972)                Schindlers List (1993)
        4   5118    Pulp Fiction (1994)           The Green Mile (1999)               The Shawshank Redemption (1994)
        5   26515   Gravity (2013)                Inception (2010)                    Il buono il brutto
        :param users: list
        :param recommended_items: list
        :param recommended_item_ratings: list
        :param max_recommended_item_count: int
        :param return_ratings: bool
        :param score_column_names_build_method: a method to return column names without rating column
        :return: DataFrame
        """
        score_column_names = score_column_names_build_method(port_scheme=PortScheme.TwoPort,
                                                             top_k=max_recommended_item_count)
        users_df = pd.DataFrame({score_column_names[0]: users})
        recommended_items_df = pd.DataFrame(recommended_items, columns=score_column_names[1:])

        if return_ratings:
            # if return ratings, build score_column_names attributes in the DataFrameSchema to filter predicted rating
            # columns, or the evaluate recommender module would raise InvalidDataset error.
            score_column_keys = score_column_keys_build_method(port_scheme=PortScheme.TwoPort,
                                                               top_k=max_recommended_item_count)
            score_column_names_dict = dict(zip(score_column_keys, score_column_names))
            score_column_names = ScoreSVDRecommenderModule._insert_pred_rating_column_names(score_column_names)
            recommended_item_ratings_df = pd.DataFrame(recommended_item_ratings, columns=score_column_names[2::2])
            res_df = pd.concat([users_df, recommended_items_df, recommended_item_ratings_df], axis=1)
            res_df = res_df[score_column_names]
            result_dt = DataTable(res_df)
            result_dt.meta_data.score_column_names = score_column_names_dict
        else:
            res_df = pd.concat([users_df, recommended_items_df], axis=1)
            res_df = res_df[score_column_names]
            result_dt = DataTable(res_df)

        return result_dt,

    @staticmethod
    def _insert_pred_rating_column_names(score_column_names):
        PredRatingColumn = "Predicted Rating"
        top_k = len(score_column_names) - 1
        new_score_column_names = score_column_names[:1]
        for i in range(1, top_k + 1):
            new_score_column_names = new_score_column_names + [score_column_names[i], f"{PredRatingColumn} {i}"]
        return new_score_column_names
