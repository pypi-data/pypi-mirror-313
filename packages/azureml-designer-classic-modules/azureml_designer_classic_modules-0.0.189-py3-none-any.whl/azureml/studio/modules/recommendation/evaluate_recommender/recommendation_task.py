from abc import abstractmethod
from azureml.studio.core.logger import module_logger
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.common.error import ErrorMapping, NotLabeledDatasetError
from azureml.studio.modules.recommendation.common.score_column_names import \
    build_regression_column_names, build_rated_ranking_column_names, build_ranking_column_names, \
    build_classification_column_names, build_regression_column_name_keys, build_classification_column_name_keys, \
    build_rated_ranking_column_name_keys, build_ranking_column_name_keys, PortScheme, \
    build_backward_compatibility_regression_column_names, build_backward_compatible_rated_ranking_column_names
from azureml.studio.modules.recommendation.common.score_column_names import \
    RECOMMENDATION_REGRESSION_SCORED_RATING_TYPE, RECOMMENDATION_USER_COLUMN_TYPE, RECOMMENDATION_ITEM_COLUMN_TYPE, \
    RECOMMENDATION_CLASSIFICATION_SCORED_LABEL_TYPE, RECOMMENDATION_CLASSIFICATION_SCORED_PROB_TYPE, \
    RECOMMENDATION_RECOMMENDED_ACTUAL_COUNT_TYPE
from azureml.studio.modules.recommendation.evaluate_recommender.regression_recommendation_evaluator import \
    RegressionRecommendationEvaluator
from azureml.studio.modules.recommendation.evaluate_recommender.classification_recommendation_evaluator import \
    ClassificationRecommendationEvaluator
from azureml.studio.modules.recommendation.evaluate_recommender.ranking_recommendation_evaluator import \
    RankingRatedRecommendationEvaluator
from azureml.studio.modules.recommendation.evaluate_recommender.ranking_recommendation_evaluator import \
    RankingRecommendationEvaluator


class RecommendationTask:
    def __init__(self, port_scheme: PortScheme, evaluator):
        self.port_scheme = port_scheme
        self.evaluator = evaluator

    def evaluate(self, scored_data: DataTable, test_data: DataTable):
        scored_data = self._prepare_scored_data(scored_data)
        return self.evaluator(self).evaluate(scored_data=scored_data, test_data=test_data)

    @abstractmethod
    def _prepare_scored_data(self, scored_data: DataTable):
        pass


class RegressionRecommendationTask(RecommendationTask):
    def __init__(self, port_scheme: PortScheme):
        module_logger.info(f"Get recommendation regression task, port scheme: {port_scheme}")
        super().__init__(port_scheme, RegressionRecommendationEvaluator)
        self.user_column = None
        self.item_column = None
        self.scored_rating_column = None
        self.true_rating_column = None

    def _prepare_scored_data(self, scored_data: DataTable):
        """This function prepare scored data. Including, extract data and reorder columns as expected order."""
        if self.port_scheme == PortScheme.OnePort:
            column_names = [self.true_rating_column, self.scored_rating_column]
        else:
            column_names = [self.user_column, self.item_column, self.scored_rating_column]
        scored_data_df = scored_data.data_frame[column_names]
        new_scored_data = DataTable(scored_data_df)
        new_scored_data.name = scored_data.name

        return new_scored_data


class ClassificationRecommendationTask(RecommendationTask):
    def __init__(self, port_scheme: PortScheme):
        module_logger.info(f"Get recommendation classification task, port scheme: {port_scheme}")
        super().__init__(port_scheme, evaluator=ClassificationRecommendationEvaluator)
        self.user_column = None
        self.item_column = None
        self.scored_label_column = None
        self.scored_prob_column = None
        self.true_label_column = None

    def _prepare_scored_data(self, scored_data: DataTable):
        """This function prepare scored data. Including, extract data and reorder columns as expected order."""
        if self.port_scheme == PortScheme.OnePort:
            column_names = [self.true_label_column, self.scored_label_column, self.scored_prob_column]
        else:
            column_names = [self.user_column, self.item_column, self.scored_label_column, self.scored_prob_column]
        scored_data_df = scored_data.data_frame[column_names]
        new_scored_data = DataTable(scored_data_df)
        new_scored_data.name = scored_data.name

        return new_scored_data


