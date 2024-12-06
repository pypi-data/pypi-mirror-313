import os

import numpy as np
from plotly import graph_objects as go
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, det_curve

from ebat.evaluation.metrics.roc import false_acceptance_rate, false_rejection_rate


class Evaluator:

    def __init__(self, decimal_places=3, plots=True):
        self.decimal_places = decimal_places
        self.plots = plots

        self.far = []
        self.frr = []
        self.thresholds = []

    def evaluate(self, authenticator, test_data, adver_data, verbose=1):
        acc, prec, rec, f1 = self.identification(authenticator, test_data)
        err = self.authentication(authenticator, test_data, adver_data)

        if verbose:
            print("==================================================================")
            print(f"Evaluation of {authenticator.name()} with the medba dataset.")
            print("==================================================================")
            print(
                "Classification Accuracy:",
                round(acc, self.decimal_places),
            )
            print("Precision:", round(prec, self.decimal_places))
            print("Recall:", round(rec, self.decimal_places))
            print("F1 Score:", round(f1, self.decimal_places))
            print("Equal Error Rate:", round(err, self.decimal_places))

        if self.plots:
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=self.thresholds, y=self.far, name="False Acceptance Rate"
                    ),
                    go.Scatter(
                        x=self.thresholds, y=self.frr, name="False Rejection Rate"
                    ),
                ]
            )
            fig.update_layout(
                xaxis_title="Confidence Threshold",
                yaxis_title="False Rates",
            )
            fig.show()

            fig = go.Figure(
                data=[
                    go.Scatter(x=self.far, y=1 - self.frr),
                ]
            )
            fig.update_layout(
                xaxis_title="False Acceptance Rate",
                yaxis_title="False Rejection Rate",
            )
            fig.show()
        return acc, prec, rec, f1, self.far, self.frr, self.thresholds, err

    def compare(self, authenticators, test_data, adver_data, verbose=1, plots=False):
        results = {}
        for authenticator in authenticators:
            results[authenticator] = self.evaluate(
                authenticator, test_data, adver_data, verbose=0
            )
        if plots:
            data = []
            for authenticator in authenticators:
                data.append(
                    go.Scatter(
                        x=results[authenticator][4],
                        y=1 - results[authenticator][5],
                        name=str(authenticator),
                    ),
                )
            fig = go.Figure(data=data)
            fig.update_layout(
                xaxis_title="False Acceptance Rate",
                yaxis_title="1 - False Rejection Rate",
            )
            fig.show()

    def identification(self, authenticator, test_data):
        X_test = test_data.X
        y_test = list(np.argmax(test_data.y, axis=1))

        y_pred = np.argmax(authenticator.identification(X_test), axis=1)
        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average="macro", zero_division=0
        )
        return acc, prec, rec, f1

    def authentication(self, authenticator, test_data, adver_data):
        X_auth = np.concatenate((test_data.X, adver_data.X))
        y_auth = list(np.repeat(True, len(test_data.y))) + list(
            np.repeat(False, len(adver_data.y))
        )
        y_scores = authenticator.authentication(X_auth)
        far, frr, thresholds = det_curve(y_auth, y_scores)
        self.far = far
        self.frr = frr
        self.thresholds = thresholds

        deltas = [abs(x - y) for x, y in zip(far, frr)]
        min_i = np.argmin(deltas)
        return (far[min_i] + frr[min_i]) / 2
