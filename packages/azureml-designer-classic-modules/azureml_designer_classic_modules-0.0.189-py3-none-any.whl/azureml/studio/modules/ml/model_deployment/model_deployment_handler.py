from pathlib import Path

from azureml.studio.core.utils.model_deployment.model_deployment_handler import ModelDeploymentHandler


BASE_PATH = Path.resolve(Path(__file__)).parent / 'resources'


class BaseLearnerDeploymentHandler(ModelDeploymentHandler):
    score_template_path = BASE_PATH / 'base_learner/score.py'
    conda_template_path = BASE_PATH / 'base_learner/conda_env.yaml'


class ClusterModelDeploymentHandler(ModelDeploymentHandler):
    score_template_path = BASE_PATH / 'cluster_model/score.py'
    conda_template_path = BASE_PATH / 'cluster_model/conda_env.yaml'


class SVDRecommendationDeploymentHandler(ModelDeploymentHandler):
    score_template_path = BASE_PATH / 'svd_recommender/score.py'
    conda_template_path = BASE_PATH / 'svd_recommender/conda_env.yaml'
