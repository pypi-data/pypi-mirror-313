import shutil
from torch import optim
import psutil
import tensorflow as tf
import torch
import rich
import torchvision.transforms as transforms
import sys
from functools import wraps
from termcolor import colored
import numpy as np
import torchvision.datasets as datasets
from importlib.machinery import SourceFileLoader
import base64
import os
import ast
import pickle
import pickletools

from tracebloc_package.utils.constants import (
    KEYPOINT_DETECTION,
    YOLO,
    PRETRAINED_WEIGHTS_FILENAME,
    IMAGE_CLASSIFICATION,
    PYTORCH_FRAMEWORK,
    OBJECT_DETECTION,
    TENSORFLOW_FRAMEWORK,
    SKLEARN_FRAMEWORK,
)
from tracebloc_package.utils.detection_utils import (
    FakeObjectDetectionDataset,
    create_yolo_dataset,
    create_fasterrcnn_dataset,
)

from tracebloc_package.utils.key_point_detection_utils import (
    FakeKeypointDetectionDataset,
)


def define_device():
    """Define the device to be used by PyTorch"""

    # Get the PyTorch version
    torch_version = torch.__version__

    # Print the PyTorch version
    print(f"PyTorch version: {torch_version}", end=" -- ")

    # Check if MPS (Multi-Process Service) device is available on MacOS
    defined_device = torch.device("cpu")
    # Print a message indicating the selected device
    print(f"using {defined_device}")

    # Return the defined device
    return defined_device


def check_MyModel(filename, path):
    try:
        # check if file contains the MyModel function
        model = SourceFileLoader(filename, f"{path}").load_module()
        model.MyModel(input_shape=(500, 500, 3), classes=10)
        return True, model

    except AttributeError:
        return (
            False,
            "Model file not provided as per docs: No function with name MyModel",
        )
    except TypeError:
        return (
            False,
            "Model file not provided as per docs: MyModel function receives no arguments",
        )
    except ValueError:
        return False, "Layers shape is not compatible with model input shape"


def is_model_supported(model_obj):
    tensorflow_supported_apis = (tf.keras.models.Sequential, tf.keras.Model)
    supported = isinstance(model_obj, tensorflow_supported_apis)
    if supported:
        # check if it of subclassing
        try:
            # Note that the `input_shape` property is only available for Functional and Sequential models.
            input_shape = model_obj.input_shape
            return True
        except AttributeError:
            return False


# function to check if layers used in tensorflow are supported
def layer_instance_check(model):
    model_layers = model.layers
    for layer in model_layers:
        if not isinstance(layer, tf.keras.layers.Layer):
            return False, []
    return True, model_layers


def is_valid_method(text):
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        return False
    return True


def get_base64_encoded_code(code):
    if not is_valid_method(code):
        raise ValueError("Input is not a valid Python method")
    code_bytes = code.encode("utf-8")
    return base64.b64encode(code_bytes).decode("utf-8")


def getImagesCount(images_count):
    count = 0
    for key in images_count.keys():
        count += images_count[key]
    return count


def dummy_dataset_tensorflow(
    input_shape,
    num_classes,
    batch_size=8,
    num_examples=1000,
    category=IMAGE_CLASSIFICATION,
):
    if category == IMAGE_CLASSIFICATION:
        # Create random images
        images = np.random.randint(0, 256, size=(num_examples,) + input_shape).astype(
            np.uint8
        )
        # Create random labels
        labels = np.random.randint(0, num_classes, size=(num_examples,))
        # One-hot encode the labels
        labels = tf.keras.utils.to_categorical(labels, num_classes=num_classes)

        # Convert to TensorFlow datasets
        ds = tf.data.Dataset.from_tensor_slices((images, labels))

        return ds.batch(batch_size)
    else:
        return None