class RankingRatedRecommendationTask(RecommendationTask):
    def __init__(self, port_scheme: PortScheme, top_k: int):
        module_logger.info(f"Get recommend items from rated items task, port scheme: {port_scheme}")
        super().__init__(port_scheme, evaluator=RankingRatedRecommendationEvaluator)
        self.top_k = top_k
        self.user_column = None
        self.rated_item_columns = None
        self.true_rating_columns = None
        self.true_top_rating_columns = None

    def _prepare_scored_data(self, scored_data: DataTable):
        """This function prepare scored data. Including, extract data and reorder columns as expected order."""
        if self.port_scheme == PortScheme.OnePort:
            column_names = [self.user_column]
            for i in range(self.top_k):
                column_names += [self.rated_item_columns[i], self.true_rating_columns[i]]
            column_names += self.true_top_rating_columns
        else:
            column_names = [self.user_column] + self.rated_item_columns

        scored_data_df = scored_data.data_frame[column_names]
        new_scored_data = DataTable(scored_data_df)
        new_scored_data.name = scored_data.name

        return new_scored_data


class RankingRecommendationTask(RecommendationTask):
    def __init__(self, port_scheme: PortScheme, top_k: int):
        module_logger.info(f"Get recommend items from all/unrated items task, port scheme: {port_scheme}")
        super().__init__(port_scheme, evaluator=RankingRecommendationEvaluator)
        self.top_k = top_k
        self.user_column = None
        self.recommended_item_columns = None
        self.recommended_item_hit_columns = None
        self.actual_count_column = None

    def _prepare_scored_data(self, scored_data: DataTable):
        """This function prepare scored data. Including, extract data and reorder columns as expected order."""
        if self.port_scheme == PortScheme.OnePort:
            column_names = [self.user_column]
            for i in range(self.top_k):
                column_names += [self.recommended_item_columns[i], self.recommended_item_hit_columns[i]]
            column_names.append(self.actual_count_column)
        else:
            column_names = [self.user_column] + self.recommended_item_columns

        scored_data_df = scored_data.data_frame[column_names]
        new_scored_data = DataTable(scored_data_df)
        new_scored_data.name = scored_data.name

        return new_scored_data


def build_regression_task(scored_data: DataTable):
    """Build regression recommendation task, if scored_data_meta is valid, return built task, or return None.

    For one port scheme, scored data is expected to look like:
        feature 1      feature 2                  feature 4      Rating     Scored Rating
        12400          V for Vendetta (2005)      1377829724     10         10
        587            Reasonable Doubt (2014)    1395001432     3          1
    If scored data does not has score_column_names attr, then the last two column names must be [Rating, Scored Rating],
    or score_column_names attr should have one key to indicate scored rating column, and label_column_name attr to
    indicate rating column.

    For two port scheme, scored data is expected to look like:
        User       Item                       Scored Rating
        12400      V for Vendetta (2005)      10
        587        Reasonable Doubt (2014)    1
    If scored data dose not has score_column_names attr, then the column names must be [Use, Item, Scored Rating],
    or score_column_names attr should have three keys to indicate user column, item column, scored rating
    column respectively.
    """
    score_column_names_dict = scored_data.meta_data.score_column_names
    if score_column_names_dict:
        score_column_keys = build_regression_column_name_keys(PortScheme.OnePort)
        if _check_score_column_name_keys(score_column_names_dict.keys(), score_column_keys):
            task = RegressionRecommendationTask(port_scheme=PortScheme.OnePort)
            task.scored_rating_column = score_column_names_dict[RECOMMENDATION_REGRESSION_SCORED_RATING_TYPE]
            task.true_rating_column = scored_data.meta_data.label_column_name
            if task.true_rating_column not in scored_data.column_names:
                ErrorMapping.throw(NotLabeledDatasetError(dataset_name=scored_data.name))
            return task

        score_column_keys = build_regression_column_name_keys(PortScheme.TwoPort)
        if _check_score_column_name_keys(score_column_names_dict.keys(), score_column_keys):
            task = RegressionRecommendationTask(port_scheme=PortScheme.TwoPort)
            task.user_column = score_column_names_dict[RECOMMENDATION_USER_COLUMN_TYPE]
            task.item_column = score_column_names_dict[RECOMMENDATION_ITEM_COLUMN_TYPE]
            task.scored_rating_column = score_column_names_dict[RECOMMENDATION_REGRESSION_SCORED_RATING_TYPE]
            return task
    else:
        column_names = scored_data.column_names
        if column_names[-2:] == build_regression_column_names(PortScheme.OnePort):
            task = RegressionRecommendationTask(PortScheme.OnePort)
            task.true_rating_column, task.scored_rating_column = column_names[-2:]
            return task

        if column_names == build_regression_column_names(PortScheme.TwoPort):
            task = RegressionRecommendationTask(PortScheme.TwoPort)
            task.user_column, task.item_column, task.scored_rating_column = column_names
            return task
    return None


