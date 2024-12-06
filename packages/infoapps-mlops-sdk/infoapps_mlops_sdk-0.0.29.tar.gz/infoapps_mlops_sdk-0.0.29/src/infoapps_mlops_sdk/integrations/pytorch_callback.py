import torch
from torch.utils.tensorboard import SummaryWriter
import requests

class MLOpsPyTorchCallback:
    def __init__(self, experiment, epochs, log_on_batch=False, log_dir="logs/mlops"):
        self.experiment = experiment
        self.log_on_batch = log_on_batch
        self.epochs = epochs
        self.writer = SummaryWriter(log_dir)
        self.current_epoch = 0
        experiment.total_epochs = epochs
        experiment.current_epoch = 0

    def log_to_server(self, metric_name, metric_value, step):
        # Send data to MLOps platform
        payload = {
            "experiment_id": self.experiment.experiment_id,
            "run_id": self.experiment.run_id,
            "metric_name": metric_name,
            "metric_value": metric_value,
            "step": step,
            "experiment_platform_type": "pytorch",
        }
        try:
            response = requests.post(self.experiment.server_url + "/api/experiments/log_metric", json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to log to MLOps: {e}")

    def on_batch_end(self, batch_idx, logs):
        if self.log_on_batch:
            step = logs["step"]
            for metric_name, metric_value in logs.items():
                if metric_name != "step":
                    self.writer.add_scalar(f"train/batch/{metric_name}", metric_value, step)
                    self.log_to_server(f"train/batch/{metric_name}", metric_value, step)

    def on_epoch_end(self, logs):
        for metric_name, metric_value in logs.items():
            self.writer.add_scalar(f"train/epoch/{metric_name}", metric_value, self.current_epoch)
            self.log_to_server(f"train/epoch/{metric_name}", metric_value, self.current_epoch)
        self.current_epoch += 1

    def close(self):
        self.writer.close()