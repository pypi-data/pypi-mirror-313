import os
import torch
from torch.utils.data import DataLoader
from transformers import AdamW
from tracebloc_package.model_file_checks.pytorch_checks import TorchChecks
from tracebloc_package.upload_model_classes.model_upload import Model
from tracebloc_package.utils.general_utils import (
    get_model_parameters,
    define_device,
    print_error,
)
from tracebloc_package.utils.constants import (
    PRETRAINED_WEIGHTS_FILENAME,
    TRAINED_WEIGHTS_FILENAME,
)
from tracebloc_package.utils.constants import PYTORCH_FRAMEWORK
from tracebloc_package.utils.text_classification_utils import text_dummy_dataset


class TorchTextClassifier(Model, TorchChecks):

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
        model_id_llm,
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
        self.model_id_llm = model_id_llm
        self.device = define_device()
        self.loss = None

    def small_training_loop(self, weight_filename, custom_loss=False):
        try:
            # Create fake text data
            # TODO: check if model id is none
            train_dataset = text_dummy_dataset(
                model_id=(
                    "bert-base-uncased"
                    if self.model_id_llm is None or ""
                    else self.model_id_llm
                ),
                num_classes=self.classes,
                max_length=None if self.input_shape[0] == "" else self.input_shape[0],
            )

            train_loader = DataLoader(
                train_dataset, batch_size=self.batch_size, shuffle=True
            )
            # check if model has loss
            loss_availability = self.check_loss_availability(loader=train_loader)

            # if model doesn't have loss in forward function, configure loss
            # before training
            if not loss_availability or self.model_id_llm is None:
                # check if user has provided a correct input shape
                if self.input_shape[0] != 512:
                    print_error(
                        text="Input shape for Text classification should be 512",
                        color="red",
                    )
                    raise ValueError
                self.loss = self.configure_loss(
                    custom_loss=custom_loss, category=self.category
                )

            self.text_classification_training(
                train_loader=train_loader, loss_exists=loss_availability
            )

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

    def check_loss_availability(self, loader):
        # Check for loss computation capability
        try:
            # Perform a single forward pass to see if loss is computed
            sample_batch = next(iter(loader))
            inputs = {
                k: v.to(self.device) for k, v in sample_batch.items() if k != "labels"
            }
            labels = sample_batch["labels"].to(self.device)
            outputs = self.model(**inputs, labels=labels)
            if "loss" in outputs:
                print("Model is configured to compute loss.")
                loss_exists = True
            else:
                print("No loss computed in the model output.")
                loss_exists = False
        except Exception as e:
            loss_exists = False
        return loss_exists

    def text_classification_training(self, train_loader, loss_exists=True):
        # Optimizer
        optimizer = AdamW(self.model.parameters(), lr=5e-5)

        # Training loop
        self.model.to(self.device)
        self.model.train()
        for batch in train_loader:
            inputs = {k: v.to(self.device) for k, v in batch.items() if k != "labels"}
            labels = batch["labels"].to(self.device)
            if not loss_exists:
                # Determine the dtype of the model's parameters
                model_dtype = next(self.model.parameters()).dtype

                # Convert input data to the appropriate dtype based on the model's dtype
                if model_dtype == torch.float32 or model_dtype == torch.float64:
                    input_tensor = inputs.get("input_ids").float().to(self.device)
                elif model_dtype == torch.int32 or model_dtype == torch.int64:
                    input_tensor = inputs.get("input_ids").long().to(self.device)
                else:
                    raise ValueError("Unsupported model dtype")
                outputs = self.model(input_tensor)
                loss = self.loss(
                    outputs, labels
                )  # Use logits and labels to compute the loss
            else:
                outputs = self.model(**inputs, labels=labels)
                loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

    def model_func_checks(self):
        # check if model is eligible
        try:
            self.is_model_supported()
            self.small_training_loop(TRAINED_WEIGHTS_FILENAME)
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