def build_backward_compatible_regression_task(scored_data: DataTable):
    """Build regression recommendation task, if scored_data is valid, return built task, or return None.

    This methods build regression task for old legacy scored regression data format. The scored data is expected to
    look like:
        User       Item                       Rating
        12400      V for Vendetta (2005)      10
        587        Reasonable Doubt (2014)    1
    Note that legacy evaluate recommender module version only supports two port scheme, and not supports
    score_column_names attribute.
    """
    column_names = scored_data.column_names
    if column_names == build_backward_compatibility_regression_column_names():
        task = RegressionRecommendationTask(PortScheme.TwoPort)
        task.user_column, task.item_column, task.scored_rating_column = column_names
        return task
    return None


def build_rated_ranking_task(scored_data: DataTable):
    """Build Ranking for rated items task, if scored_data_meta is valid, return built task, or return None.

    For one port scheme, scored data is expected to look like:
        User   Rated Item 1   True Rating 1  Rated Item 2   True Rating 2  True Top Rating 1  True Top Rating 2
        14887  1375666        9              73486          9              10                  10
        19075  1408101        9              2378281        6              9                   7
    If scored data does not has score_column_names attr, then the column names must be
    [User, Rated Item 1, True Rating 1, ..., Rated Item k, True Rating k, True Top Rating 1, ..., True Top Rating k].
    Or score_column_names attr should have keys to indicate user column, k rated item columns, k true rating columns,
    and k true top rating columns.

    For two port scheme, scored data is expected to look like:
        User   Rated Item 1   Rated Item 2
        14887  1375666        73486
        19075  1408101        2378281
    If scored data dose not has score_column_names attr, then the column names must be
    [Use, Rated Item 1, ..., Rated Item k]. Or score_column_names attr should have keys to indicate user column and k
    rated item columns.
    """
    scored_column_names_dict = scored_data.meta_data.score_column_names
    if scored_column_names_dict:
        top_k = (len(scored_column_names_dict) - 1) // 3
        score_column_keys = build_rated_ranking_column_name_keys(PortScheme.OnePort, top_k=top_k)
        if _check_score_column_name_keys(scored_column_names_dict.keys(), score_column_keys):
            task = RankingRatedRecommendationTask(port_scheme=PortScheme.OnePort, top_k=top_k)
            task.user_column = scored_column_names_dict[RECOMMENDATION_USER_COLUMN_TYPE]
            task.rated_item_columns = [scored_column_names_dict[col] for col in score_column_keys[1:2 * top_k:2]]
            task.true_rating_columns = [scored_column_names_dict[col] for col in score_column_keys[2:2 * top_k + 1:2]]
            task.true_top_rating_columns = [scored_column_names_dict[col] for col in score_column_keys[2 * top_k + 1:]]
            return task

        top_k = len(scored_column_names_dict) - 1
        score_column_keys = build_rated_ranking_column_name_keys(PortScheme.TwoPort, top_k=top_k)
        if _check_score_column_name_keys(scored_column_names_dict.keys(), score_column_keys):
            task = RankingRatedRecommendationTask(port_scheme=PortScheme.TwoPort, top_k=top_k)
            task.user_column = scored_column_names_dict[RECOMMENDATION_USER_COLUMN_TYPE]
            task.rated_item_columns = [scored_column_names_dict[col] for col in score_column_keys[1:]]
            return task
    else:
        column_names = scored_data.column_names
        top_k = (len(column_names) - 1) // 3
        if column_names == build_rated_ranking_column_names(PortScheme.OnePort, top_k=top_k):
            task = RankingRatedRecommendationTask(PortScheme.OnePort, top_k=top_k)
            task.user_column = column_names[0]
            task.rated_item_columns = column_names[1:top_k * 2:2]
            task.true_rating_columns = column_names[2:top_k * 2 + 1:2]
            task.true_top_rating_columns = column_names[top_k * 2 + 1:]
            return task

        top_k = len(column_names) - 1
        if column_names == build_rated_ranking_column_names(PortScheme.TwoPort, top_k=top_k):
            task = RankingRatedRecommendationTask(PortScheme.TwoPort, top_k=top_k)
            task.user_column = column_names[0]
            task.rated_item_columns = column_names[1:]
            return task
    return None


