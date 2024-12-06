from abc import abstractmethod
from random import sample, randint

import numpy as np
import torch
from sklearn.ensemble import RandomForestClassifier
from torch.utils.data import DataLoader
from plotly import graph_objects as go

from data.retrievers import MedbaRetriever
from evaluation.evaluator import Evaluator


class BaseClassifier:

    def __init__(self):
        pass

    @abstractmethod
    def identification(self, X_test):
        pass

    @abstractmethod
    def authentication(self, X_auth, confidence_level=0.5):
        pass


class RandomClassifier:

    def __init__(self, user_classes):
        self.user_classes = user_classes

    def name(self):
        return "Random Classifier"

    def train(self, train_data):
        pass

    def predict_users(self, X_test):
        return [sample(self.user_classes, 1)[0] for _ in range(len(X_test))]

    def authenticate(self, X_auth, confidence_level):
        return [
            False if x < confidence_level else True for x in np.random.rand(len(X_auth))
        ]


class RandomForest(BaseClassifier):

    def __init__(self, user_classes):
        self.user_classes = user_classes
        self.model = RandomForestClassifier()

    def name(self):
        return "Random Forest Classifier"

    def train(self, train_data):
        """
        Trains the model.
        """
        y_train = np.argmax(train_data.y, axis=1)
        self.model.fit(train_data.X, y_train)

    def predict_users(self, X_test):
        """
        Takes test data of shape (n_samples, n_features) and returns a vector of predicted classes.
        """
        return self.model.predict(X_test)

    def authenticate(self, X_adver, confidence_level):
        """
        X_adver: test data of shape (n_samples, n_features) that includes legitimate and illegitimate users.
        confidence_level: confidence level of the authenticator.

        return boolean list of whether each data record should be authenticated.
        """
        y_proba = self.model.predict_proba(X_adver)
        result = np.max(y_proba, axis=1) >= confidence_level
        return result.tolist()


class MLPModel(torch.nn.Module):
    def __init__(self, user_classes):
        super().__init__()
        self.linear1 = torch.nn.Linear(39, 1024)
        self.activation = torch.nn.ReLU()
        self.dropout = torch.nn.Dropout(0.5)
        self.linear2 = torch.nn.Linear(1024, len(user_classes))
        self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, x):
        x = self.linear1(x)
        x = self.activation(x)
        x = self.dropout(x)
        x = self.linear2(x)
        x = self.softmax(x)
        return x


class SimpleMLP(BaseClassifier):

    def __init__(self, user_classes):
        super().__init__()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = MLPModel(user_classes).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.0001)
        self.loss = torch.nn.CrossEntropyLoss()

    def name(self):
        return "Simple MLP Classifier"

    def train(self, train_data):
        train_data = DataLoader(
            train_data,
            batch_size=32,
            shuffle=True,
            drop_last=True,
        )
        self.model.train()
        for e in range(10):
            for X, y in train_data:
                X, y = X.to(self.device).float(), y.to(self.device).float()
                y_pred = self.model(X)
                loss = self.loss(y_pred, y)

                loss.backward()
                self.optimizer.step()

    def identification(self, X_test):
        self.model.eval()
        X_test = torch.tensor(X_test).to(self.device).float()
        y_pred = self.model(X_test)
        return y_pred.argmax(axis=1).cpu().numpy()

    def authentication(self, X_adver, confidence_level):
        self.model.eval()
        X_adver = torch.tensor(X_adver).to(self.device).float()
        y_proba = self.model(X_adver).detach().cpu().numpy()
        result = np.max(y_proba, axis=1) >= confidence_level
        return result.tolist()


if __name__ == "__main__":
    DATA_CONFIG = {
        "users": [5, 6, 22, 24, 27, 31, 38, 41, 43, 45, 49, 50, 51, 53, 54],
        "exp_device": "comp",
        "task": "Hidden Patterns",
        "window": 1,
        "window_step": 0.5,
        "train": {"seance": 0, "diff": 0},
        "valid": {"seance": 0, "diff": 0},
        "test": {"seance": 0, "diff": 1},
        "adver": {"seance": 0, "diff": 1},
    }
    ret = MedbaRetriever(DATA_CONFIG)
    train, validation, test, adver = ret.load_datasets()

    classifier = SimpleMLP(ret.user_classes)
    classifier.train(train)

    evaluator = Evaluator(plots=False)
    evaluator.evaluate(test, adver, classifier)