def dummy_dataset_pytorch(
    image_size,
    num_classes=2,
    num_images=50,
    num_channels=3,
    category=IMAGE_CLASSIFICATION,
    model_type="",
    tmp_path="",
    num_feature_points=None,
):
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
        ]
    )

    if category == IMAGE_CLASSIFICATION:
        image_shape = (num_channels, image_size, image_size)
        train_dataset = datasets.FakeData(
            size=num_images,
            image_size=image_shape,
            num_classes=num_classes,
            transform=transform,
        )
        return train_dataset

    elif category == OBJECT_DETECTION:
        image_shape = (448, 448)

        fake_dataset = FakeObjectDetectionDataset(
            num_classes=num_classes, num_samples=10
        )
        classes = fake_dataset.get_classes()
        if model_type == YOLO:
            train_dataset = create_yolo_dataset(
                dataset=fake_dataset, classes=classes, image_shape=image_shape, S=7, B=2
            )
            return train_dataset

        else:
            train_dataset = create_fasterrcnn_dataset(
                dataset=fake_dataset, classes=classes, image_shape=image_shape
            )
            return train_dataset
    elif category == KEYPOINT_DETECTION:
        if type(image_size) is int:
            image_shape = (image_size, image_size)
        else:
            image_shape = image_size

        fake_dataset = FakeKeypointDetectionDataset(
            image_size=image_shape,
            num_images=10,
            num_classes=num_classes,
            transform=transform,
            num_feature_points=num_feature_points,
        )
        return fake_dataset


# Function to create YOLO-compatible dataset


# Function to create Faster R-CNN-compatible dataset


def get_model_parameters(**kwargs) -> None:
    model = kwargs["model"]
    framework = kwargs["framework"]

    if framework == PYTORCH_FRAMEWORK:
        if not kwargs["preweights"]:
            parameters = [val.cpu().numpy() for _, val in model.state_dict().items()]
        else:
            model.load_state_dict(
                torch.load(
                    PRETRAINED_WEIGHTS_FILENAME, map_location=torch.device("cpu")
                )
            )
            parameters = [val.cpu().numpy() for _, val in model.state_dict().items()]
    elif framework == TENSORFLOW_FRAMEWORK:
        parameters = model.get_weights()
    else:
        parameters = None

    weight_file_path = kwargs["weight_file_path"]
    weights_file_name = kwargs["weights_file_name"]

    if parameters:
        with open(
            os.path.join(weight_file_path, f"{weights_file_name}.pkl"), "wb"
        ) as f:
            pickled = pickle.dumps(parameters)
            optimized_pickle = pickletools.optimize(pickled)
            f.write(optimized_pickle)
    else:
        with open(
            os.path.join(weight_file_path, f"{weights_file_name}.pkl"), "wb"
        ) as f:
            pickle.dump(model, f)

    del parameters


def validate_kwargs(
    kwargs, allowed_kwargs, error_message="Keyword argument not understood:"
):
    """Checks that all keyword arguments are in the set of allowed keys."""
    for kwarg in kwargs:
        if kwarg not in allowed_kwargs:
            raise TypeError(error_message, kwarg)


def get_model_params_count(framework="tensorflow", model=None) -> int:
    """
    calculate total trainable parameters of a given model
    """
    if framework == TENSORFLOW_FRAMEWORK:
        return model.count_params()
    elif framework == SKLEARN_FRAMEWORK:
        # Count parameters for sklearn models
        if hasattr(model, "coef_") and model.coef_ is not None:
            coef_count = model.coef_.size  # Number of elements in coef_
            intercept_count = (
                model.intercept_.size if hasattr(model, "intercept_") else 0
            )
            return coef_count + intercept_count
        elif hasattr(model, "tree_"):  # For tree-based models
            tree = model.tree_
            return tree.capacity  # Number of nodes in the tree
        elif hasattr(model, "estimators_"):  # For ensemble models
            return sum(
                get_model_params_count(framework="sklearn", model=est)
                for est in model.estimators_
            )
        else:
            return 400
    else:
        return sum(p.numel() for p in model.parameters() if p.requires_grad)