def build_backward_compatible_rated_ranking_task(scored_data: DataTable):
    """Build ranking for rated items task, if scored_data is valid, return built task, or return None.

    This method builds rated ranking recommendation task for old legacy scored regression data format.
    The scored data is expected to look like:
        User        Item 1      Item 2       Item 3
        14887       1375666     73486        111161
        19075       1408101     2378281      99674
    Note that legacy evaluate recommender module version only supports two port scheme, and not supports
    score_column_names attribute.
    """
    column_names = scored_data.column_names
    top_k = len(column_names) - 1
    if column_names == build_backward_compatible_rated_ranking_column_names(top_k=top_k):
        task = RankingRatedRecommendationTask(PortScheme.TwoPort, top_k=top_k)
        task.user_column = column_names[0]
        task.rated_item_columns = column_names[1:]
        return task
    return None


def build_ranking_task(scored_data: DataTable):
    """Build Ranking for all/unrated items task, if scored_data_meta is valid, return built task, or return None.

    For one port scheme, scored data is expected to look like:
        User       Recommended Item 1     Hit 1      Recommended Item 2,     Hit 2      Actual Count
        12400      111161                 False      99674                   False       1
        587        100150                 True       99674                   False       4
    If scored data does not has score_column_names attr, then the column names must be
    [User, Recommended Item 1, Hit 1, ..., Recommended Item k, Hit k, Actual Count]. Or score_column_names attr should
    have keys to indicate user column, k recommended item columns, k hit columns, and actual count column.

    For two port scheme, scored data is expected to look like:
        User       Recommended Item 1     Recommended Item 2
        12400      111161                 99674
        587        100150                 99674
    If scored data dose not has score_column_names attr, then the column names must be
    [Use, Recommended Item 1, ..., Recommended Item k]. Or score_column_names attr should have keys to indicate user
    column and k recommended item columns.
    """
    score_column_names_dict = scored_data.meta_data.score_column_names
    if score_column_names_dict:
        top_k = (len(score_column_names_dict) - 2) // 2
        score_column_keys = build_ranking_column_name_keys(port_scheme=PortScheme.OnePort, top_k=top_k)
        if _check_score_column_name_keys(score_column_names_dict.keys(), score_column_keys):
            task = RankingRecommendationTask(port_scheme=PortScheme.OnePort, top_k=top_k)
            task.user_column = score_column_names_dict[RECOMMENDATION_USER_COLUMN_TYPE]
            task.recommended_item_columns = [score_column_names_dict[col] for col in score_column_keys[1:2 * top_k:2]]
            task.recommended_item_hit_columns = [score_column_names_dict[col] for col in score_column_keys[2::2]]
            task.actual_count_column = score_column_names_dict[RECOMMENDATION_RECOMMENDED_ACTUAL_COUNT_TYPE]
            return task

        top_k = len(score_column_names_dict) - 1
        score_column_keys = build_ranking_column_name_keys(port_scheme=PortScheme.TwoPort, top_k=top_k)
        if _check_score_column_name_keys(score_column_names_dict.keys(), score_column_keys):
            task = RankingRecommendationTask(port_scheme=PortScheme.TwoPort, top_k=top_k)
            task.user_column = score_column_names_dict[RECOMMENDATION_USER_COLUMN_TYPE]
            task.recommended_item_columns = [score_column_names_dict[col] for col in score_column_keys[1:]]
            return task
    else:
        column_names = scored_data.column_names
        top_k = (len(column_names) - 2) // 2
        if column_names == build_ranking_column_names(port_scheme=PortScheme.OnePort, top_k=top_k):
            task = RankingRecommendationTask(port_scheme=PortScheme.OnePort, top_k=top_k)
            task.user_column = column_names[0]
            task.recommended_item_columns = column_names[1:top_k * 2:2]
            task.recommended_item_hit_columns = column_names[2:top_k * 2 + 1:2]
            task.actual_count_column = column_names[-1]
            return task

        top_k = len(column_names) - 1
        if column_names == build_ranking_column_names(port_scheme=PortScheme.TwoPort, top_k=top_k):
            task = RankingRecommendationTask(port_scheme=PortScheme.TwoPort, top_k=top_k)
            task.user_column = column_names[0]
            task.recommended_item_columns = column_names[1:]
            return task
    return None


