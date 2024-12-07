import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader


# Custom dataset
class GenericDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features.astype(np.float32)
        self.labels = labels.astype(np.float32)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return torch.tensor(self.features[idx]), torch.tensor(self.labels[idx])


def generate_generic_data(num_samples, num_feature_points, num_classes):

    # Generate dummy data with simpler column names and only float/int values
    dummy_data = {
        "a": np.random.randint(0, 10000, num_samples),
        "b": np.random.uniform(0, 1000, num_samples),
        "c": np.random.randint(0, 500, num_samples),
        "d": np.random.uniform(5000, 10000, num_samples),
        "e": np.random.randint(0, 3000, num_samples),
        "f": np.random.uniform(100, 1000, num_samples),
        "g": np.random.randint(0, 500, num_samples),
        "h": np.random.uniform(0, 500, num_samples),
        "i": np.random.uniform(0, 100, num_samples),
        "j": np.random.randint(0, 1000, num_samples),
        "k": np.random.uniform(0, 500, num_samples),
        "l": np.random.uniform(0, 200, num_samples),
        "m": np.random.randint(0, 2000, num_samples),
        "n": np.random.uniform(0, 300, num_samples),
        "o": np.random.uniform(0, 10, num_samples),
        "p": np.random.randint(0, 200, num_samples),
        "q": np.random.uniform(0, 500, num_samples),
        "r": np.random.uniform(0, 1000, num_samples),
        "s": np.random.uniform(0, 1000, num_samples),
        "t": np.random.uniform(0, 1000, num_samples),
        "u": np.random.uniform(0, 1000, num_samples),
        "v": np.random.uniform(0, 1000, num_samples),
        "w": np.random.randint(0, 100, num_samples),
        "x": np.random.uniform(0, 10, num_samples),
        "y": np.random.randint(0, 100, num_samples),
        "z": np.random.uniform(0, 500, num_samples),
        "aa": np.random.uniform(0, 500, num_samples),
        "ab": np.random.uniform(0, 1000, num_samples),
        "ac": np.random.uniform(0, 500, num_samples),
        "ad": np.random.uniform(0, 500, num_samples),
        "ae": np.random.randint(0, 100, num_samples),
        "af": np.random.uniform(0, 500, num_samples),
        "ag": np.random.uniform(0, 10, num_samples),
        "ah": np.random.uniform(0, 10, num_samples),
        "ai": np.random.uniform(0, 500, num_samples),
        "aj": np.random.uniform(0, 500, num_samples),
        "ak": np.random.uniform(0, 500, num_samples),
        "al": np.random.uniform(0, 500, num_samples),
        "am": np.random.uniform(0, 500, num_samples),
        "an": np.random.uniform(0, 500, num_samples),
        "ao": np.random.uniform(0, 500, num_samples),
        "ap": np.random.uniform(0, 500, num_samples),
        "aq": np.random.uniform(0, 500, num_samples),
        "ar": np.random.uniform(0, 500, num_samples),
        "as": np.random.uniform(0, 500, num_samples),
        "at": np.random.uniform(0, 500, num_samples),
        "au": np.random.uniform(0, 500, num_samples),
        "av": np.random.uniform(0, 500, num_samples),
        "aw": np.random.uniform(0, 500, num_samples),
        "ax": np.random.uniform(0, 500, num_samples),
        "ay": np.random.uniform(0, 500, num_samples),
        "az": np.random.uniform(0, 500, num_samples),
        "ba": np.random.uniform(0, 500, num_samples),
        "bb": np.random.uniform(0, 500, num_samples),
        "bc": np.random.uniform(0, 500, num_samples),
        "bd": np.random.uniform(0, 500, num_samples),
        "be": np.random.uniform(0, 500, num_samples),
        "bf": np.random.uniform(0, 500, num_samples),
        "bg": np.random.uniform(0, 500, num_samples),
        "bh": np.random.uniform(0, 500, num_samples),
        "bi": np.random.uniform(0, 500, num_samples),
        "bj": np.random.randint(0, 2, num_samples),  # Binary class label
    }

    # Generate dummy data with exactly 69 features and only float/int values
    dummy_data = {
        f"feature_{i}": np.random.uniform(0, 100, num_samples)
        for i in range(num_feature_points)
    }
    dummy_data["label"] = np.random.randint(
        0, num_classes, num_samples
    )  # Binary class label

    # Convert dictionary to DataFrame and extract features and labels
    features = pd.DataFrame(dummy_data).iloc[:, :num_feature_points].values
    labels = pd.DataFrame(dummy_data)["label"].values
    return features, labels


def get_dataloader(num_samples=50, num_feature_points=69, batch_size=4, num_classes=2):
    data_features, labels = generate_generic_data(
        num_samples=num_samples,
        num_feature_points=num_feature_points,
        num_classes=num_classes,
    )
    # Create Dataset and DataLoader
    dataset = GenericDataset(data_features, labels)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)