def get_paths(**kwargs):
    """
    take path provided by user as modelname
    updates model path, weights path and model name
    """
    validate_kwargs(kwargs=kwargs, allowed_kwargs={"path"})

    # define useful variables
    extension = ".py"
    model_file_path = kwargs["path"]
    weights_file_path = None
    model_name = None

    # check if user provided a filename
    if "/" not in model_file_path:
        model_file_path = "./" + model_file_path
    # check if user provided path with .py extension
    root, ext = os.path.splitext(model_file_path)
    if ext:
        if ext != extension:
            extension = ".zip"

        # get weights path --> remove .py from the given path and add _weights.pkl after it
        if os.path.exists(model_file_path.rsplit(".", 1)[0] + "_weights.pkl"):
            weights_file_path = model_file_path.rsplit(".", 1)[0] + "_weights.pkl"
        else:
            weights_file_path = model_file_path.rsplit(".", 1)[0] + "_weights.pth"
        # get model name --> get model name from given path
        model_name = model_file_path.rsplit(".", 1)[0].split("/")[-1]
    else:
        # get models path --> add .py at the end of given path
        if os.path.exists(model_file_path + ".zip"):
            extension = ".zip"
        model_file_path = model_file_path + extension
        # get weights path --> add _weights.pkl after given path
        if os.path.exists(model_file_path + "_weights.pkl"):
            weights_file_path = model_file_path + "_weights.pkl"
        else:
            weights_file_path = model_file_path + "_weights.pth"
        # get model name --> get filename from given path
        model_name = model_file_path.split("/")[-1]
    return model_name, model_file_path, weights_file_path, extension


def env_url(environment="production"):
    url = None
    if environment == "local":
        url = "http://127.0.0.1:8000/"
    elif environment == "development":
        url = "https://dev-api.tracebloc.io/"
    elif environment == "ds":
        url = "https://xray-backend.azurewebsites.net/"
    elif environment == "staging":
        url = "https://stg-api.tracebloc.io"
    elif environment == "" or environment == "production":
        url = "https://tracebloc.azurewebsites.net/"
    return url


