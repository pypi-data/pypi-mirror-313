import os
import torch
import gc
from torch import optim
from torch.utils.data import DataLoader
from torch.cuda.amp import GradScaler, autocast
from tracebloc_package.model_file_checks.pytorch_checks import TorchChecks
from tracebloc_package.upload_model_classes.model_upload import Model
from tracebloc_package.utils.general_utils import (
    get_model_parameters,
    dummy_dataset_pytorch,
    collate_fn,
    get_cpu_gpu_estimate,
)
from tracebloc_package.utils.constants import (
    PRETRAINED_WEIGHTS_FILENAME,
    TRAINED_WEIGHTS_FILENAME,
    RCNN,
    HEATMAP,
)
from tracebloc_package.utils.constants import PYTORCH_FRAMEWORK


class TorchKeyPointDetector(Model, TorchChecks):

    def __init__(
        self,
        model_name,
        token,
        weights,
        url,
        model_path,
        tmp_model_file_path,
        tmp_dir_path,
        progress_bar_1,
        classes,
        weights_path,
        input_shape,
        model,
        category,
        progress_bar,
        message,
        framework,
        image_size,
        batch_size,
        model_type,
        num_feature_points,
    ):
        super().__init__(
            model_name=model_name,
            token=token,
            weights=weights,
            url=url,
            model_path=model_path,
            tmp_model_file_path=tmp_model_file_path,
            tmp_dir_path=tmp_dir_path,
            progress_bar_1=progress_bar_1,
            classes=classes,
            weights_path=weights_path,
            framework=framework,
            image_size=image_size,
            batch_size=batch_size,
            model_type=model_type,
            num_feature_points=num_feature_points,
        )
        TorchChecks.__init__(
            self,
            model=model,
            category=category,
            progress_bar=progress_bar,
            message=message,
            classes=classes,
        )
        self.__weights_path = weights_path
        self.tmp_file_path = ""
        self.input_shape = input_shape
        self.loss = None
        self.num_feature_points = num_feature_points

    def small_training_loop(self, weight_filename, custom_loss=False):
        try:
            # Define the number of fake images and other properties
            # Create fake image data
            train_dataset = dummy_dataset_pytorch(
                image_size=self.image_size,
                num_classes=self.classes,
                category=self.category,
                model_type=self.model_type,
                tmp_path=self.tmp_dir_path,
                num_feature_points=self.num_feature_points,
            )

            if self.model_type == RCNN:
                train_loader = DataLoader(
                    train_dataset,
                    batch_size=self.batch_size,
                    shuffle=True,
                    collate_fn=collate_fn,
                )
            else:
                train_loader = DataLoader(
                    train_dataset, batch_size=self.batch_size, shuffle=True
                )

            self.loss = self.configure_loss(
                custom_loss=custom_loss, category=self.category
            )

            output = self.keypoint_training(train_loader=train_loader)

            util_analysis_result = get_cpu_gpu_estimate(
                train_loader, output, self.model, self.batch_size, self.loss
            )
            if util_analysis_result is None:
                self.message = f"\nDecrease either image size or batch size to avoid over utilisation of resources"
                raise Exception(
                    f"\nDecrease either image size or batch size to avoid over utilisation of resources"
                )
            else:
                self.utilisation_category = util_analysis_result

            # dump weights from trained model will be used in averaging check
            get_model_parameters(
                model=self.model,
                weight_file_path=self.tmp_dir_path,
                weights_file_name=TRAINED_WEIGHTS_FILENAME,
                framework=PYTORCH_FRAMEWORK,
                preweights=False,
            )
            if self.progress_bar is not None:
                self.progress_bar.update(1)
        except Exception as e:  # pragma: no cover
            self.message = f"\nModel not support training on {self.category} dataset as there is error {e} "
            raise

    def keypoint_training(self, train_loader):
        optimizer = optim.SGD(self.model.parameters(), lr=0.001, momentum=0.9)
        scaler = GradScaler()

        try:
            total_loss = 0
            num_batches = 0
            self.model.train()

            for i, data in enumerate(train_loader, 0):
                optimizer.zero_grad()
                images, targets = data

                with autocast():  # Mixed precision context
                    if self.model_type == RCNN:
                        loss_dict = self.model(images, targets)
                        losses = sum(loss for loss in loss_dict.values())
                        outputs = targets
                    elif self.model_type == HEATMAP:
                        keypoints_targets = targets[
                            "heatmap"
                        ]  # Shape: (batch_size, num_feature_points, image_size)
                        outputs = self.model(images)
                        losses = self.loss(outputs, keypoints_targets)
                    else:
                        keypoints_targets = targets[
                            "keypoints"
                        ]  # Shape: (batch_size, num_feature_points, 3)
                        outputs = self.model(images)
                        losses = self.loss(outputs, keypoints_targets)

                scaler.scale(losses).backward()  # Scaled loss for mixed precision
                scaler.step(optimizer)
                scaler.update()

                total_loss += losses.item()
                num_batches += 1

                # Clear memory
                del images, targets, losses
                torch.cuda.empty_cache()
                gc.collect()
            return outputs

        except Exception as e:
            raise e

    def model_func_checks(self):
        # check if model is eligible
        try:
            self.is_model_supported()
            self.small_training_loop(TRAINED_WEIGHTS_FILENAME)
            # TODO: following weights are being saved at three different places; why? need to check
            # will need to be moved once clarified by the developer
            if os.path.exists(
                os.path.join(self.tmp_dir_path, f"{PRETRAINED_WEIGHTS_FILENAME}.pth")
            ):
                get_model_parameters(
                    model=self.model,
                    weight_file_path=self.tmp_dir_path,
                    weights_file_name=PRETRAINED_WEIGHTS_FILENAME,
                    framework=PYTORCH_FRAMEWORK,
                    preweights=True,
                )
                self.progress_bar.update(1)
            else:
                get_model_parameters(
                    model=self.model,
                    weight_file_path=self.tmp_dir_path,
                    weights_file_name=PRETRAINED_WEIGHTS_FILENAME,
                    framework=PYTORCH_FRAMEWORK,
                    preweights=False,
                )
                self.progress_bar.update(2)
            self.average_weights()
            self.load_averaged_weights()
            self.message = "all check passed"
            eligible = True
        except Exception as e:  # pragma: no cover
            self.message = f"\nModel checks failed with error:\n {e}"
            eligible = False
        if not eligible:
            return eligible, self.message, None, self.progress_bar  # pragma: no cover
        return eligible, self.message, self.model_name, self.progress_bar
