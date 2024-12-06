import re
import time

import tensorflow as tf
from tensorflow.keras.callbacks import Callback
import requests
import datetime


class MLOpsKerasCallback(Callback):
    def __init__(self, experiment, epochs, log_dir="logs/mlops", log_on_batch=False):
        super().__init__()
        # self.mlops_endpoint = mlops_endpoint
        experiment.total_epochs = epochs
        experiment.current_epoch = 0
        self.experiment = experiment
        self.log_dir = log_dir
        self.log_on_batch = log_on_batch
        self.writer = tf.summary.create_file_writer(self.log_dir)

    def log_to_server(self, metric_name, metric_value, step):

        # time.sleep(.1)
        # Send data to MLOps platform
        payload = {
            "experiment_id": self.experiment.experiment_id,
            "run_id": self.experiment.run_id,
            "metric_name": metric_name,
            "metric_value": metric_value,
            "step": step,
            "experiment_platform_type": "keras",
        }
        # print(f"Preparing to send to server: {payload}")
        try:
            response = requests.post(self.experiment.server_url + "/api/experiments/log_metric", json=payload)
            response.raise_for_status()
            # print(f"Sent to server: {payload}")

            # Check if this is the last metric of the last epoch
            # if is_final_epoch:
            #     self.final_metric_logged = True

        except requests.exceptions.RequestException as e:
            print(f"Failed to log to MLOps: {e}")

    def on_batch_end(self, batch, logs=None):
        if self.log_on_batch:
            logs = logs or {}
            step = self.model.optimizer.iterations.numpy()
            with self.writer.as_default():
                for metric_name, metric_value in logs.items():
                    tf.summary.scalar(f"train/batch/{metric_name}", metric_value, step=step)
                    self.log_to_server(f"train/batch/{metric_name}", metric_value, step)

    def clean_metric_name(self, metric_name):
        """
        Removes any '_<number>' suffix from the metric name.
        """
        return re.sub(r'_\d+$', '', metric_name)

    def on_epoch_end(self, epoch, logs=None):
        # self.current_epoch += 1  # Track the current epoch
        # print(f"Epoch {self.current_epoch}/{self.total_epochs}")
        logs = logs or {}
        # is_final_epoch = self.current_epoch == self.total_epochs  # Check if it's the last epoch

        with self.writer.as_default():
            for metric_name, metric_value in logs.items():
                cleaned_name = self.clean_metric_name(metric_name)
                tf.summary.scalar(f"train/epoch/{cleaned_name}", metric_value, step=epoch)
                self.log_to_server(f"train/epoch/{cleaned_name}", metric_value, epoch)

        self.writer.flush()
        # if is_final_epoch:
        #     # self.experiment.stop()
        #     self.experiment.experiment_done_running()
        #     print("Experiment stopped after final epoch.")
