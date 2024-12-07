import os

import torch
from torch import optim
from torch.utils.data import DataLoader

from tracebloc_package.model_file_checks.pytorch_checks import TorchChecks
from tracebloc_package.upload_model_classes.model_upload import Model
from tracebloc_package.utils.general_utils import (
    get_model_parameters,
    dummy_dataset_pytorch,
)
from tracebloc_package.utils.constants import (
    PRETRAINED_WEIGHTS_FILENAME,
    TRAINED_WEIGHTS_FILENAME,
)
from tracebloc_package.utils.constants import PYTORCH_FRAMEWORK


class TorchImageClassifier(Model, TorchChecks):

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
            )

            train_loader = DataLoader(
                train_dataset, batch_size=self.batch_size, shuffle=True
            )

            self.loss = self.configure_loss(
                custom_loss=custom_loss, category=self.category
            )

            self.classification_training(train_loader=train_loader)

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

    def classification_training(self, train_loader):
        optimizer = optim.SGD(self.model.parameters(), lr=0.001, momentum=0.9)
        for epoch in range(1):  # loop over the dataset multiple times
            running_loss = 0.0
            for i, data in enumerate(train_loader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data
                labels = torch.tensor(labels, dtype=torch.long)
                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = self.model(inputs)
                loss = self.loss(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.item()

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
