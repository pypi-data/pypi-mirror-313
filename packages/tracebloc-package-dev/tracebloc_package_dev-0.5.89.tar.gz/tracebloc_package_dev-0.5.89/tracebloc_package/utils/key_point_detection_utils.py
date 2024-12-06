import torch
from torch.utils.data import Dataset
from PIL import Image
import numpy as np


class FakeKeypointDetectionDataset(Dataset):
    def __init__(
        self,
        num_images,
        image_size,
        num_feature_points=4,
        num_classes=10,
        transform=None,
    ):
        self.num_images = num_images
        self.image_size = image_size  # e.g., (2448, 2648)
        self.num_feature_points = num_feature_points
        self.num_classes = num_classes
        self.transform = transform

    def __len__(self):
        return self.num_images

    def __getitem__(self, idx):
        # Create a blank image
        image = Image.new("RGB", self.image_size, color="white")

        # Generate keypoints
        keypoints = self.generate_random_keypoints(
            self.num_feature_points, self.image_size
        )

        # Calculate bounding box
        bboxes = self.get_bbox(keypoints)

        # Transformation logic
        if self.transform:
            image = self.transform(image)

        # Create target dictionary
        target = {
            "boxes": torch.as_tensor([bboxes], dtype=torch.float32),
            "labels": torch.randint(
                0, self.num_classes, (1,)
            ),  # Random class for the object
            "image_id": torch.tensor([idx]),
            "area": torch.tensor([(bboxes[2] - bboxes[0]) * (bboxes[3] - bboxes[1])]),
            "iscrowd": torch.tensor([0]),
            "keypoints": torch.as_tensor(keypoints, dtype=torch.float32),
            "heatmap": self.generate_heatmap(keypoints),
        }

        return image, target

    def generate_random_keypoints(self, num_feature_points, size):
        return [
            [np.random.randint(0, s) for s in size] + [1]
            for _ in range(num_feature_points)
        ]

    def get_bbox(self, keypoints):
        x_coords = [kp[0] for kp in keypoints]
        y_coords = [kp[1] for kp in keypoints]
        return [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]

    def generate_heatmap(self, keypoints, sigma=2):
        heatmaps = np.zeros(
            (len(keypoints), self.image_size[0], self.image_size[1]), dtype=np.float32
        )

        for i, (x, y, v) in enumerate(keypoints):
            if x > 0 and y > 0:  # valid keypoint

                xx, yy = np.meshgrid(
                    np.arange(self.image_size[1]), np.arange(self.image_size[0])
                )
                heatmaps[i] = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * sigma**2))

        return torch.tensor(heatmaps, dtype=torch.float32)
