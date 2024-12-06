import random

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms as transforms

device = torch.device("cpu")


def convert_cellboxes(predictions, S=7, C=3):
    """
    Converts bounding boxes output from Yolo with
    an image split size of S into entire image ratios
    rather than relative to cell ratios. Tried to do this
    vectorized, but this resulted in quite difficult to read
    code... Use as a black box? Or implement a more intuitive,
    using 2 for loops iterating range(S) and convert them one
    by one, resulting in a slower but more readable implementation.
    """

    predictions = predictions.to("cpu")
    batch_size = predictions.shape[0]
    predictions = predictions.reshape(batch_size, 7, 7, C + 10)
    bboxes1 = predictions[..., C + 1 : C + 5]
    bboxes2 = predictions[..., C + 6 : C + 10]
    scores = torch.cat(
        (predictions[..., C].unsqueeze(0), predictions[..., C + 5].unsqueeze(0)), dim=0
    )
    best_box = scores.argmax(0).unsqueeze(-1)
    best_boxes = bboxes1 * (1 - best_box) + best_box * bboxes2
    cell_indices = torch.arange(7).repeat(batch_size, 7, 1).unsqueeze(-1)
    x = 1 / S * (best_boxes[..., :1] + cell_indices)
    y = 1 / S * (best_boxes[..., 1:2] + cell_indices.permute(0, 2, 1, 3))
    w_y = 1 / S * best_boxes[..., 2:4]
    converted_bboxes = torch.cat((x, y, w_y), dim=-1)
    predicted_class = predictions[..., :C].argmax(-1).unsqueeze(-1)
    best_confidence = torch.max(predictions[..., C], predictions[..., C + 5]).unsqueeze(
        -1
    )
    converted_preds = torch.cat(
        (predicted_class, best_confidence, converted_bboxes), dim=-1
    )

    return converted_preds


def cellboxes_to_boxes(out, S=7, C=4):
    converted_pred = convert_cellboxes(out, C=C).reshape(out.shape[0], S * S, -1)
    converted_pred[..., 0] = converted_pred[..., 0].long()
    all_bboxes = []

    for ex_idx in range(out.shape[0]):
        bboxes = []

        for bbox_idx in range(S * S):
            bboxes.append([x.item() for x in converted_pred[ex_idx, bbox_idx, :]])
        all_bboxes.append(bboxes)

    return all_bboxes


def intersection_over_union(boxes_preds, boxes_labels, box_format="midpoint"):
    """
    Calculates intersection over union

    Parameters:
        boxes_preds (tensor): Predictions of Bounding Boxes (BATCH_SIZE, 4)
        boxes_labels (tensor): Correct labels of Bounding Boxes (BATCH_SIZE, 4)
        box_format (str): midpoint/corners, if boxes are (x,y,w,h) or (x1,y1,x2,y2) respectively.

    Returns:
        tensor: Intersection over union for all examples
    """
    # boxes_preds shape is (N, 4) where N is the number of bboxes
    # boxes_labels shape is (n, 4)

    if box_format == "midpoint":
        box1_x1 = boxes_preds[..., 0:1] - boxes_preds[..., 2:3] / 2
        box1_y1 = boxes_preds[..., 1:2] - boxes_preds[..., 3:4] / 2
        box1_x2 = boxes_preds[..., 0:1] + boxes_preds[..., 2:3] / 2
        box1_y2 = boxes_preds[..., 1:2] + boxes_preds[..., 3:4] / 2
        box2_x1 = boxes_labels[..., 0:1] - boxes_labels[..., 2:3] / 2
        box2_y1 = boxes_labels[..., 1:2] - boxes_labels[..., 3:4] / 2
        box2_x2 = boxes_labels[..., 0:1] + boxes_labels[..., 2:3] / 2
        box2_y2 = boxes_labels[..., 1:2] + boxes_labels[..., 3:4] / 2

    if box_format == "corners":
        box1_x1 = boxes_preds[..., 0:1]
        box1_y1 = boxes_preds[..., 1:2]
        box1_x2 = boxes_preds[..., 2:3]
        box1_y2 = boxes_preds[
            ..., 3:4
        ]  # Output tensor should be (N, 1). If we only use 3, we go to (N)
        box2_x1 = boxes_labels[..., 0:1]
        box2_y1 = boxes_labels[..., 1:2]
        box2_x2 = boxes_labels[..., 2:3]
        box2_y2 = boxes_labels[..., 3:4]

    x1 = torch.max(box1_x1, box2_x1)
    y1 = torch.max(box1_y1, box2_y1)
    x2 = torch.min(box1_x2, box2_x2)
    y2 = torch.min(box1_y2, box2_y2)

    # .clamp(0) is for the case when they don't intersect. Since when they don't intersect, one of these will be
    # negative so that should become 0
    intersection = (x2 - x1).clamp(0) * (y2 - y1).clamp(0)

    box1_area = abs((box1_x2 - box1_x1) * (box1_y2 - box1_y1))
    box2_area = abs((box2_x2 - box2_x1) * (box2_y2 - box2_y1))

    return intersection / (box1_area + box2_area - intersection + 1e-6)


