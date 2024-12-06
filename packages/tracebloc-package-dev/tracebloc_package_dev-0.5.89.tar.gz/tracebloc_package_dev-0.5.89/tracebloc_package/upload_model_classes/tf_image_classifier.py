import os

import tensorflow as tf
from tracebloc_package.model_file_checks.tensorflow_checks import TensorflowChecks
from tracebloc_package.upload_model_classes.model_upload import Model
from tracebloc_package.utils.general_utils import (
    dummy_dataset_tensorflow,
    get_model_parameters,
)
from tracebloc_package.utils.constants import (
    PRETRAINED_WEIGHTS_FILENAME,
    TRAINED_WEIGHTS_FILENAME,
)
from tracebloc_package.utils.constants import TENSORFLOW_FRAMEWORK


class TfImageClassifier(Model, TensorflowChecks):

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
        TensorflowChecks.__init__(
            self,
            model=model,
            category=category,
            progress_bar=progress_bar,
            message=message,
        )
        self.input_shape = input_shape
        self.loss = None

    def small_training_loop(self, weight_filename, custom_loss=False):
        try:
            self.loss = self.configure_loss(custom_loss=custom_loss)
            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(),
                loss=self.loss,
            )
            # mock dataset for small training
            training_dataset = dummy_dataset_tensorflow(
                input_shape=self.input_shape,
                num_classes=self.classes,
                num_examples=20,
                category=self.category,
            )
            self.model.fit(training_dataset, epochs=1, verbose=0)
            # dump weights from trained model will be used in averaging check
            get_model_parameters(
                model=self.model,
                weight_file_path=self.tmp_dir_path,
                weights_file_name=TRAINED_WEIGHTS_FILENAME,
                framework=TENSORFLOW_FRAMEWORK,
                preweights=False,
            )
            if self.progress_bar is not None:
                self.progress_bar.update(1)
        except Exception as e:  # pragma: no cover
            self.message = f"\nModel not support training on {self.category} dataset."
            raise

    def model_func_checks(self):
        try:
            self.is_model_supported()
            self.check_original_model_channels()
            self.layer_instance_check()
            self.small_training_loop(TRAINED_WEIGHTS_FILENAME)
            if not os.path.exists(
                os.path.join(self.tmp_dir_path, f"{PRETRAINED_WEIGHTS_FILENAME}.pkl")
            ):
                get_model_parameters(
                    model=self.model,
                    weight_file_path=self.tmp_dir_path,
                    weights_file_name=PRETRAINED_WEIGHTS_FILENAME,
                    framework=TENSORFLOW_FRAMEWORK,
                    preweights=False,
                )
                self.progress_bar.update(1)
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