def build_classification_task(scored_data: DataTable):
    """Build classification recommendation task, if scored_data_meta is valid, return built task, or return None.

    For one port scheme, scored data is expected to look like:
        feature 1  feature 2  feature 3  feature 4      feature 5  Label  Scored Label   Scored Probability
        6849       40         50         Bachelors      13         0      0              0.16749155521392806
        7298       50         43         Some-college   10         1      1              0.9986370205879208
    If scored data does not has score_column_names attr, then the last three column names must be
    [Label, Scored Label, Scored Probability]. Or score_column_names attr should have keys to indicate scored label
    column and scored probability column, and label_column_name attr to indicate true bale column.

    For two port scheme, scored data is expected to look like:
        User       Item       Scored Label   Scored Probability
        6849       40         0      0              0.16749155521392806
        7298       50         1      1              0.9986370205879208
    If scored data dose not has score_column_names attr, then the column names must be
    [Use, Item, Scored Label, Scored Probability]. Or score_column_names attr should have four keys to indicate
    user column, item column, scored label column and scored probability column respectively.
    """
    score_column_names_dict = scored_data.meta_data.score_column_names
    if score_column_names_dict:
        score_column_keys = build_classification_column_name_keys(port_scheme=PortScheme.OnePort)
        if _check_score_column_name_keys(score_column_names_dict.keys(), score_column_keys):
            task = ClassificationRecommendationTask(port_scheme=PortScheme.OnePort)
            task.scored_label_column = score_column_names_dict[RECOMMENDATION_CLASSIFICATION_SCORED_LABEL_TYPE]
            task.scored_prob_column = score_column_names_dict[RECOMMENDATION_CLASSIFICATION_SCORED_PROB_TYPE]
            task.true_label_column = scored_data.meta_data.label_column_name
            if task.true_label_column not in scored_data.column_names:
                ErrorMapping.throw(NotLabeledDatasetError(dataset_name=scored_data.name))
            return task

        score_column_keys = build_classification_column_name_keys(port_scheme=PortScheme.TwoPort)
        if _check_score_column_name_keys(score_column_names_dict.keys(), score_column_keys):
            task = ClassificationRecommendationTask(port_scheme=PortScheme.TwoPort)
            task.user_column = score_column_names_dict[RECOMMENDATION_USER_COLUMN_TYPE]
            task.item_column = score_column_names_dict[RECOMMENDATION_ITEM_COLUMN_TYPE]
            task.scored_label_column = score_column_names_dict[RECOMMENDATION_CLASSIFICATION_SCORED_LABEL_TYPE]
            task.scored_prob_column = score_column_names_dict[RECOMMENDATION_CLASSIFICATION_SCORED_PROB_TYPE]
            return task
    else:
        column_names = scored_data.column_names
        if column_names[-3:] == build_classification_column_names(PortScheme.OnePort):
            task = ClassificationRecommendationTask(PortScheme.OnePort)
            task.true_label_column, task.scored_label_column, task.scored_prob_column = column_names[-3:]
            return task

        if column_names == build_classification_column_names(PortScheme.TwoPort):
            task = ClassificationRecommendationTask(PortScheme.TwoPort)
            task.user_column, task.item_column, task.scored_label_column, task.scored_prob_column = column_names
            return task
    return None


def build_recommendation_task(scored_data: DataTable):
    """Match recommendation task according to the scored dataset column name patterns or score column names attrs.

    For now, evaluate recommender supports 4 kinds of recommendation task: Regression, Classification, Ranking for
    rated items, Ranking for all/unrated items. And recommendation task can be deduced from 2 ways:
    1. according to scored dataset column names
    2. according to score column names attr in DataFrameSchema of scored dataset
    """
    ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(curr_column_count=scored_data.number_of_columns,
                                                                   required_column_count=2,
                                                                   arg_name=scored_data.name)
    build_task_methods = [build_regression_task,
                          build_rated_ranking_task,
                          build_ranking_task,
                          build_classification_task,
                          build_backward_compatible_regression_task,  # check if backward compatible scored data
                          build_backward_compatible_rated_ranking_task]  # check if backward compatible scored data

    task = None
    for method in build_task_methods:
        task = method(scored_data=scored_data)
        if task is not None:
            return task

    return task


def _check_score_column_name_keys(curr_column_keys, exp_column_keys):
    if len(curr_column_keys) != len(exp_column_keys):
        return False
    return all(key in curr_column_keys for key in exp_column_keys)
