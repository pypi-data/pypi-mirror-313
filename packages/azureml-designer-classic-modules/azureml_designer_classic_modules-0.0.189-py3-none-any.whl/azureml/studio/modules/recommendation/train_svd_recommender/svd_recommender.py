import surprise
import pandas as pd
import numpy as np
from azureml.studio.core.logger import time_profile
from azureml.studio.modules.recommendation.common.recommender_utils import get_user_column_name, get_item_column_name, \
    get_rating_column_name
from azureml.studio.modules.recommendation.common.base_recommender import BaseRecommender
from azureml.studio.modules.ml.model_deployment.model_deployment_handler import SVDRecommendationDeploymentHandler


class SVDRecommender(BaseRecommender):
    def __init__(self, num_factors, num_iterations, learning_rate, random_state=0):
        self.model = surprise.SVD(n_factors=num_factors,
                                  n_epochs=num_iterations,
                                  lr_all=learning_rate,
                                  random_state=random_state,
                                  verbose=False)
        self._deployment_handler = None

    @time_profile
    def train(self, training_data: pd.DataFrame):
        """Train SVD Recommendation model with given dataset."""
        training_dataset = self._build_dataset(training_data)
        # for now, we use bias to compute ratings for cold-start users and items,
        # for details, refer to Surprise libaray source codes.
        self.model.fit(trainset=training_dataset)

    @property
    def deployment_handler(self):
        return self._deployment_handler

    @deployment_handler.setter
    def deployment_handler(self, value):
        if not isinstance(value, SVDRecommendationDeploymentHandler):
            raise TypeError(f'deployment_handler must be an instance of class '
                            f'{SVDRecommendationDeploymentHandler.__name__}.')
        self._deployment_handler = value

    def predict(self, test_data_df: pd.DataFrame):
        """Predict rating for each user-item pair in the test data."""
        user_ids = test_data_df[get_user_column_name(test_data_df)]
        item_ids = test_data_df[get_item_column_name(test_data_df)]
        predictions = [self.model.predict(user_id, item_id).est for user_id, item_id in zip(user_ids, item_ids)]
        return user_ids, item_ids, predictions

    def recommend(self, users, max_recommended_item_count, included_items=None, excluded_items=None):
        """Recommend a list of items for each user.

        This method generates a certain number of recommended items for each user. The candidate items are
        determined by included_items and excluded_items parameters. These parameters are not expected to be
        non-None at the same time. And if they are both None, we consider all items as candidate items for each user.

        :param users: a series of users.
        :param max_recommended_item_count: customize the number of recommended items for each user.
        :param included_items: defaults to None. If not None, each element in included_items is expected to contain
                candidate items for the corresponding user.
        :param excluded_items: defaults to None. If not None, each element in excluded_items is expected to contain
                items not to be considered for the corresponding user.
        """
        recommended_items = []
        recommended_item_ratings = []

        if included_items is not None:
            total_items = included_items
        elif excluded_items is not None:
            full_items = set(self.model.trainset._raw2inner_id_items.keys())
            total_items = [list(full_items - set(items)) for items in excluded_items]
        else:
            total_items = [list(self.model.trainset._raw2inner_id_items.keys())] * len(users)
        for target_user, target_items in zip(users, total_items):
            topk_items, topk_ratings = self._recommended_topk_items(target_user, target_items,
                                                                    max_recommended_item_count)
            recommended_items.append(topk_items)
            recommended_item_ratings.append(topk_ratings)

        return users, recommended_items, recommended_item_ratings

    def _recommended_topk_items(self, target_user, target_items, max_recommended_item_count):
        ratings_sr = pd.Series([self.model.predict(target_user, item).est for item in target_items])
        topk_ratings_sr = ratings_sr.nlargest(max_recommended_item_count)
        topk_items = [target_items[idx] for idx in topk_ratings_sr.index]
        topk_ratings = topk_ratings_sr.tolist()
        # use np.nan to fill top-k item list with less than k items
        topk_items += [np.nan] * (max_recommended_item_count - len(topk_items))
        # use 0 rating to fill top-k rating list with less than k ratings
        topk_ratings += [0] * (max_recommended_item_count - len(topk_ratings))
        return topk_items, topk_ratings

    @staticmethod
    def _build_dataset(df: pd.DataFrame):
        rating_column_name = get_rating_column_name(df)
        min_rating = df[rating_column_name].min()
        max_rating = df[rating_column_name].max()
        rating_scale = [min_rating, max_rating]
        training_dataset = surprise.Dataset.load_from_df(df, reader=surprise.reader.Reader(
            rating_scale=rating_scale)).build_full_trainset()
        return training_dataset
