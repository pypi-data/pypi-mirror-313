import os

import numpy as np
from plotly import graph_objects as go
from sklearn.metrics import precision_recall_fscore_support

from evaluation.metrics.roc import false_acceptance_rate, false_rejection_rate
from evaluation.metrics.confusion import classification_accuracy


class Evaluator:

    def __init__(self, decimal_places=3, plots=True, thresholds=np.linspace(0, 1, 100)):
        self.decimal_places = decimal_places
        self.plots = plots
        self.thresholds = thresholds

        self.fars = []
        self.frrs = []
        self.err = 1
        self.err_i = 0

    def evaluate(self, test_data, adver_data, authenticator):
        X_test = test_data.X
        X_auth = np.concatenate((X_test, adver_data.X))
        y_test = list(np.argmax(test_data.y, axis=1))
        y_auth = list(np.repeat(True, len(y_test))) + list(
            np.repeat(False, len(adver_data.y))
        )

        print("==================================================================")
        print(f"Evaluation of {authenticator.name()} with the medba dataset.")
        print("==================================================================")
        y_pred = authenticator.identification(X_test)
        print(
            "Classification Accuracy:",
            round(classification_accuracy(y_test, y_pred), self.decimal_places),
        )
        prec, rec, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average="macro", zero_division=0
        )
        print("Precision:", round(prec, self.decimal_places))
        print("Recall:", round(rec, self.decimal_places))
        print("F1 Score:", round(f1, self.decimal_places))

        fars, frrs = [], []
        for confidence in self.thresholds:
            y_granted = authenticator.authentication(X_auth, confidence)
            fars.append(false_acceptance_rate(y_auth, y_granted))
            frrs.append(false_rejection_rate(y_auth, y_granted))
        self.fars = fars
        self.frrs = frrs

        deltas = [abs(a - b) for a, b in zip(fars, frrs)]
        i_min = deltas.index(np.min(deltas))
        self.err_i = i_min
        self.err = round((fars[i_min] + frrs[i_min]) / 2, self.decimal_places)
        print(f"Equal Error Rate: {self.err}")

        if self.plots:
            fig = go.Figure(
                data=[
                    go.Scatter(x=self.thresholds, y=fars, name="False Acceptance Rate"),
                    go.Scatter(x=self.thresholds, y=frrs, name="False Rejection Rate"),
                ]
            )
            fig.update_layout(
                xaxis_title="Confidence Threshold",
                yaxis_title="False Rates",
            )
            fig.show()


class Recorder:
    def __init__(self):
        self.results = {}

    def add_approach(self, approach_name):
        if approach_name in self.results.keys():
            raise ValueError("Approach already present in results.")
        self.results[approach_name] = {}

    def add_metric(self, approach_name, metric_name, metric_value):
        if metric_name in self.results[approach_name].keys():
            raise ValueError("Metric already present in results.")
        self.results[approach_name][metric_name] = metric_value
