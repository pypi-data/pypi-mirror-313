import pandas as pd
import numpy as np
from abc import abstractmethod
from sklearn.metrics import mean_absolute_error, r2_score, explained_variance_score, accuracy_score, log_loss, \
    f1_score, roc_auc_score, mean_squared_error


class _Metric:
    def __init__(self, name):
        self._name = name

    def __call__(self, *args, **kwargs):
        return self.calculate(*args, **kwargs)

    @abstractmethod
    def calculate(self, *args, **kwargs):
        pass

    @property
    def name(self):
        return self._name


# metrics for regression task

class _MAE(_Metric):
    def __init__(self):
        super().__init__(name="MAE")

    def calculate(self, y_true, y_pred):
        """Calculate Mean Absolute Error."""
        return mean_absolute_error(y_true, y_pred)


class _RMSE(_Metric):
    def __init__(self):
        super().__init__(name="RMSE")

    def calculate(self, y_true, y_pred):
        """Calculate Root Mean Squared Error."""
        return np.sqrt(mean_squared_error(y_true, y_pred))


class _RSquared(_Metric):
    def __init__(self):
        super().__init__(name="R2")

    def calculate(self, y_true, y_pred):
        """Calculate coefficient of determination, denoted as R^2."""
        return r2_score(y_true, y_pred)


class _ExpVar(_Metric):
    def __init__(self):
        super().__init__(name="Explained Variance")

    def calculate(self, y_true, y_pred):
        """Calculate explained variance."""
        return explained_variance_score(y_true, y_pred)


# metrics for classification task

class _Accuracy(_Metric):
    def __init__(self):
        super().__init__(name="Accuracy")

    def calculate(self, true_label, pred_label, pred_prob):
        """Calculate the Accuracy metric for implicit feedback typed recommender.

        :param true_label: binary labels
        :param pred_label: binary labels
        :param pred_prob: prediction probabilities which are ranging from 0.0 to 1.0
        :return: Accuracy metric value
        """
        return accuracy_score(true_label, pred_label)


class _LogLoss(_Metric):
    def __init__(self):
        super().__init__(name="Log Loss")

    def calculate(self, true_label, pred_label, pred_prob):
        """Calculate the Log Loss metric for implicit feedback typed recommender.

        :param true_label: binary labels
        :param pred_label: binary labels
        :param pred_prob: prediction probabilities which are ranging from 0.0 to 1.0
        :return: Log Loss metric value
        """
        return log_loss(true_label, pred_prob, labels=[0, 1])


class _F1Score(_Metric):
    def __init__(self):
        super().__init__(name="F1")

    def calculate(self, true_label, pred_label, pred_prob):
        """Calculate the F1 score metric for implicit feedback typed recommender.

        :param true_label: binary labels
        :param pred_label: binary labels
        :param pred_prob: prediction probabilities which are ranging from 0.0 to 1.0
        :return: F1 score metric value
        """
        return f1_score(true_label, pred_label)


class _AUC(_Metric):
    def __init__(self):
        super().__init__(name="AUC")

    def calculate(self, true_label, pred_label, pred_prob):
        """Calculate the Area Under Curve metric for implicit feedback typed recommender.

        :param true_label: binary labels
        :param pred_label: binary labels
        :param pred_prob: prediction probabilities which are ranging from 0.0 to 1.0
        :return: AUC metric value
        """
        if true_label.nunique() == 1:
            return 0.0
        return roc_auc_score(true_label, pred_prob)


# metrics for rated item recommendation task

class _RatingRelNDCG(_Metric):
    _IDCG_COL = "IDCG"
    _DCG_COL = "DCG"

    def __init__(self):
        super().__init__(name="NDCG")

    def calculate(self,
                  true_rating_df,
                  pred_rating_df,
                  user_col,
                  true_rating_col,
                  pred_rating_col,
                  rank_col):
        """Calculate NDCG@K metrics, this metric is usually for top-K rated items ranking.

        This implementation of Normalized Discounted Cumulative Gain takes true rating as gain of each rated item.

        :param true_rating_df: true top ratings for each user
        :param pred_rating_df: true ratings for each rated items
        :param user_col: user column name
        :param true_rating_col: true top rating column name
        :param pred_rating_col: true rating column for rated items
        :param rank_col: rank column name for both true_rating_df and pred_rating_df
        :return: NDCG@K metric value
        """
        idcg_df = true_rating_df.copy()
        dcg_df = pred_rating_df.copy()

        idcg_df[self._IDCG_COL] = idcg_df[true_rating_col] / np.log2(idcg_df[rank_col] + 1)
        idcg_df = idcg_df.groupby(user_col, as_index=False, sort=False).agg({self._IDCG_COL: "sum"})

        dcg_df[self._DCG_COL] = dcg_df[pred_rating_col] / np.log2(dcg_df[rank_col] + 1)
        dcg_df = dcg_df.groupby(user_col, as_index=False, sort=False).agg({self._DCG_COL: "sum"})

        ndcg_df = pd.merge(idcg_df, dcg_df, on=user_col)

        n_users = len(ndcg_df)
        if n_users == 0:
            return 0.0

        return (ndcg_df[self._DCG_COL] / ndcg_df[self._IDCG_COL]).sum(skipna=False) / len(ndcg_df)


# metrics for item recommendation task

