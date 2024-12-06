import gc
import os
import shutil
import sys

# hide warnings from tensorflow
import warnings

import json
import pickle
from collections import OrderedDict

import tensorflow as tf

import numpy as np
import requests
import rich
import torch
from termcolor import colored
from torch import nn
from tqdm import tqdm

from tracebloc_package.utils.general_utils import (
    validate_kwargs,
    get_model_params_count,
    print_error,
    remove_tmp_file,
    load_model,
    resize_weight_arrays,
)
from tracebloc_package.utils.constants import (
    TENSORFLOW_FRAMEWORK,
    PYTORCH_FRAMEWORK,
    SKLEARN_FRAMEWORK,
    IMAGE_CLASSIFICATION,
    OBJECT_DETECTION,
    TEXT_CLASSIFICATION,
    KEYPOINT_DETECTION,
)
from tracebloc_package.utils.constants import (
    MODEL_PARAMS_LIMIT,
    PRETRAINED_WEIGHTS_FILENAME,
    TRAINED_WEIGHTS_FILENAME,
    AVERAGED_WEIGHTS_PATH,
)

warnings.filterwarnings("ignore")


class Model:
    """ """

    def __init__(self, **kwargs):
        self.message = None
        validate_kwargs(
            kwargs,
            {
                "weights_path",
                "progress_bar_1",
                "model_path",
                "model_name",
                "classes",
                "token",
                "weights",
                "tmp_model_file_path",
                "tmp_dir_path",
                "url",
                "framework",
                "image_size",
                "batch_size",
                "model_type",
                "num_feature_points",
            },
        )
        self.weights_path = kwargs["weights_path"]
        self.progress_bar = kwargs["progress_bar_1"]
        self.__model_path = kwargs["model_path"]
        self.model_name = kwargs["model_name"]
        self.classes = kwargs["classes"]
        self.__token = kwargs["token"]
        self.weights = kwargs["weights"]
        self.tmp_model_file_path = kwargs["tmp_model_file_path"]
        self.tmp_dir_path = kwargs["tmp_dir_path"]
        self.framework = kwargs["framework"]
        self.__check_model_url = kwargs["url"] + "check-model/"
        self.image_size = kwargs["image_size"]
        self.batch_size = kwargs["batch_size"]
        self.model_type = kwargs["model_type"]
        self.num_feature_points = kwargs["num_feature_points"]
        self.average_weights_file_path = None
        self.received_model_name = None
        self.model_check_class = None
        self.progress_bar_2 = None
        self.model = None

    def uploaded_params(self):
        if self.received_model_name is not None:
            return (
                self.received_model_name,
                self.model_name,
                self.__model_path,
                self.framework,
                self.classes,
            )

    def validate_model_file(self):
        try:
            # check if model has supported parameters
            if self.framework != SKLEARN_FRAMEWORK:
                self.check_model_support()
            gc.collect()
        except Exception as e:
            print_error(
                text=f"\nUpload failed due to {e}",
                docs_print=True,
                docs="For more information check the [link=https://docs.tracebloc.io/user-uploadModel]docs["
                "/link]",
            )
            self.progress_bar.close()
            return None
        self.copy_weights_if_enabled()
        try:
            (
                status,
                self.message,
                model_name,
                progress_bar,
            ) = self.model_func_checks()
            if not status:
                remove_tmp_file(tmp_dir_path=self.tmp_dir_path)
                print_error(text=self.message)
                self.progress_bar.close()
                return None
            self.model = load_model(
                update_progress_bar=True,
                tmp_model_file_path=self.tmp_model_file_path,
                tmp_dir_path=self.tmp_dir_path,
                message=self.message,
                progress_bar=self.progress_bar,
            )
            remove_tmp_file(tmp_dir_path=self.tmp_dir_path)
            self.progress_bar.close()
            self.received_model_name = self.upload_model()
            self.progress_bar_2.close()
        except FileNotFoundError:
            print_error(
                text=f"\nUpload failed due to reason {self.message}",
                docs_print=True,
                docs="For more information check the [link=https://docs.tracebloc.io/user-uploadModel]docs[/link]",
            )
            self.progress_bar.close()
            return None
        except Exception as e:
            print_error(text=f"\nUpload failed.\n")
            if self.__url != "https://tracebloc.azurewebsites.net/":
                print(
                    f"Error in Upload is {e} at {sys.exc_info()[-1].tb_lineno} with message : {self.message}"
                )
            self.progress_bar.close()
            return None

    def upload_model(self):
        global model_weights
        try:
            self.progress_bar_2 = tqdm(total=1, desc="Model Upload Progress")
            model_file = open(self.__model_path, "rb")
            files = {"upload_file": model_file}
            if self.weights:
                weights_valid = self.check_weights()
                if not weights_valid:
                    return None
                model_weights = open(self.weights_path, "rb")
                files["upload_weights"] = model_weights
                values = {
                    "model_name": self.model_name,
                    "setWeights": True,
                    "type": "functional_test",
                }
            else:
                values = {
                    "model_name": self.model_name,
                    "setWeights": False,
                    "type": "functional_test",
                }
            # call check-model API to do functional test
            header = {"Authorization": f"Token {self.__token}"}
            r = requests.post(
                self.__check_model_url, headers=header, files=files, data=values
            )
            if self.weights:
                model_weights.close()
            model_file.close()
            body_unicode = r.content.decode("utf-8")
            content = json.loads(body_unicode)
            text = content["text"]
            check_status = content["check_status"]
            if not check_status:
                tex = colored(
                    text,
                    "red",
                )
                print(tex, "\n")
                return None
            self.progress_bar_2.update(1)
            return content["model_name"]
        except Exception as e:
            text = colored(
                f"\nUpload failed with message :{e}",
                "red",
            )
            print(text, "\n")
            self.progress_bar_2.close()

    def check_weights(self):
        # load model weights from current directory
        try:
            weights_file = open(self.weights_path, "rb")
        except FileNotFoundError:
            text = colored(
                f"Weights Upload failed. No weights file found with the name '{self.model_name}_weights.pkl'\n in "
                f"path '{os.getcwd()}'.",
                "red",
            )
            print(text, "\n")
            rich.print(
                "For more information check the [link=https://docs.tracebloc.io/user-uploadModel]docs[/link]"
            )
            return False
        # Load weights to check if it works
        try:
            if self.framework == TENSORFLOW_FRAMEWORK:
                we = pickle.load(weights_file)
                self.model.set_weights(we)
                weights_file.close()
                return True
            elif self.framework == PYTORCH_FRAMEWORK:
                try:
                    self.model.load_state_dict(torch.load(self.weights_path))
                    weights_file.close()
                    return True
                except Exception as e:
                    text = colored(
                        f"\nWeights upload failed with message: \n{e}",
                        "red",
                    )
                    print(text, "\n")

                    return False
            else:
                raise Exception("\nFramework not valid")
        except ValueError:
            weights_file.close()
            text = colored(
                "Weights upload failed. Provide weights compatible with the model provided.",
                "red",
            )
            print(text, "\n")
            print(
                "For more information check the docs 'https://docs.tracebloc.io/weights'"
            )
            return False, []
        except Exception as e:
            weights_file.close()
            text = colored(
                f"Weights upload failed with error: \n{e}",
                "red",
            )
            print(text, "\n")
            print(
                "For more information check the docs 'https://docs.tracebloc.io/weights'"
            )
            raise

    def model_func_checks(self):
        raise NotImplementedError(
            self.__class__.__name__ + "need to override this function"
        )

    def average_weights(self):
        weights = []
        new_weights = []

        # Set no_images_array dynamically based on the framework
        if self.framework == PYTORCH_FRAMEWORK:
            no_images_array = [100, 100]
        else:
            no_images_array = [20, 20]

        weights_file_path_1 = os.path.join(
            self.tmp_dir_path, f"{PRETRAINED_WEIGHTS_FILENAME}.pkl"
        )
        weights_file_path_2 = os.path.join(
            self.tmp_dir_path, f"{TRAINED_WEIGHTS_FILENAME}.pkl"
        )
        self.average_weights_file_path = os.path.join(
            self.tmp_dir_path, f"{AVERAGED_WEIGHTS_PATH}.pkl"
        )

        # Load weights from files
        try:
            with open(weights_file_path_1, "rb") as pkl_file, open(
                weights_file_path_2, "rb"
            ) as pkl_file2:
                weights.append(pickle.load(pkl_file))
                weights.append(pickle.load(pkl_file2))
        except Exception as e:
            raise

        # Average weights
        try:
            new_weights = [
                np.array(
                    [
                        np.average(np.array(w), weights=no_images_array, axis=0)
                        for w in zip(*resize_weight_arrays(weights_list_tuple))
                    ]
                )
                for weights_list_tuple in zip(*weights)
            ]
            del weights
            del no_images_array

        except Exception as e:
            raise

        # Save averaged weights
        try:
            with open(self.average_weights_file_path, "wb") as f:
                pickle.dump(new_weights, f)
            del new_weights
            self.progress_bar.update(1)
        except Exception as e:
            raise

    def load_averaged_weights(self):
        try:
            with open(self.average_weights_file_path, "rb") as f:
                parameters = pickle.load(f)

            if hasattr(self.model, "set_weights"):
                # Assuming TensorFlow model
                self.model.set_weights(parameters)

            elif hasattr(self.model, "load_state_dict"):
                # Assuming PyTorch model
                params_dict = zip(self.model.state_dict().keys(), parameters)
                state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
                self.model.load_state_dict(state_dict, strict=True)
                del params_dict
                del state_dict

            del parameters
            self.progress_bar.update(1)

        except Exception as e:
            raise e

    def check_model_support(self):
        # get model trainable parameters
        total_params = get_model_params_count(
            framework=self.framework, model=self.model
        )
        if total_params > MODEL_PARAMS_LIMIT:
            message = f"\nPlease provide model with trainable parameters less than {MODEL_PARAMS_LIMIT}"
            remove_tmp_file(tmp_dir_path=self.tmp_dir_path)
            print_error(text=message)
            self.progress_bar.close()
            return None

    def copy_weights_if_enabled(self):
        """
        Copy the weights file specified by the user if the 'weights' attribute is True.

        Raises:
            Exception: If copying the weights fails, prints an error message and returns None.
        """
        if not self.weights:
            return

        try:
            # Define the file extension based on the framework
            extension = ".pth" if self.framework == PYTORCH_FRAMEWORK else ".pkl"
            destination_path = os.path.join(
                self.tmp_model_file_path, PRETRAINED_WEIGHTS_FILENAME + extension
            )

            # Copy the weights file
            shutil.copy2(self.weights_path, destination_path)
        except Exception as e:
            print_error(
                text=f"\nUpload failed. There is no weights with the name '{self.model_name}' "
                f"in your folder '{os.getcwd()}'.",
                docs_print=True,
                docs="For more information check the [link=https://docs.tracebloc.io/user-uploadModel]docs[/link]",
            )
            self.progress_bar.close()
            return None

    def configure_loss(self, custom_loss=False, category=None):
        """
        Configures the model's loss function based on whether a custom loss or a specific category is specified.
        If `custom_loss` is True or the category indicates object detection, it attempts to import the Custom_loss
        class from a loss.py file in the temporary path. If the file doesn't exist, a FileNotFoundError is raised.
        If `custom_loss` is False and the category is image classification with PyTorch framework, it sets the loss
        to CrossEntropyLoss. Otherwise, it defaults to BinaryCrossentropy.

        Args:
            custom_loss (bool): Flag indicating whether to use a custom loss function.
            category (str): Category of the task, e.g., 'IMGCLASSIFICATION', 'OBDETECTION'.

        Raises:
            FileNotFoundError: If the loss.py file is missing and custom_loss or OBDETECTION category is specified.
            ImportError: If there is an issue importing the Custom_loss class.

        Returns:
            loss
        """
        if (
            category == IMAGE_CLASSIFICATION and self.framework == PYTORCH_FRAMEWORK
        ) or (category == TEXT_CLASSIFICATION and self.framework == PYTORCH_FRAMEWORK):
            return nn.CrossEntropyLoss()
        elif custom_loss or category == OBJECT_DETECTION:
            loss_file_path = os.path.join(self.tmp_dir_path, "loss.py")
            if not os.path.exists(loss_file_path):
                raise FileNotFoundError(
                    "loss.py file missing in the zip.\nPlease refer to the documentation for more information."
                )

            try:
                sys.path.append(self.tmp_model_file_path)
                from loss import Custom_loss

                loss = Custom_loss
                return loss
            except ImportError as e:
                raise ImportError(
                    f"Failed to import Custom_loss from {loss_file_path}. Error: {str(e)}"
                )
        elif category == KEYPOINT_DETECTION:
            return nn.MSELoss(reduction="sum")

        else:
            return tf.keras.losses.BinaryCrossentropy()
