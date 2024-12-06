import sklearn
from sklearn.base import is_classifier, is_regressor
from tracebloc_package.utils.constants import SKLEARN_FRAMEWORK


class SklearnChecks:
    def __init__(self, model, category, message, classes, model_type, progress_bar):
        self.message = message
        self.model = model
        self.category = category
        self.progress_bar = progress_bar
        self.utilisation_category = "low"
        self.classes = classes
        self.model_type = model_type

    def is_model_supported(self):
        """
        Check if model contains:
            - input_shape
            - classes
        """
        supported = True
        # Check for classifier or regressor
        if not (is_classifier(self.model) or is_regressor(self.model)):
            return False

        # Check for required methods
        required_methods = ["fit", "predict"]
        for method in required_methods:
            if not hasattr(self.model, method):
                supported = False
            if not supported:  # pragma: no cover
                self.message = "\nModel file not provided as per docs: model does not support sklearn functions"  # pragma: no cover
                raise Exception("sklearn functions not supported")  # pragma: no cover
        self.progress_bar.update(3)

    def small_training_loop(self, weight_filename, custom_loss=False):
        raise NotImplementedError(
            self.__class__.__name__ + "need to override this function"
        )