class _PrecisionAtK(_Metric):
    def __init__(self):
        super().__init__(name="Precision")

    def calculate(self,
                  hit_rank_df,
                  count_df,
                  user_col,
                  hit_col,
                  rank_col,
                  hit_count_col,
                  actual_count_col):
        """Calculate Precision@K metrics, this metric is usually for top-K item recommendation task.

        :param hit_rank_df: pd.DataFrame, record recommended items rank and relevant or not
        :param count_df: pd.DataFrame, record hit item count and actual item count
        :param user_col: user column name
        :param hit_col: hit column name
        :param rank_col: rank column name
        :param hit_count_col: hit item count column name
        :param actual_count_col: actual count column name
        :return: Precision@K metric value
        """
        n_users = len(count_df)
        if n_users == 0:
            return 0.0

        top_k = hit_rank_df[rank_col].max(skipna=False)
        return (count_df[hit_count_col] / top_k).sum(skipna=False) / n_users


class _RecallAtK(_Metric):
    def __init__(self):
        super().__init__(name="Recall")

    def calculate(self,
                  hit_rank_df,
                  count_df,
                  user_col,
                  hit_col,
                  rank_col,
                  hit_count_col,
                  actual_count_col):
        """Calculate Recall@K metrics, this metric is usually for top-K item recommendation task.

        :param hit_rank_df: pd.DataFrame, record recommended items rank and relevant or not
        :param count_df: pd.DataFrame, record hit item count and actual item count
        :param user_col: user column name
        :param hit_col: hit column name
        :param rank_col: rank column name
        :param hit_count_col: hit item count column name
        :param actual_count_col: actual count column name
        :return: Recall@K metric value
        """
        n_users = len(count_df)
        if n_users == 0:
            return 0.0

        return (count_df[hit_count_col] / count_df[actual_count_col]).sum(skipna=False) / n_users


class _NDCGAtK(_Metric):
    _IDCG_COL = "IDCG"
    _DCG_COL = "DCG"
    _NDCG_COL = "NDCG"

    def __init__(self):
        super().__init__(name="NDCG")

    def calculate(self,
                  hit_rank_df,
                  count_df,
                  user_col,
                  hit_col,
                  rank_col,
                  hit_count_col,
                  actual_count_col):
        """Calculate NDCG@K metrics, this metric is usually for top-K item recommendation task.

        This implementation of Normalized Discounted Cumulative Gain takes 1.0 as gain of each relevant item and
        0.0 as gain of each irrelevant item.

        :param hit_rank_df: pd.DataFrame, record recommended items rank and relevant or not
        :param count_df: pd.DataFrame, record hit item count and actual item count
        :param user_col: user column name
        :param hit_col: hit column name
        :param rank_col: rank column name
        :param hit_count_col: hit item count column name
        :param actual_count_col: actual count column name
        :return: NDCG@K metric value
        """
        n_users = len(count_df)
        if n_users == 0:
            return 0.0

        dcg_df = hit_rank_df.copy()
        dcg_df[self._DCG_COL] = dcg_df[hit_col] / np.log2(dcg_df[rank_col] + 1)
        dcg_df = dcg_df.groupby(user_col, as_index=False).agg({self._DCG_COL: "sum"}).reset_index(drop=False)

        top_k = hit_rank_df[rank_col].max()
        ndcg_df = pd.merge(dcg_df, count_df, on=[user_col])
        ndcg_df[self._IDCG_COL] = ndcg_df[actual_count_col].apply(
            lambda x: sum(1.0 / np.log2(range(2, min(top_k, x) + 2))))
        ndcg_df[self._NDCG_COL] = ndcg_df[self._DCG_COL] / ndcg_df[self._IDCG_COL]

        return ndcg_df[self._NDCG_COL].sum(skipna=False) / n_users


class _MAPAtK(_Metric):
    _AVE_PRECISION_COL = "Precision"

    def __init__(self):
        super().__init__(name="MAP")

    def calculate(self,
                  hit_rank_df,
                  count_df,
                  user_col,
                  hit_col,
                  rank_col,
                  hit_count_col,
                  actual_count_col):
        """Calculate MAP@K metrics, this metric is usually for top-K item recommendation task.

        This implementation of mean average precision is referenced from Spark MLlib evaluation metrics.
        https://spark.apache.org/docs/2.3.0/mllib-evaluation-metrics.html#ranking-systems
        Note that:
        1.The evaluation function is named as 'MAP@K' because the evaluation class takes top k items for
        the prediction items.
        2.The MAP is meant to calculate Avg. Precision for the relevant items, so it is normalized by the number of
        relevant items in the ground truth data, instead of K.

        :param hit_rank_df: pd.DataFrame, record recommended items rank and relevant or not
        :param count_df: pd.DataFrame, record hit item count and actual item count
        :param user_col: user column name
        :param hit_col: hit column name
        :param rank_col: rank column name
        :param hit_count_col: hit item count column name
        :param actual_count_col: actual count column name
        :return: MAP@K metric value
        """
        n_users = len(count_df)
        if n_users == 0:
            return 0.0

        ap_df = hit_rank_df.copy()
        ap_df = ap_df[ap_df[hit_col]]
        ap_df[self._AVE_PRECISION_COL] = (ap_df.groupby(user_col, as_index=False).cumcount() + 1) / ap_df[rank_col]
        ap_df = ap_df.groupby(user_col, as_index=False).agg({self._AVE_PRECISION_COL: "sum"})

        ap_df = pd.merge(ap_df, count_df, on=[user_col])
        ap_df[self._AVE_PRECISION_COL] = ap_df[self._AVE_PRECISION_COL] / ap_df[actual_count_col]

        return ap_df[self._AVE_PRECISION_COL].sum(skipna=False) / n_users


mae = _MAE()
rmse = _RMSE()
rsquared = _RSquared()
exp_var = _ExpVar()
accuracy = _Accuracy()
logloss = _LogLoss()
f1 = _F1Score()
auc = _AUC()
rating_rel_ndcg = _RatingRelNDCG()
precision_at_k = _PrecisionAtK()
recall_at_k = _RecallAtK()
ndcg_at_k = _NDCGAtK()
map_at_k = _MAPAtK()
