import os

import numpy as np
from plotly import graph_objects as go
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, det_curve


class Evaluator:

    def __init__(self, decimal_places=3, plots=True):
        self.decimal_places = decimal_places
        self.plots = plots

        self.far = []
        self.frr = []
        self.thresholds = []

    def evaluate(self, authenticator, test_data, adver_data, verbose=1, name=None):
        self.identification(authenticator, test_data)
        self.authentication(authenticator, test_data, adver_data)
        self.name = str(authenticator) if not name else name

        if verbose:
            print("==================================================================")
            print(f"Evaluation of {self.name} with the medba dataset.")
            print("==================================================================")
            print(
                "Classification Accuracy:",
                round(self.acc, self.decimal_places),
            )
            print("Precision:", round(self.prec, self.decimal_places))
            print("Recall:", round(self.rec, self.decimal_places))
            print("F1 Score:", round(self.f1, self.decimal_places))
            print("Equal Error Rate:", round(self.err, self.decimal_places))

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

    def identification(self, authenticator, test_data):
        X_test = test_data.X
        y_test = list(np.argmax(test_data.y, axis=1))

        y_pred = np.argmax(authenticator.identification(X_test), axis=1)
        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average="macro", zero_division=0
        )
        self.acc = acc
        self.prec = prec
        self.rec = rec
        self.f1 = f1

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
        self.err = (far[min_i] + frr[min_i]) / 2


class Comparator:

    def __init__(self, evaluators):
        self.evaluators = evaluators

    def compare(self):
        data = []
        for evaluator in self.evaluators:
            data.append(
                go.Scatter(
                    x=evaluator.far,
                    y=1 - evaluator.frr,
                    name=evaluator.name,
                ),
            )
        fig = go.Figure(data=data)
        fig.update_layout(
            xaxis_title="False Acceptance Rate",
            yaxis_title="1 - False Rejection Rate",
        )
        fig.show()
