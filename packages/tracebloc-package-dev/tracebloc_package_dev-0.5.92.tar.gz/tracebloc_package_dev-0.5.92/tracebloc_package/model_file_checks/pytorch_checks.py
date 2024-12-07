from tracebloc_package.utils.general_utils import (
    validate_kwargs,
)


class TorchChecks:
    def __init__(self, **kwargs):
        validate_kwargs(
            kwargs,
            {
                "model",
                "category",
                "message",
                "progress_bar",
                "classes",
            },
        )
        self.message = kwargs["message"]
        self.model = kwargs["model"]
        self.category = kwargs["category"]
        self.progress_bar = kwargs["progress_bar"]
        self.classes = kwargs["classes"]
        self.average_weights_file_path = None
        self.loss = None
        self.utilisation_category = "low"

    def is_model_supported(self):
        """
        Check if model contains:
            - forward function
        """
        model = self.model
        self.progress_bar.update(1)
        if not hasattr(model, "forward"):
            self.message = "\nModel file not provided as per docs: forward function not found in  Model"
            raise Exception("forward func missing")

    def small_training_loop(self, weight_filename, custom_loss=False):
        raise NotImplementedError(
            self.__class__.__name__ + "need to override this function"
        )
