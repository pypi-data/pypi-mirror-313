# experiment.py

from turihub import Hub
# import neptune.new as neptune
from tensorboardX import SummaryWriter
import pytorch_lightning as pl
import mlflow

class BaseExperiment:
    """
    Base experiment class to define common methods across platforms.
    """
    def log_metric(self, name, value, step=None):
        raise NotImplementedError("log_metric must be implemented in subclasses.")

    def log_image(self, name, image, step=None):
        raise NotImplementedError("log_image must be implemented in subclasses.")

    def stop(self):
        raise NotImplementedError("stop must be implemented in subclasses.")


class HubExperiment(BaseExperiment):
    """
    Experiment class for logging data to Neptune.
    """
    def __init__(self, **kwargs):
        api_token = "97f5426b-46d5-4712-95ce-030ac3ae2bbb"
        self.run = Hub(apikey=api_token, **kwargs)

    def project(self, projectname):
        project = self.run.project(projectname)
        return project

    def log_metric(self, name, value, step=None):
        self.run[name].log(value, step=step)

    def log_image(self, name, image, step=None):
        self.run[name].upload(image)

    def stop(self):
        self.run.stop()

# class NeptuneExperiment(BaseExperiment):
#     """
#     Experiment class for logging data to Neptune.
#     """
#     def __init__(self, project, api_token, **kwargs):
#         self.run = neptune.init_run(project=project, api_token=api_token, **kwargs)
#
#     def log_metric(self, name, value, step=None):
#         self.run[name].log(value, step=step)
#
#     def log_image(self, name, image, step=None):
#         self.run[name].upload(image)
#
#     def stop(self):
#         self.run.stop()


class TensorboardExperiment(BaseExperiment):
    """
    Experiment class for logging data to TensorBoard.
    """
    def __init__(self, log_dir="logs"):
        self.writer = SummaryWriter(log_dir)

    def log_metric(self, name, value, step=None):
        self.writer.add_scalar(name, value, global_step=step)

    def log_image(self, name, image, step=None):
        self.writer.add_image(name, image, global_step=step)

    def stop(self):
        self.writer.close()


class PytorchLightningExperiment(BaseExperiment):
    """
    Experiment class for logging data via PyTorch Lightning's built-in logger.
    """
    def __init__(self, logger=None):
        self.logger = logger or pl.loggers.TensorBoardLogger("logs/")

    def log_metric(self, name, value, step=None):
        if step:
            self.logger.log_metrics({name: value}, step)
        else:
            self.logger.log_metrics({name: value})

    def log_image(self, name, image, step=None):
        # PyTorch Lightning does not directly support image logging in the default loggers.
        pass

    def stop(self):
        # PyTorch Lightning logger cleanup is usually handled by the framework, so this may not be necessary.
        pass

class MLFlowExperiment(BaseExperiment):
    """
    Experiment class for logging data to MLFlow.
    """
    def __init__(self, experiment_name="default"):
        mlflow.set_experiment(experiment_name)
        self.run = mlflow.start_run()

    def log_metric(self, name, value, step=None):
        mlflow.log_metric(name, value, step=step)

    def log_image(self, name, image, step=None):
        # MLFlow logs images as artifacts
        mlflow.log_artifact(image, artifact_path=name)

    def log_param(self, name, value):
        mlflow.log_param(name, value)

    def stop(self):
        mlflow.end_run()