def non_max_suppression(bboxes, iou_threshold, threshold, box_format="corners"):
    """
    Does Non Max Suppression given bboxes
    Parameters:
        bboxes (list): list of lists containing all bboxes with each bboxes
        specified as [class_pred, prob_score, x1, y1, x2, y2]
        iou_threshold (float): threshold where predicted bboxes is correct
        threshold (float): threshold to remove predicted bboxes (independent of IoU)
        box_format (str): "midpoint" or "corners" used to specify bboxes
    Returns:
        list: bboxes after performing NMS given a specific IoU threshold
    """

    assert type(bboxes) == list

    bboxes = [box for box in bboxes if box[1] > threshold]
    bboxes = sorted(bboxes, key=lambda x: x[1], reverse=True)
    bboxes_after_nms = []

    while bboxes:
        chosen_box = bboxes.pop(0)

        bboxes = [
            box
            for box in bboxes
            if box[0] != chosen_box[0]
            or intersection_over_union(
                torch.tensor(chosen_box[2:]),
                torch.tensor(box[2:]),
                box_format=box_format,
            )
            < iou_threshold
        ]

        bboxes_after_nms.append(chosen_box)

    return bboxes_after_nms


def get_bboxes(
    loader,
    model,
    iou_threshold,
    threshold,
    pred_format="cells",
    box_format="midpoint",
    device=device,
    C=4,
):
    all_pred_boxes = []
    all_true_boxes = []
    bboxes = None

    # make sure model is in eval before get bboxes
    model.eval()
    train_idx = 0

    for batch_idx, (x, labels) in enumerate(loader):
        x = x.to(device)
        labels = labels.to(device)

        predictions = model(x)

        batch_size = x.shape[0]
        true_bboxes = cellboxes_to_boxes(labels, C=C)
        bboxes = cellboxes_to_boxes(predictions, C=C)

        for idx in range(batch_size):
            nms_boxes = non_max_suppression(
                bboxes[idx],
                iou_threshold=iou_threshold,
                threshold=threshold,
                box_format=box_format,
            )

            # if batch_idx == 0 and idx == 0:
            #    plot_image(x[idx].permute(1,2,0).to("cpu"), nms_boxes)
            #    print(nms_boxes)

            for nms_box in nms_boxes:
                all_pred_boxes.append([train_idx] + nms_box)

            for box in true_bboxes[idx]:
                # many will get converted to 0 pred
                if box[1] > threshold:
                    all_true_boxes.append([train_idx] + box)

            train_idx += 1

    model.train()
    return all_pred_boxes, all_true_boxes, bboxes[0]


class FakeObjectDetectionDataset(Dataset):
    def __init__(self, num_samples, num_classes=None, image_shape=(256, 256)):
        self.num_samples = num_samples
        self.num_classes = num_classes if num_classes else random.randint(1, 10)
        self.classes = [self._generate_class_name() for _ in range(self.num_classes)]
        self.image_shape = image_shape
        self.data = self._generate_fake_data()

    def _generate_class_name(self):
        # Generate a random class name
        return "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(5))

    def _generate_fake_data(self):
        data = []
        for _ in range(self.num_samples):
            image = torch.rand((3, *self.image_shape))  # Fake image data
            num_objects = random.randint(1, 5)
            labels = [
                random.randint(0, self.num_classes - 1) for _ in range(num_objects)
            ]
            boxes = [
                (random.random(), random.random(), random.random(), random.random())
                for _ in range(num_objects)
            ]
            target = {"boxes": boxes, "labels": labels}
            data.append((image, target))
        return data

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        return self.data[idx]

    def __iter__(self):
        return iter(self.data)

    def get_classes(self):
        return self.classes


