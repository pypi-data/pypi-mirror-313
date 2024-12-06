import re

from pytorch_lightning.callbacks import Callback
import torchmetrics
from torchmetrics import Accuracy, Precision, Recall, AUROC
import torch
import requests

class MLOpsLightningCallback(Callback):
    def __init__(self, experiment, epochs, num_classes=None, metrics_to_log=None, log_dir="logs/mlops", log_on_batch=False):
        super().__init__()
        experiment.total_epochs = epochs
        experiment.current_epoch = 0
        self.experiment = experiment
        self.log_dir = log_dir
        self.log_on_batch = log_on_batch

        self.num_classes = num_classes
        self.metrics_to_log = metrics_to_log or ["accuracy", "precision", "recall", "auc"]
        self.metrics = {}

        # Define the task as "multiclass" because the number of classes is more than 2
        task = "multiclass" if num_classes and num_classes > 2 else "binary"

        # Initialize metrics dynamically based on the number of classes
        self.metrics["accuracy"] = Accuracy(task=task, num_classes=num_classes, average="macro")
        self.metrics["precision"] = Precision(task=task, num_classes=num_classes, average="macro")
        self.metrics["recall"] = Recall(task=task, num_classes=num_classes, average="macro")
        self.metrics["auc"] = AUROC(task=task, num_classes=num_classes)

    def log_to_server(self, metric_name, metric_value, step):

        # time.sleep(.1)
        # Send data to MLOps platform
        payload = {
            "experiment_id": self.experiment.experiment_id,
            "run_id": self.experiment.run_id,
            "metric_name": metric_name,
            "metric_value": float(metric_value),
            "step": step,
            "experiment_platform_type": "pytorch-lightning",
        }

        try:
            response = requests.post(self.experiment.server_url + "/api/experiments/log_metric", json=payload)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Failed to log to MLOps: {e}")

    # def on_train_epoch_end(self, trainer, pl_module):
    #     epoch_outputs = trainer.fit_loop.epoch_loop.batch_outputs
    #     all_preds = []
    #     all_targets = []
    #
    #     # Collect predictions and targets from all batches
    #     for batch_outputs in epoch_outputs:
    #         for output in batch_outputs:
    #             preds = output["preds"]
    #             targets = output["targets"]
    #             all_preds.append(preds)
    #             all_targets.append(targets)
    #
    #     # Concatenate all predictions and targets
    #     all_preds = torch.cat(all_preds, dim=0)
    #     all_targets = torch.cat(all_targets, dim=0)
    #
    #     # Calculate and log metrics
    #     for metric_name, metric_fn in self.metrics.items():
    #         if metric_name in self.metrics_to_log:
    #             metric_value = metric_fn(all_preds, all_targets)
    #             print(f"Epoch {trainer.current_epoch} - {metric_name}: {metric_value}")
    #             self.log_to_mlops(metric_name, metric_value, trainer.current_epoch)

    def clean_metric_name(self, metric_name):
        """
        Removes any '_<number>' suffix from the metric name.
        """
        return re.sub(r'_\d+$', '', metric_name)

    def on_train_epoch_end(self, trainer, pl_module):
        # # Aggregate predictions and targets
        # outputs = trainer.predict(dataloaders=trainer.train_dataloader)
        # all_preds, all_targets = self._aggregate_outputs(outputs)
        #
        # # Calculate and log metrics
        # for metric_name, metric_fn in self.metrics.items():
        #     if metric_name in self.metrics_to_log:
        #         metric_value = metric_fn(all_preds, all_targets)
        #         print(f"Train Epoch {trainer.current_epoch} - {metric_name}: {metric_value}")
        #         self.log_to_mlops(metric_name, metric_value, trainer.current_epoch)
        all_preds = []
        all_targets = []

        # Ensure the model is on the same device as the inputs
        device = pl_module.device

        # Move metrics to the correct device
        for metric_name, metric_fn in self.metrics.items():
            self.metrics[metric_name] = metric_fn.to(device)

        # Iterate through the training dataloader
        # for batch in trainer.train_dataloader:
        #     x, y = batch
        #     x, y = x.to(device), y.to(device)  # Move tensors to the same device as the model
        #     logits = pl_module(x)
        #     preds = torch.argmax(logits, dim=1)
        #
        #     all_preds.append(preds)
        #     all_targets.append(y)

        # Concatenate all predictions and targets
        # Collect raw logits instead of class indices
        for batch in trainer.train_dataloader:
            x, y = batch
            x, y = x.to(device), y.to(device)  # Move to device
            logits = pl_module(x)  # Raw logits from the model
            all_preds.append(logits)  # Store logits
            all_targets.append(y)  # Store targets

        # Concatenate raw logits and targets
        all_preds = torch.cat(all_preds, dim=0)  # Shape: [num_samples, num_classes]
        all_targets = torch.cat(all_targets, dim=0)  # Shape: [num_samples]

        # Calculate and log metrics
        for metric_name, metric_fn in self.metrics.items():
            if metric_name in self.metrics_to_log:
                metric_value = metric_fn(all_preds, all_targets)
                cleaned_name = self.clean_metric_name(metric_name)
                # print(f"Train Epoch {trainer.current_epoch} - {metric_name}: {metric_value}")
                self.log_to_server(f"train/epoch/{cleaned_name}", metric_value, trainer.current_epoch)

        # print(f"Train Epoch {trainer.current_epoch} - {metric_name}: {metric_value}")

    # def _aggregate_outputs(self, outputs):
    #     all_preds = []
    #     all_targets = []
    #
    #     for batch in outputs:
    #         all_preds.append(batch["preds"])
    #         all_targets.append(batch["targets"])
    #
    #     return torch.cat(all_preds, dim=0), torch.cat(all_targets, dim=0)

    # def log_to_mlops(self, metric_name, metric_value, epoch):
    #     if self.experiment:
    #         payload = {
    #             # "experiment_id": self.experiment.experiment_id,
    #             # "run_id": self.experiment.run_id,
    #             "metric_name": metric_name,
    #             "metric_value": float(metric_value),
    #             "step": epoch,
    #             "experiment_platform_type": "pytorch-lightning",
    #         }
    #         try:
    #             # Replace with your server logging logic
    #             print(f"Logging to server: {payload}")
    #         except Exception as e:
    #             print(f"Failed to log metric: {e}")
