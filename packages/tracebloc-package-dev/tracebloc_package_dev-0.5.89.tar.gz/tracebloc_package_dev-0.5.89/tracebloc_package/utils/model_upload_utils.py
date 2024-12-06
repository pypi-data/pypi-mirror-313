from tracebloc_package.upload_model_classes.torch_generic_classifier import (
    TorchGenericClassifier,
)
from tracebloc_package.upload_model_classes.torch_key_point_detector import (
    TorchKeyPointDetector,
)
from tracebloc_package.upload_model_classes.torch_object_detector import (
    TorchObjectDetector,
)
from tracebloc_package.upload_model_classes.torch_text_classifier import (
    TorchTextClassifier,
)
from tracebloc_package.utils.constants import (
    KEYPOINT_DETECTION,
    TEXT_CLASSIFICATION,
    GENERIC_CLASSIFICATION,
)
from tracebloc_package.utils.constants import (
    TENSORFLOW_FRAMEWORK,
    PYTORCH_FRAMEWORK,
    IMAGE_CLASSIFICATION,
    OBJECT_DETECTION,
    SKLEARN_FRAMEWORK,
)
from tracebloc_package.upload_model_classes.tf_image_classifier import TfImageClassifier
from tracebloc_package.upload_model_classes.skl_generic_classifier import (
    SKLGenericClassifier,
)
from tracebloc_package.upload_model_classes.torch_image_classifier import (
    TorchImageClassifier,
)

task_classes_dict = {
    (IMAGE_CLASSIFICATION, TENSORFLOW_FRAMEWORK): TfImageClassifier,
    (IMAGE_CLASSIFICATION, PYTORCH_FRAMEWORK): TorchImageClassifier,
    (OBJECT_DETECTION, PYTORCH_FRAMEWORK): TorchObjectDetector,
    (KEYPOINT_DETECTION, PYTORCH_FRAMEWORK): TorchKeyPointDetector,
    (TEXT_CLASSIFICATION, PYTORCH_FRAMEWORK): TorchTextClassifier,
    (GENERIC_CLASSIFICATION, PYTORCH_FRAMEWORK): TorchGenericClassifier,
    (GENERIC_CLASSIFICATION, SKLEARN_FRAMEWORK): SKLGenericClassifier,
    # Add more categories and corresponding classes here
}