def create_yolo_dataset(dataset, classes, image_shape, S, B):
    try:
        yolo_dataset = []
        C = len(classes)
        class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
        for img, target in dataset:
            try:
                # Extract bounding boxes and labels
                bboxes = target["boxes"]
                if not isinstance(bboxes, list):
                    d_box = [bboxes]
                else:
                    d_box = bboxes

                # boxes = [[float(obj["bndbox"]["xmin"]), float(obj["bndbox"]["ymin"]),
                #           float(obj["bndbox"]["xmax"]), float(obj["bndbox"]["ymax"])]
                #          for obj in d_box]

                labels = target["labels"]

                # Resize image
                img = transforms.ToPILImage()(img)
                # image = Image.open(img).convert("RGB")
                image = img.resize(image_shape)
                image = transforms.ToTensor()(image)

                # YOLO format: [label, x_center, y_center, width, height]
                image_info = {"path": image, "boxes": []}
                for box, label in zip(bboxes, labels):
                    x_center = ((box[0] + box[2]) / 2) / image_shape[0]
                    y_center = ((box[1] + box[3]) / 2) / image_shape[1]
                    width = (box[2] - box[0]) / image_shape[0]
                    height = (box[3] - box[1]) / image_shape[1]
                    yolo_box = [label, x_center, y_center, width, height]
                    image_info["boxes"].append(yolo_box)

                # yolo_dataset.append(image_info)
                image_info["boxes"] = torch.as_tensor(
                    image_info["boxes"], dtype=torch.float32
                )

                S = S
                B = B
                # Convert To Cells
                label_matrix = torch.zeros((S, S, C + 5 * B))
                for box in image_info["boxes"]:
                    class_label, x, y, width, height = box.tolist()
                    class_label = int(class_label)

                    # i,j represents the cell row and cell column
                    i, j = int(S * y), int(S * x)
                    x_cell, y_cell = S * x - j, S * y - i

                    """
                    Calculating the width and height of cell of bounding box,
                    relative to the cell is done by the following, with
                    width as the example:
        
                    width_pixels = (width*self.image_width)
                    cell_pixels = (self.image_width)
        
                    Then to find the width relative to the cell is simply:
                    width_pixels/cell_pixels, simplification leads to the
                    formulas below.
                    """
                    width_cell, height_cell = (
                        width * S,
                        height * S,
                    )

                    # If no object already found for specific cell i,j
                    # Note: This means we restrict to ONE object
                    # per cell!
                    #             print(i, j)
                    if label_matrix[i, j, C] == 0:
                        # Set that there exists an object
                        label_matrix[i, j, C] = 1

                        # Box coordinates
                        box_coordinates = torch.tensor(
                            [x_cell, y_cell, width_cell, height_cell]
                        )

                        label_matrix[i, j, 4:8] = box_coordinates

                        # Set one hot encoding for class_label
                        label_matrix[i, j, class_label] = 1
            except:
                continue
            data_yolo = [image_info["path"], label_matrix]
            yolo_dataset.append(data_yolo)

        return yolo_dataset
    except Exception as e:
        raise e


def create_fasterrcnn_dataset(dataset, classes, image_shape):
    fasterrcnn_dataset = []
    for img, target in dataset:
        # Extract bounding boxes and labels
        boxes = target["annotation"]["object"]
        if not isinstance(boxes, list):
            boxes = [boxes]

        boxes = [
            [
                float(obj["bndbox"]["xmin"]),
                float(obj["bndbox"]["ymin"]),
                float(obj["bndbox"]["xmax"]),
                float(obj["bndbox"]["ymax"]),
            ]
            for obj in boxes
        ]

        labels = [classes.index(obj["name"]) for obj in boxes]

        # Resize image
        image = Image.open(img).convert("RGB")
        image = image.resize(image_shape)

        # Faster R-CNN format: {"boxes": [[x1, y1, x2, y2], ...], "labels": [label1, ...]}
        image_info = {"path": image, "boxes": boxes, "labels": labels}
        fasterrcnn_dataset.append(image_info)

    return fasterrcnn_dataset
