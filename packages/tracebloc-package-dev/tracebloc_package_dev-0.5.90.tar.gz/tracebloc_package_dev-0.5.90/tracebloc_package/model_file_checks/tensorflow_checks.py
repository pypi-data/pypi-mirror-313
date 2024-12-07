import tensorflow as tf
from silence_tensorflow import silence_tensorflow

silence_tensorflow()


class TensorflowChecks:
    def __init__(self, model, category, message, progress_bar):
        self.message = message
        self.model = model
        self.category = category
        self.progress_bar = progress_bar
        self.utilisation_category = "low"

    def is_model_supported(self):
        """
        Check if model contains:
            - input_shape
            - classes
        """
        tensorflow_supported_apis = (tf.keras.models.Sequential, tf.keras.Model)
        model = self.model
        supported = isinstance(model, tensorflow_supported_apis)
        if supported:  # pragma: no cover
            # check if it is of model subclassing api
            if not hasattr(model, "input_shape"):
                self.message = "\nModel file not provided as per docs: unsupported API used for Model"  # pragma: no cover
                raise Exception("input shape missing")  # pragma: no cover
        self.progress_bar.update(1)

    def layer_instance_check(self):
        """
        If model layers are of type keras layers
        """
        for layer in self.model.layers:
            if not isinstance(layer, tf.keras.layers.Layer):
                self.message = "\nLayers in Model are not supported by Tensorflow"  # pragma: no cover
                raise Exception("invalid layer")  # pragma: no cover
        self.progress_bar.update(1)

    def small_training_loop(self, weight_filename, custom_loss=False):
        raise NotImplementedError(
            self.__class__.__name__ + "need to override this function"
        )

    def check_original_model_channels(self):
        """
        check for model channels to be 3
        """
        model_channel = self.model
        if model_channel.input_shape[3] != 3:
            self.message = (
                "\nPlease provide model input shape with 3 channels"  # pragma: no cover
            )
            raise Exception("invalid input shape")  # pragma: no cover
        self.progress_bar.update(1)
