from pathlib import Path

from azureml.studio.core.utils.model_deployment.model_deployment_handler import ModelDeploymentHandler


BASE_PATH = Path.resolve(Path(__file__)).parent / 'resources'


class VowpalWabbitModelDeploymentHandler(ModelDeploymentHandler):
    score_template_path = BASE_PATH / 'score.py'
    conda_template_path = BASE_PATH / 'conda_env.yaml'
