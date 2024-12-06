import json
import os
import random
from abc import abstractmethod
from datetime import timedelta, datetime
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import numpy as np
import pgeof
from pandas import to_datetime, get_dummies, read_csv
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import Dataset


class EbatDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.classes = list(np.unique(np.argmax(y, axis=1)))

    def __len__(self):
        return len(self.y)

    def __getitem__(self, item):
        return self.X[item], self.y[item]


class Retriever:

    def __init__(self, config):
        random.seed(42)
        self.config = config

    @abstractmethod
    def load_datasets(self) -> (EbatDataset, EbatDataset, EbatDataset, EbatDataset):
        raise NotImplementedError("Implement this method in children.")


class MedbaRetriever(Retriever):
    def __init__(self, config):
        super(MedbaRetriever, self).__init__(config)
        all_users = [x for x in range(1, 55)]
        all_users.remove(3)
        self.ADV_USERS = sorted(
            random.sample(
                list(set(all_users) - set(self.config["users"])),
                len(self.config["users"]),
            )
        )
        self.DIFFICULTIES = ["lo", "md", "hg"]

        self.user_classes = None
        self.data_path = Path(os.getcwd()) / "data/medba/"
        if not os.path.exists(self.data_path):
            self.download()

    def download(self):
        print("Downloading Medba data...", end="")
        try:
            os.makedirs(self.data_path, exist_ok=False)
        except FileExistsError:
            print(
                f"\nFiles already downloaded.\nIf corrupted, delete the {self.data_path} folder and try again."
            )
            print("")
        urlretrieve(
            "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/Behaviouralbiometrics/iot_dataset.zip",
            self.data_path / "medba.zip",
        )
        print("DONE")
        print("Extracting Medba data...", end="")
        with ZipFile(self.data_path / "medba.zip", "r") as zip_ref:
            zip_ref.extractall(self.data_path)
        os.remove(self.data_path / "medba.zip")
        print("DONE")

    def _cast_datetime(self, data):
        try:
            data["time"] = to_datetime(data["time"])
        except ValueError:
            # Some dates are malformed, therefore, we fix the issue here.
            timedates = data["time"].tolist()
            for i, x in enumerate(timedates):
                if len(x) != 32:
                    timedates[i] = x[:19] + ".000000+00:00"
            data["time"] = to_datetime(timedates)
        return data

    def _generate_lookback(self, X, y):
        X_lookback, y_lookback, X_window, y_window = [], [], [], []
        for X_curr, y_curr in zip(X, y):
            if len(X_window) < self.config["lookback"]:
                X_window.append(X_curr)
                y_window.append(y_curr)
            else:
                if len(set(y_window)) == 1:
                    X_lookback.append(X_window.copy())
                    y_lookback.append(y_window[0])

                X_window.append(X_curr)
                X_window.pop(0)
                y_window.append(y_curr)
                y_window.pop(0)

        if len(set(y_window)) == 1:
            X_lookback.append(X_window.copy())
            y_lookback.append(y_window[0])

        return np.array(X_lookback), np.array(y_lookback)

    def _scale(self, X, y):
        X = MinMaxScaler().fit_transform(X)
        if "lookback" in self.config.keys() and self.config["lookback"]:
            X, y = self._generate_lookback(X, y)
        y = get_dummies(np.array(y), dtype=float).values
        return X, y

    def _pointcloud_feature_extraction(self, xyz):
        xyz.insert(0, [0, 0, 0])
        xyz = np.array(xyz).astype(np.float32)
        radius = 0.2
        k = 3
        try:
            knn, _ = pgeof.radius_search(xyz, xyz, radius, k)
        except ValueError:
            return np.repeat(0, 11)

        # Converting radius neighbors to CSR format
        nn_ptr = np.r_[0, (knn >= 0).sum(axis=1).cumsum()]
        nn = knn[knn >= 0]

        # You may need to convert nn/nn_ptr to uint32 arrays
        nn_ptr = nn_ptr.astype("uint32")
        nn = nn.astype("uint32")

        features = pgeof.compute_features(xyz, nn, nn_ptr)
        return features[0]

    def _load_dataset(self, partition):
        # We split the dataset in two parts for the purpose of validation/test split.
        # Also generate an adversarial dataset consisting of the same number of other users.
        users = self.config["users"] if partition != "adver" else self.ADV_USERS
        X, y = [], []
        for user in users:
            seances = os.listdir(self.data_path / f"{str(user).zfill(3)}")
            iot_data = read_csv(
                self.data_path
                / f"{str(user).zfill(3)}/{seances[self.config[partition]['seance']]}"
                / f"{self.config['exp_device']}/{self.config['task']}"
                / f"{self.DIFFICULTIES[self.config[partition]['diff']]}/iot_records.csv"
            )
            radar_data = read_csv(
                self.data_path
                / f"{str(user).zfill(3)}/{seances[self.config[partition]['seance']]}"
                / f"{self.config['exp_device']}/{self.config['task']}"
                / f"{self.DIFFICULTIES[self.config[partition]['diff']]}/radar_records.csv"
            )
            iot_data = self._cast_datetime(iot_data)
            radar_data = self._cast_datetime(radar_data)

            radar_data["radar pointcloud"] = radar_data["radar pointcloud"].apply(
                json.loads
            )
            radar_data["radar features"] = radar_data["radar pointcloud"].apply(
                self._pointcloud_feature_extraction
            )
            curr_time = iot_data["time"].min()
            end_time = iot_data["time"].max()
            window = timedelta(seconds=self.config["window"])
            window_step = timedelta(seconds=self.config["window_step"])

            while True:
                curr_data = iot_data[
                    (iot_data["time"] >= curr_time)
                    & (iot_data["time"] <= curr_time + window)
                ]
                curr_data = curr_data.groupby("sensor id").mean().values.T[0].tolist()
                if len(curr_data) != 28:
                    # This sometimes occur at the very end of the session.
                    # In that case, we discard the data for the remainder of the session.
                    # print(f"Data for user {user} has only {len(curr_data)} sensors.")
                    break
                rad_data = radar_data[
                    (radar_data["time"] >= curr_time)
                    & (radar_data["time"] <= curr_time + window)
                ]
                try:
                    curr_data.extend(rad_data["radar features"].values[0].tolist())
                except IndexError:
                    curr_data.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

                X.append(curr_data)
                y.append(users.index(user))
                curr_time += window_step
                if curr_time > end_time:
                    break

        X, y = self._scale(X, y)
        return X, y

    def load_datasets(self):
        print("Loading the dataset...", end="")

        s = datetime.now()
        X_train, y_train = self._load_dataset("train")
        X_valid, y_valid = self._load_dataset("valid")
        X_test, y_test = self._load_dataset("test")
        X_adver, y_adver = self._load_dataset("adver")
        print(f"DONE ({datetime.now() - s})")

        print(f"Train dataset size: {X_train.shape} {y_train.shape}")
        print(f"Validation dataset size: {X_valid.shape} {y_valid.shape}")
        print(f"Test dataset size: {X_test.shape} {y_test.shape}")
        print(f"Adver dataset size: {X_adver.shape} {y_adver.shape}")
        self.user_classes = [i for i in range(y_train.shape[1])]
        return (
            EbatDataset(X_train, y_train),
            EbatDataset(X_valid, y_valid),
            EbatDataset(X_test, y_test),
            EbatDataset(X_adver, y_adver),
        )


if __name__ == "__main__":
    ret = MedbaRetriever(
        {
            "users": [5, 6, 22, 24, 27, 31, 38, 41, 43, 45, 49, 50, 51, 53, 54],
            "exp_device": "comp",
            "task": "Typing",
            "window": 1,
            "window_step": 0.5,
            "train": {"seance": 0, "diff": 0},
            "valid": {"seance": 0, "diff": 0},
            "test": {"seance": 0, "diff": 0},
            "adver": {"seance": 0, "diff": 0},
        }
    )
    ret.load_datasets()