def require_login(func):
    """
    Decorator can be used for User class to check if user has logged in.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if (
            getattr(self, "_User__token", "") == ""
            or getattr(self, "_User__token") is None
        ):
            text = colored(
                "You are not logged in. Please go back to ‘1. Connect to Tracebloc’ and proceed with logging in.",
                "red",
            )
            print(text, "\n")
            return
        return func(self, *args, **kwargs)

    return wrapper


def print_error(text, color="red", docs_print=False, **kwargs):
    text = colored(text=text, color=color)
    print(text, "\n")
    if docs_print:
        rich.print(kwargs["docs"])


def resize_weight_arrays(weights_list_tuple):
    # Find the maximum shape among all weight arrays in the tuple
    max_shape = np.array(max(w.shape for w in weights_list_tuple))

    # Broadcast each weight array to the maximum shape
    resized_weights_list = []
    for w in weights_list_tuple:
        if w.shape == ():
            # Convert 0-dimensional array to 1-dimensional array
            broadcasted_w = np.broadcast_to(w, (1,))
        else:
            broadcasted_w = np.broadcast_to(w, max_shape)
        resized_weights_list.append(broadcasted_w)

    return resized_weights_list


def load_model(filename="", update_progress_bar=False, **kwargs):
    tmp_model_file_path = kwargs["tmp_model_file_path"]
    tmp_dir_path = kwargs["tmp_dir_path"]
    if update_progress_bar:
        progress_bar = kwargs["progress_bar"]
    message = kwargs["message"]
    try:
        sys.path.append(tmp_dir_path)
        loaded_model = SourceFileLoader(
            f"{filename}", f"{tmp_model_file_path}"
        ).load_module()
        model = loaded_model.MyModel()
        if update_progress_bar:
            progress_bar.update(1)
        return model
    except Exception as e:
        if message == "":
            message = f"Error loading the model file, {str(e)}"
        raise


def remove_tmp_file(tmp_dir_path, update_progress_bar=False, progress_bar=None):
    """
    remove temporary model file
    """
    if os.path.exists(tmp_dir_path):  # pragma: no cover
        shutil.rmtree(tmp_dir_path)
    if update_progress_bar:
        progress_bar.update(1)


def collate_fn(batch):
    """
    Custom collate function for handling varying sizes of tensors and different numbers of objects
    in images during data loading.

    Args:
        batch (list): A batch of data.

    Returns:
        Tuple: Collated batch of data.
    """
    return tuple(zip(*batch))


def get_cpu_gpu_estimate(
    input_data, output_data, model, batchsize, loss, take_gpu_est=True
):
    estimated_cpu_memory = estimate_cpu_memory(batchsize)

    total_input_bytes = get_dataset_size(input_data, batchsize)
    total_output_bytes = get_output_size(output_data, batchsize)
    total_model_params = get_model_memory_usage(model, loss)
    total_bytes_count = total_input_bytes + total_output_bytes + total_model_params

    if take_gpu_est:
        data_parallel_factor = (
            1  # Increase if using data parallelism, e.g., 2 for two GPUs
        )
        precision_factor = (
            0.5  # Adjust if changing precision, e.g., 0.5 if using float16 on GPU
        )
        optimizer_memory_factor = 3
        estimated_gpu_memory = int(
            estimated_cpu_memory
            * data_parallel_factor
            * precision_factor
            * optimizer_memory_factor
        )
    else:
        estimated_gpu_memory = 0

    if check_limit(total_bytes_count):
        return categorize_utilization(
            total_bytes_count, estimated_cpu_memory, estimated_gpu_memory
        )
    else:
        return None


def categorize_utilization(total_memory, cpu_memory, gpu_memory):
    """
    Categorizes memory utilization as 'High' or 'Low' based on predefined thresholds.

    Parameters:
        total_memory (float): The total memory usage in bytes.
        cpu_memory (float): The estimated CPU memory usage in bytes.
        gpu_memory (float): The estimated GPU memory usage in bytes.

    Returns:
        dict: A dictionary with categories for 'total', 'cpu', and 'gpu'.
    """
    thresholds = {
        "total": 603590000,  # 773.59 million bytes for total memory
        "cpu": 90637600000,  # 110.64 billion bytes for CPU memory
        "gpu": 165956400000,  # 165.96 billion bytes for GPU memory
    }
    categories = {
        "total": 1 if total_memory > thresholds["total"] else 0,
        "cpu": 1 if cpu_memory > thresholds["cpu"] else 0,
        "gpu": 1 if gpu_memory > thresholds["gpu"] else 0,
    }

    # Count how many are 'High'
    high_count = sum(category for category in categories.values())

    # Determine overall category based on the majority
    overall_util_category = "high" if high_count >= 1 else "low"
    return overall_util_category


def get_dataset_size(data_loader, batchsize):
    total_size = 0
    # Iterate through all the batches in the data loader
    for batch in data_loader:
        # Handle complex batch structures such as dictionaries or tuples of tensors
        total_size += recurse_through_structure(batch)
    if batchsize > 10:
        total_size = int(total_size * (batchsize / 10))
    return total_size


def recurse_through_structure(element):
    size = 0
    if isinstance(element, dict):
        for value in element.values():
            size += recurse_through_structure(value)
    elif isinstance(element, (list, tuple)):
        for item in element:
            size += recurse_through_structure(item)
    elif torch.is_tensor(element):
        size += element.nelement() * element.element_size()
    return size


def get_output_size(outputs, batchsize):
    total_size = 0
    for output in outputs:  # outputs might be a list of dictionaries
        total_size += recurse_through_structure(output)
    if batchsize > 10:
        total_size = int(total_size * (batchsize / 10))
    return total_size


def get_model_memory_usage(model, loss):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    # Memory usage of model parameters
    total_param_size = sum(p.numel() * p.element_size() for p in model.parameters())

    # Memory usage of optimizer states
    total_optim_size = 0
    if optimizer is not None:
        for state in optimizer.state.values():
            for k, v in state.items():
                if torch.is_tensor(v):
                    total_optim_size += v.numel() * v.element_size()

    # Additional memory used by custom loss function (if applicable)
    total_loss_size = 0
    if loss is not None and hasattr(loss, "parameters"):
        total_loss_size = sum(p.numel() * p.element_size() for p in loss.parameters())

    total_memory_bytes = total_param_size + total_optim_size + total_loss_size
    return total_memory_bytes


def estimate_cpu_memory(batchsize):
    scale_factor = int(batchsize / 10)
    # Get the current process
    process = psutil.Process(os.getpid())
    # Get memory usage in bytes
    memory_info = process.memory_info()
    memory_used = memory_info.rss
    max_memory_util = memory_used * scale_factor
    return max_memory_util


def check_limit(total_memory):

    # Define the memory threshold (2 GB in bytes)
    memory_threshold = 2000000000

    # Check if the total memory usage exceeds the threshold
    if total_memory > memory_threshold:
        return False

    return True
