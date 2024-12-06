import torch
import random
from torch.utils.data import Dataset
from transformers import AutoTokenizer


def text_dummy_dataset(model_id="bert-base-uncased", num_classes=2, max_length=None):
    # Generate synthetic data
    words = [
        "apple",
        "banana",
        "car",
        "dog",
        "elephant",
        "flower",
        "giraffe",
        "happy",
        "ice",
        "jungle",
    ]
    num_samples = 100
    data = [
        {
            "text": " ".join(
                random.choice(words) for _ in range(random.randint(4, 10))
            ),
            "label": random.randint(0, num_classes - 1),
        }
        for _ in range(num_samples)
    ]  # Labels are dynamic based on num_classes

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Prepare dataset
    if max_length is not None:
        # If max_length is specified, enable truncation and padding to max_length
        encodings = tokenizer(
            [x["text"] for x in data],
            max_length=max_length,
            truncation=True,
            padding="max_length",
        )
    else:
        # If max_length is None, do not explicitly set truncation and padding to max_length
        encodings = tokenizer([x["text"] for x in data], padding=True)
    labels = [x["label"] for x in data]
    return TextDataset(encodings, labels)


# Dataset
class TextDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)
