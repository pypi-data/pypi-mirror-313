import inspect
import os
import pprint
import requests, json
import base64
from termcolor import colored
from tracebloc_package.utils import check_parameters
from tracebloc_package.model_file_checks.tensorflow_checks import TensorflowChecks
from tracebloc_package.model_file_checks.pytorch_checks import TorchChecks
from tracebloc_package.utils.general_utils import (
    getImagesCount,
    validate_kwargs,
    get_model_params_count,
)
from tracebloc_package.utils.constants import (
    CONSTANT,
    STANDARD,
    ADAPTIVE,
    CUSTOM,
    TYPE,
    VALUE,
    TRAINED_WEIGHTS_FILENAME,
    TENSORFLOW_FRAMEWORK,
    PYTORCH_FRAMEWORK,
    IMAGE_CLASSIFICATION,
    GENERIC_CLASSIFICATION,
    TEXT_CLASSIFICATION,
    SKLEARN_FRAMEWORK,
)


class LinkModelDataSet:
    """
    creating a training plan and assign data set
    parameters: modelId, datasetId, token

    methods:get_parameters, get_trainingplan
    """

    def __init__(self, **kwargs):
        self.default_dict = kwargs
        validate_kwargs(
            kwargs,
            {
                "modelId",
                "model",
                "modelname",
                "datasetId",
                "token",
                "weights",
                "totalDatasetSize",
                "total_images",
                "num_classes",
                "class_names",
                "image_size",
                "batchsize",
                "model_path",
                "url",
                "environment",
                "framework",
                "model_type",
                "category",
                "loss",
                "model_id",
                "hf_token",
                "utilisation_category",
            },
        )
        self.__framework = kwargs["framework"]
        self.__url = kwargs["url"]
        self.__token = kwargs["token"]
        self.__earlystopCallback = {}
        self.__reducelrCallback = {}
        self.__modelCheckpointCallback = {}
        self.__terminateOnNaNCallback = {}
        self.__learningRateSet = False
        self.__optimizerSet = False
        self.__callbacks = str()
        self.__message = "training"
        self.__datasetId = kwargs["datasetId"]
        self.__epochs = 10
        self.__cycles = 1
        self.__modelId = kwargs["modelId"]
        self.__modelName = kwargs["modelname"]
        self.__model = kwargs["model"]
        self.__image_shape = kwargs["image_size"]
        self.__image_type = "rgb"
        self.__optimizer = "sgd"
        self.__totalDatasetSize = kwargs["totalDatasetSize"]
        self.__category = kwargs["category"]
        self.__trainingDatasetSize = kwargs["totalDatasetSize"]
        self.__trainingClasses = kwargs["class_names"]
        self.__subdataset = {}
        self.__model_id = kwargs["model_id"]
        self.__hf_token = kwargs["hf_token"]
        self.__lora_enable = False
        self.__lora_r = 256
        self.__lora_alpha = 512
        self.__lora_dropout = 0.05
        self.__q_lora = False
        if kwargs["loss"] is not None:
            self.__lossFunction = {TYPE: CUSTOM, VALUE: "loss.py"}
        else:
            self.__lossFunction = (
                {TYPE: STANDARD, VALUE: "crossentropy"}
                if self.__category == TEXT_CLASSIFICATION
                else {TYPE: STANDARD, VALUE: "mse"}
            )
        self.__learningRate = {TYPE: CONSTANT, VALUE: 0.001}
        self.__seed = False
        self.__total_images = kwargs["total_images"]
        self.__images_per_edge = kwargs["total_images"]
        self.__num_classes = kwargs["num_classes"]
        self.__class_names = kwargs["class_names"]
        self.__batchSize = self.__default_batchSize(kwargs["batchsize"])
        self.__featurewise_center = False
        self.__samplewise_center = False
        self.__featurewise_std_normalization = False
        self.__samplewise_std_normalization = False
        self.__zca_whitening = False
        self.__rotation_range = 0
        self.__width_shift_range = 0.0
        self.__height_shift_range = 0.0
        self.__brightness_range = "None"
        self.__shear_range = 0.0
        self.__zoom_range = 0.0
        self.__channel_shift_range = 0.0
        self.__fill_mode = "constant"
        self.__cval = 0.0
        self.__horizontal_flip = False
        self.__vertical_flip = False
        self.__rescale = "None"
        self.__validation_split = self.__default_validation_split()
        self.__shuffle = True
        self.__layers_non_trainable = ""
        self.__metrics = str(["accuracy"])
        self.__objective = ""
        self.__name = "None"
        self.__model_type = kwargs["model_type"]
        self.__model_params = self.__set_model_params()
        self.__upperboundTime = 0
        self.__weights = kwargs["weights"]
        self.__images_per_class = json.dumps(self.__class_names)
        self.__feature_interaction = []
        self.__eligibility_passed = True
        self.__error_method = []
        self.__reform_model = False
        self.__utilisation_category = kwargs["utilisation_category"]
        self.model_path = kwargs["model_path"]
        self._model_name = kwargs["modelname"]
        self.tmp_path = os.path.join(
            self.model_path.rsplit("/", 1)[0],
            f"tmpmodel_{self._model_name[:64]}",
        )
        if self.__category == GENERIC_CLASSIFICATION:
            print(
                "User can create new features for this dataset. For this you can use 'feature_interaction' method for this. To get feature list use 'get_features' method."
            )
        if not os.path.isdir(self.tmp_path):
            os.mkdir(self.tmp_path)
        self._environment = kwargs["environment"]
        self.__experimenturl = "https://ai.tracebloc.io/experiments/"
        if kwargs["environment"] == "development" or kwargs["environment"] == "ds":
            self.__experimenturl = "https://dev.tracebloc.io/experiments/"
        elif kwargs["environment"] == "staging":
            self.__experimenturl = "https://stg.tracebloc.io/experiments/"

    def resetTrainingPlan(self):
        self.__earlystopCallback = {}
        self.__reducelrCallback = {}
        self.__modelCheckpointCallback = {}
        self.__terminateOnNaNCallback = {}
        self.__learningRateSet = False
        self.__optimizerSet = False
        self.__callbacks = str()
        self.__epochs = 10
        self.__cycles = 1
        self.__image_shape = self.default_dict["image_size"]
        self.__image_type = "rgb"
        self.__optimizer = "sgd"
        self.__trainingDatasetSize = self.default_dict["totalDatasetSize"]
        self.__trainingClasses = self.default_dict["class_names"]
        # self.__lossFunction = {TYPE: STANDARD, VALUE: "mse"}
        self.__learningRate = {TYPE: CONSTANT, VALUE: 0.001}
        self.__seed = False
        self.__batchSize = self.__default_batchSize(self.default_dict["batchsize"])
        self.__featurewise_center = False
        self.__samplewise_center = False
        self.__featurewise_std_normalization = False
        self.__samplewise_std_normalization = False
        self.__zca_whitening = False
        self.__rotation_range = 0
        self.__width_shift_range = 0.0
        self.__height_shift_range = 0.0
        self.__brightness_range = "None"
        self.__shear_range = 0.0
        self.__zoom_range = 0.0
        self.__channel_shift_range = 0.0
        self.__fill_mode = "constant"
        self.__cval = 0.0
        self.__horizontal_flip = False
        self.__vertical_flip = False
        self.__rescale = "None"
        self.__validation_split = self.__default_validation_split()
        self.__shuffle = True
        self.__layers_non_trainable = ""
        self.__metrics = str(["accuracy"])
        self.__objective = ""
        self.__name = "None"
        self.__model_type = self.default_dict["model_type"]
        self.__category = self.default_dict["category"]
        self.__upperboundTime = 0
        self.__images_per_edge = self.__total_images
        self.__images_per_class = json.dumps(self.__class_names)
        self.__feature_interaction = []
        self.__eligibility_passed = True
        self.__reform_model = False
        print("Training Plan Parameters reset")

    def __print_error(self, error):
        self.__eligibility_passed = False
        method = inspect.currentframe().f_back.f_code.co_name
        text = colored(
            error,
            "red",
        )
        print(text, "\n")
        self.__error_method.append(method)

    def __set_model_params(self):
        return get_model_params_count(framework=self.__framework, model=self.__model)

    def __not_supported_parameters(self, parameter, framework="pytorch", message=False):
        if message:
            print_statement = parameter
        else:
            print_statement = (
                f"The parameter {parameter} is not supported on {framework}\n"
            )
        text = colored(
            print_statement,
            "red",
        )
        print(text, "\n")
        return

    def __remove_error_method(self):
        method = inspect.currentframe().f_back.f_code.co_name
        if method in self.__error_method:
            self.__error_method.remove(method)
        if len(self.__error_method) == 0:
            self.__eligibility_passed = True

    def trainingClasses(self, training_dataset: dict):
        """
        creates sub dataset of the current dataset of the no of images per class selected by user
        Please provide number of images per class
        example: dataset: {'car': 65, 'person': 42}
        Classes in dataset car, person

        trainingObject.trainingClasses({'car': 30, 'person': 30})
        """
        class_names = self.__class_names.keys()
        for class_name in class_names:
            num_images = int(self.__class_names[class_name])
            least_data = 5 if num_images > 5 else 1
            if class_name in training_dataset.keys():
                value = training_dataset[class_name]
                if least_data < value <= num_images:
                    pass
                else:
                    error_msg = (
                        f"trainingClasses: Please provide num of images for class {class_name}\n "
                        f"greater than 5 and less than equal to {num_images}\n"
                    )
                    self.__print_error(error_msg)
                    return
            else:
                error_msg = (
                    "trainingClasses: trainingDatasetSize dictionary must contain all classes that are present in the "
                    "dataset.\n"
                    " Customisation in terms of classes is not allowed.\n"
                )
                self.__print_error(error_msg)
                return
        self.__trainingClasses = training_dataset
        self.__trainingDatasetSize = getImagesCount(training_dataset)
        # recalculate the validation split
        header = {"Authorization": f"Token {self.__token}"}
        data = {
            "edges_involved": json.dumps(list(self.__images_per_edge.keys())),
            "images_per_class": json.dumps(training_dataset),
            "type": "recalculate_image_count_per_edge",
            "datasetId": self.__datasetId,
        }
        re = requests.post(
            f"{self.__url}check-model/",
            headers=header,
            data=data,
        )
        body_unicode = re.content.decode("utf-8")
        content = json.loads(body_unicode)
        if re.status_code == 200:
            self.__images_per_edge = content["total_images_per_edge"]
            if self.__validation_split < self.__default_validation_split():
                self.__validation_split = self.__default_validation_split()
            if (
                self.__framework == TENSORFLOW_FRAMEWORK
                and self.__batchSize > self.__default_batchSize()
            ):
                self.__batchSize = self.__default_batchSize()
            self.__images_per_class = json.dumps(
                training_dataset
            )  # assign images count for sub-dataset
            self.__subdataset = json.dumps(
                {
                    "trainingDatasetSize": self.__trainingDatasetSize,
                    "trainingClasses": self.__trainingClasses,
                }
            )
            self.__remove_error_method()
        else:
            if self._environment == "production" or self._environment == "":
                self.__print_error("trainingClasses:Error while setting subdataset\n")
            else:
                self.__print_error(content["message"])

    def __update_image_model(self):
        """
        change image type and size data as user choice in model file provided by user
        """
        header = {"Authorization": f"Token {self.__token}"}
        data = {
            "model_name": self.__modelId,
            "image_shape": self.__image_shape,
            "image_type": self.__image_type,
            "type": "reform_model",
        }
        re = requests.post(
            f"{self.__url}check-model/",
            headers=header,
            data=data,
        )
        if re.status_code == 202:
            body_unicode = re.content.decode("utf-8")
            content = json.loads(body_unicode)
            self.__modelId = content["model_name"]
        if re.status_code == 400:
            body_unicode = re.content.decode("utf-8")
            content = json.loads(body_unicode)
            error_message = f"imageType:Error Occured while setting updated image format \nfor model as {content['message']}\n"
            self.__print_error(error_message)

    def imageShape(self, image_shape: int):
        """
        Set image shape
        parameters: integer. value must be between 48 and 224
        example: trainingObject.imageShape(224)
        default: 224
        maximum value : 224
        warning : for pytorch please only imageshape for which layers are designed and is specified in model file is allowed
        """
        if self.__framework == TENSORFLOW_FRAMEWORK:
            if type(image_shape) is int and (48 <= image_shape <= 224):
                self.__image_shape = image_shape
                self.__update_image_model()
                self.__remove_error_method()
            else:
                error_msg = "imageShape:Invalid type"
                self.__print_error(error_msg)
        else:
            error_msg = (
                "imageShape:Image shape/size is fixed for each model for pytorch\n"
            )
            self.__not_supported_parameters(error_msg, message=True)
            self.__remove_error_method()

    def imageType(self, image_type: str):
        """
        Set image type to be used for training
        parameters: string type values.
        supported type: ['rgb', 'gray']
        example: trainingObject.imageType('rgb')
        default: rgb
        """
        allowed_types = ["rgb", "grayscale"]
        try:
            if type(image_type) is str:
                allowed_types.index(image_type.lower())
                self.__image_type = image_type.lower()
                if self.__framework == TENSORFLOW_FRAMEWORK:
                    self.__update_image_model()
                self.__remove_error_method()
        except:
            error_msg = f"imageType:Enter values from {allowed_types}\n "
            self.__print_error(error_msg)

    def seed(self, seed: bool):
        """
        Boolean.
        Sets the global random seed when selected
        default: False
        example:trainingObject.seed(True)
        """
        if type(seed) == bool:
            self.__seed = str(seed)
            self.__remove_error_method()
        else:
            error_msg = "seed:Invalid input type\n"
            self.__print_error(error_msg)

    def experimentName(self, name: str):
        """
        String.
        Name of the experiment
        example:trainingObject.experimentName('Classifying manufacturing defects')
        """
        self.__name = str(name)

    def objective(self, objective: str):
        """
        String.
        Objective of the experiment
        example:trainingObject.objective('Classify images using Convolutional Neural Networks (specifically, VGG16)
        pre-trained on the ImageNet dataset with Keras deep learning library.')
        """
        if type(objective) == str:
            self.__objective = objective
            self.__remove_error_method()
        else:
            error_msg = "objective:Please enter a string in objective\n"
            self.__print_error(error_msg)

    def epochs(self, epochs: int):
        """
        Integer.
        Number of epochs to train the model.
        An epoch is an iteration over the entire data provided.
        Note that in conjunction with initial_epoch, epochs is to be understood as "final epoch".
        The model is not trained for a number of iterations given by epochs,
        but merely until the epoch of index epochs is reached.
        example: trainingObject.epochs(100)
        default: 10
        """
        if type(epochs) == int and epochs != 0:
            self.__epochs = epochs
            self.__remove_error_method()
        else:
            error_msg = "epochs:Invalid input type or value '0' given for epochs\n"
            self.__print_error(error_msg)

    def cycles(self, cycles: int):
        """
        Set number of cycles
        parameters: integer type values.
        example: trainingObject.cycles(10)
        default: 1
        """
        if type(cycles) == int and cycles != 0:
            self.__cycles = cycles
            self.__remove_error_method()
        else:
            self.__eligibility_passed = False
            error_msg = "cycles:Invalid input type\n"
            self.__print_error(error_msg)

    def __default_batchSize(self, batchsize=None):
        """
        set default batch size when training object is created
        """
        # get edge with the lowest images
        if self.__framework == TENSORFLOW_FRAMEWORK or batchsize is None:
            edge_min = min(self.__images_per_edge, key=self.__images_per_edge.get)
            # get images count for selected edge
            images = int(self.__images_per_edge[edge_min])
            batch = images // 3
            if 8 <= batch < 16:
                return 8
            elif 16 <= batch < 32:
                return 16
            elif 32 <= batch < 64:
                return 32
            elif 64 <= batch < 128:
                return 64
            else:
                return 128
        else:
            return batchsize

    def batchSize(self, batchSize: int):
        """
        Integer or None. Number of samples per gradient update. If unspecified, batch_size will default to 32.
        example: trainingObject.batchSize(16)
        default: 32
        """
        if self.__framework != PYTORCH_FRAMEWORK:
            # get edge with the lowest images
            edge_min = min(self.__images_per_edge, key=self.__images_per_edge.get)
            # get images count for selected edge
            images = int(self.__images_per_edge[edge_min])
            # check for no of batches
            if type(batchSize) == int:
                if images // batchSize < 3:
                    error_msg = "batchSize:Please choose smaller batch size as dataset selected have less images\n"
                    self.__print_error(error_msg)
                    return
                elif batchSize < self.__num_classes:
                    error_msg = "batchSize:Please choose batch size greater than num of classes in dataset provided\n"
                    self.__print_error(error_msg)
                    return
                elif batchSize > 128:
                    error_msg = "batchSize:Please choose batch size less than 128\n"
                    self.__print_error(error_msg)
                    return
                self.__batchSize = batchSize
                self.__remove_error_method()
            else:
                error_msg = "batchSize:Invalid input type\n"
                self.__print_error(error_msg)
        else:
            error_msg = "batchSize:batch-size is fixed for each model for pytorch"
            self.__not_supported_parameters(error_msg, message=True)
            self.__remove_error_method()

    def __default_validation_split(self):
        """
        set default validation split when training object is created
        """
        # get edge with lowest images
        edge_min = min(self.__images_per_edge, key=self.__images_per_edge.get)
        images = int(self.__images_per_edge[edge_min])
        minimum = round(self.__num_classes / images, 2)
        if minimum == 0:
            return 0.1
        elif minimum > 0.5:
            return 0.5
        return minimum

    def validation_split(self, validation_split: float):
        """
        Float. Fraction of images reserved for validation (strictly between 0 and 1).
        example: trainingObject.validation_split(0.2)
        default: 0.1
        """
        # calculate minimum validation split using the following equation
        # minimum = number of classes / total images
        # get edge with lowest images
        # edge_min = min(self.__images_per_edge, key=self.__images_per_edge.get)
        # images = int(self.__images_per_edge[edge_min])
        # minimum = round(self.__num_classes / images, 2)
        minimum = self.__default_validation_split()

        if type(validation_split) == float and minimum <= validation_split <= 0.5:
            self.__validation_split = validation_split
            self.__remove_error_method()
        else:
            error_msg = f"validation_split:Invalid input type or value not in [{minimum}, 0.5]\n"
            self.__print_error(error_msg)

    def optimizer(self, optimizer: str):
        """
        String (name of optimizer)
        example: trainingObject.optimizer('rmsprop')
        supported optimizers: ['adam','rmsprop','sgd','adadelta', 'adagrad', 'adamax','nadam', 'ftrl'] for tensorflow
        supported optimizers: ["adam", "rmsprop", "sgd", "adadelta", "adagrad", "adamax"] for pytorch
        default: 'sgd'
        """
        if self.__framework == TENSORFLOW_FRAMEWORK:
            o = [
                "adam",
                "rmsprop",
                "sgd",
                "adadelta",
                "adagrad",
                "adamax",
                "nadam",
                "ftrl",
            ]
            optlrrateflag = True
            error = None
            optimizer = optimizer.lower()
            try:
                o.index(optimizer)
                if self.__learningRateSet:
                    optlrrateflag, error = check_parameters.get_optimizer(
                        optimizer, self.__learningRate.copy()
                    )
                if not optlrrateflag and error is not None:
                    error_msg = (
                        f"optimizer:While setting optimiser error Occurred as {error}\n"
                    )
                    self.__print_error(error_msg)
                else:
                    self.__optimizer = optimizer
                    self.__optimizerSet = True
                    self.__remove_error_method()
            except Exception as e:
                error_msg = f"optimizer:Please provide supported optimizers:\n {o}\n"
                self.__print_error(error_msg)
        else:
            o = [
                "adam",
                "rmsprop",
                "sgd",
                "adadelta",
                "adagrad",
                "adamax",
            ]
            try:
                o.index(optimizer)
                self.__optimizer = optimizer
                self.__remove_error_method()
            except:
                error_msg = f"optimizer:Please provide supported optimizers: \n{o}\n"
                self.__print_error(error_msg)

    def learningRate(self, learningRate: dict):
        """
        Set learning rate by passing a dictionary
        There are three different type of learningrate : constant, adaptive, custom
        default: {'type': 'constant', 'value': 0.0001}
        Set constant type learning rate for optimization.
        parameters: value
        example: trainingObject.learningRateConstant({'type': 'constant', 'value': 0.0001})

        Adaptive learning rate as per learning rate schedulars present in tensorflow
        parameters: dictionary containing schedular Name in schedular key value and rest all neccessary parameters added in dictionary
        example: trainingObject.learningRateAdaptive({'type': 'adaptive', 'schedular': 'ExponentialDecay', 'decay_steps':1000, 'decay_rate':0.5})

        Set learning rate for as custom function.
        first write custom learning rate function as method and pass method name in learning rate
        example:
        def custom_LearningRate_schedular(epoch):
            if epoch < 5:
                return 0.01
            else:
                return 0.01 * tf.math.exp(0.1 * (10 - epoch))
        trainingObject.learningRateCustom({'type': 'constant', 'value': custom_LearningRate_schedular, 'epoch': 4})
        """
        if self.__framework != PYTORCH_FRAMEWORK:
            optlrrateflag = True
            error = None
            if TYPE in learningRate.keys():
                if self.__optimizerSet:
                    optlrrateflag, error = check_parameters.get_optimizer(
                        self.__optimizer, learningRate.copy()
                    )
                if not optlrrateflag:
                    error_msg = f"learningRate:While setting Learning Rate error Occurred as \n{error}\n"
                    self.__print_error(error_msg)
                else:
                    if learningRate[TYPE] == CUSTOM and callable(learningRate[VALUE]):
                        try:
                            # Serialize the loss function
                            serialized_data = learningRate
                            # Encode the binary data as text
                            encoded_data = base64.b64encode(serialized_data).decode(
                                "utf-8"
                            )
                            self.__learningRate = {TYPE: CUSTOM, VALUE: encoded_data}
                            self.__learningRateSet = True
                            self.__remove_error_method()
                        except Exception as e:
                            error_msg = f"learningRate:Error while setting custom learning rate : \n{e}\n"
                            self.__print_error(error_msg)
                    elif (
                        learningRate[TYPE] == CONSTANT or learningRate[TYPE] == ADAPTIVE
                    ):
                        self.__learningRate = learningRate
                        self.__learningRateSet = True
                        self.__remove_error_method()
                    else:
                        error_msg = "learningRate:Input not as per given convention for learningRate\n"
                        self.__print_error(error_msg)
            else:
                error_msg = (
                    "learningRate:Input not as per given convention for learningRate\n"
                )
                self.__print_error(error_msg)
        else:
            if learningRate[TYPE] == CONSTANT:
                self.__learningRate = learningRate
                self.__remove_error_method()
            else:
                error_msg = "learningRate:Adaptive and Custom learning rate"
                self.__not_supported_parameters(error_msg)
                self.__remove_error_method()

    def lossFunction(self, lossFunction: dict):
        """
        Set the loss function.

        Parameters: String type values or custom loss function.

        Default: {'type': 'standard', 'value': 'mse'}

        Set standard loss functions like this:
        Example: `trainingObject.lossFunction({'type': 'standard', 'value': 'categorical_crossentropy'})`

        Supported loss functions for TensorFlow:
        ['binary_crossentropy', 'categorical_crossentropy', 'mse']

        Supported loss functions for PyTorch:
        ['crossentropy', 'mse', 'l1']

        Set a custom loss function like this:
        Example:
        ```python
        def custom_mse(y_true, y_pred):
            # Calculate squared difference between target and predicted values
            loss = torch.square(y_pred - y_true)  # (batch_size, 2)

            # Multiply the values with weights along the batch dimension
            loss = loss * torch.tensor([0.3, 0.7])  # (batch_size, 2)

            # Sum both loss values along the batch dimension
            loss = torch.sum(loss, axis=1)  # (batch_size,)
            return loss

        trainingObject.lossFunction({'type': 'custom', 'value': custom_mse})

        """
        if self.__framework == TENSORFLOW_FRAMEWORK:
            l = ["binary_crossentropy", "categorical_crossentropy", "mse"]
            if TYPE in lossFunction.keys() and VALUE in lossFunction.keys():
                if lossFunction[TYPE] == STANDARD:
                    try:
                        l.index(lossFunction[VALUE].lower())
                        self.__lossFunction = lossFunction
                        self.__remove_error_method()
                    except:
                        error_msg = f"lossFunction:Please provide tensorflow supported default loss functions losses: \n{l}\n"
                        self.__print_error(error_msg)
                elif lossFunction[TYPE] == CUSTOM:
                    if os.path.exists(os.path.join(self.tmp_path, "loss.py")):
                        try:
                            model_checks = TensorflowChecks(
                                model=self.__model,
                                model_name=self.__modelName,
                                model_type=self.__model_type,
                                category=self.__category,
                                classes=self.__num_classes,
                                progress_bar=None,
                                message="",
                                tmp_path=self.tmp_path,
                            )
                            model_checks.small_training_loop(
                                weight_filename=TRAINED_WEIGHTS_FILENAME,
                                custom_loss=True,
                            )
                        except Exception as e:
                            error_msg = f"lossFunction:custom loss provided give error as \n{e}\n"
                            self.__print_error(error_msg)
                            return
                    else:
                        error_msg = "loss.py file missing in the zip.\n Please refer docs for more information."
                        self.__print_error(error_msg)
                        return
                else:
                    error_msg = (
                        "lossFunction:Invalid input function given for loss function\n"
                    )
                    self.__print_error(error_msg)
            else:
                error_msg = "lossFunction:type missing\n"
                self.__print_error(error_msg)
        elif self.__framework == SKLEARN_FRAMEWORK:
            l = ["mse", "binarycrossentropy"]
            if (
                TYPE in lossFunction.keys()
                and VALUE in lossFunction.keys()
                and lossFunction[TYPE] == STANDARD
            ):
                try:
                    l.index(lossFunction[VALUE].lower())
                    self.__lossFunction = lossFunction
                    self.__remove_error_method()
                except:
                    error_msg = f"lossFunction:Please provide sklearn supported default loss functions losses: \n{l}\n"
                    self.__print_error(error_msg)
            else:
                error_msg = f"lossFunction:only standard loss function supported in sklearn \n{l}\n"
                self.__print_error(error_msg)
        else:
            if self.__category == TEXT_CLASSIFICATION:
                l = ["crossentropy"]
            elif self.__category == GENERIC_CLASSIFICATION:
                l = ["mse"]
            else:
                l = ["crossentropy", "mse", "l1"]
            if (
                TYPE in lossFunction.keys()
                and VALUE in lossFunction.keys()
                and lossFunction[TYPE] == STANDARD
            ):
                try:
                    l.index(lossFunction[VALUE].lower())
                    self.__lossFunction = lossFunction
                    self.__remove_error_method()
                except:
                    error_msg = f"lossFunction:Please provide pytorch supported default loss functions losses: \n{l}\n"
                    self.__print_error(error_msg)
            elif lossFunction[TYPE] == CUSTOM:
                if os.path.exists(os.path.join(self.tmp_path, "loss.py")):
                    try:
                        model_checks = TorchChecks(
                            model=self.__model,
                            model_name=self.__modelName,
                            model_type=self.__model_type,
                            category=self.__category,
                            progress_bar=None,
                            message="",
                            image_size=self.__image_shape,
                            batch_size=self.__batchSize,
                            classes=self.__num_classes,
                            tmp_path=self.tmp_path,
                        )
                        model_checks.small_training_loop(
                            weight_filename=TRAINED_WEIGHTS_FILENAME,
                            custom_loss=True,
                        )
                    except Exception as e:
                        error_msg = (
                            f"lossFunction:custom loss provided give error as \n{e}\n"
                        )
                        self.__print_error(error_msg)
                        return
                else:
                    error_msg = "loss.py file missing in the zip.\n Please refer docs for more information."
                    self.__print_error(error_msg)
                    return

    def __check_layers(self, layersFreeze):
        """
        load model and get all layers avaiable in model
        """
        try:
            for layer_to_freeze in layersFreeze:
                layer = self.__model.get_layer(layer_to_freeze)
        except Exception as e:
            return False, e
        return True, ""

    def layersFreeze(self, layersFreeze: list):
        """
        Provide name of layers in a list to be frozen before training a model.
        Get layers name in a model provided with the summary shown above.
        example: trainingObject.layersFreeze(['layer_name','layer_name', ...])
        default: None
        """
        if self.__framework == TENSORFLOW_FRAMEWORK:
            if type(layersFreeze) == list and all(
                isinstance(sub, str) for sub in layersFreeze
            ):
                layers_eligible = True
                status, _error = self.__check_layers(layersFreeze)
                if not status:
                    layers_eligible = False
                if layers_eligible:
                    layersFreeze = str(layersFreeze)
                    self.__layers_non_trainable = layersFreeze
                    self.__remove_error_method()
                else:
                    error_msg = f"layersFreeze:Provide layers only which model contains for layersFreeze : \n{_error}\n"
                    self.__print_error(error_msg)
            else:
                error_msg = (
                    "layersFreeze:Provide values as list of strings for layersFreeze\n"
                )
                self.__print_error(error_msg)
        else:
            self.__not_supported_parameters("layersFreeze")
            self.__remove_error_method()

    def terminateOnNaNCallback(self):
        """
        Callback that terminates training when a NaN loss is encountered.
        example: trainingObject.terminateOnNaNCallback()
        """
        c = [""]
        self.__terminateOnNaNCallback["terminateOnNaN"] = c

    def modelCheckpointCallback(self, monitor: str, save_best_only: bool):
        """
        Callback to save the model weights. parameters: monitor: Quantity to be monitored, save_best_only:  if
        save_best_only=True, it only saves when the model is considered the "best" and the latest best model
        according to the quantity monitored will not be overwritten. example: trainingObject.modelCheckpointCallback(
        'val_loss', True)
        """
        f = ["accuracy", "loss", "val_loss", "val_accuracy"]
        try:
            f.index(monitor.lower())
            if type(save_best_only) == bool:
                c = [monitor, save_best_only]
                self.__modelCheckpointCallback["modelCheckpoint"] = c
                self.__remove_error_method()
            else:
                error_msg = "modelCheckpointCallback:Invalid datatype for arguments given for save_best_only\n"
                self.__print_error(error_msg)
        except:
            error_msg = f"modelCheckpointCallback:Please provide supported monitor values: {f}\n"
            self.__print_error(error_msg)

    def earlystopCallback(self, monitor: str, patience: int):
        """
        Stop training when a monitored metric has stopped improving.
        parameters: monitor: Quantity to be monitored,
                                patience: Number of epochs with no improvement after which training will be stopped.
        example: trainingObject.earlystopCallback('loss', 10)


        """
        f = ["accuracy", "loss", "val_loss", "val_accuracy"]
        try:
            f.index(monitor.lower())
            if type(patience) == int:
                c = [monitor, patience]
                self.__earlystopCallback["earlystopping"] = c
                self.__remove_error_method()
            else:
                error_msg = "earlystopCallback:Invalid datatype for arguments given for patience\n"
                self.__print_error(error_msg)
        except:
            error_msg = (
                f"earlystopCallback:Please provide supported monitor values: {f}\n"
            )
            self.__print_error(error_msg)

    def reducelrCallback(
        self, monitor: str, factor: float, patience: int, min_delta: float
    ):
        """
        Reduce learning rate when a metric has stopped improving. parameters: monitor: Quantity to be monitored,
        factor: factor by which the learning rate will be reduced. new_lr = lr * factor. patience: number of epochs
        with no improvement after which learning rate will be reduced. min_delta: threshold for measuring the new
        optimum, to only focus on significant changes.
        example: trainingObject.reducelrCallback('loss', 0.1, 10, 0.0001)
        """
        f = ["accuracy", "loss", "val_loss", "val_accuracy"]
        try:
            f.index(monitor.lower())
            if (
                type(factor) == float
                and type(patience) == int
                and type(min_delta) == float
            ):
                c = [monitor, factor, patience, min_delta]
                self.__reducelrCallback["reducelr"] = c
                self.__remove_error_method()
            else:
                error_msg = "reducelrCallback:Invalid datatype for arguments given for reducelrCallback\n"
                self.__print_error(error_msg)
        except:
            error_msg = (
                f"reducelrCallback:Please provide supported monitor values: {f}\n"
            )
            self.__print_error(error_msg)

    def __setCallbacks(self):
        """
        List of dictionaries.
        List of tensorflow callbacks for training.
        default: []
        """
        c = []
        if len(self.__reducelrCallback) != 0:
            c.append(self.__reducelrCallback)
        if len(self.__earlystopCallback) != 0:
            c.append(self.__earlystopCallback)
        if len(self.__modelCheckpointCallback) != 0:
            c.append(self.__modelCheckpointCallback)
        if len(self.__terminateOnNaNCallback) != 0:
            c.append(self.__terminateOnNaNCallback)

        self.__callbacks = str(c)

    def samplewise_center(self, samplewise_center: bool):
        """
        Boolean. Set each sample mean to 0.
        example: trainingObject.samplewise_center(True)
        default: False
        """
        if self.__framework != PYTORCH_FRAMEWORK:
            if type(samplewise_center) == bool:
                self.__samplewise_center = samplewise_center
                self.__remove_error_method()
            else:
                error_msg = (
                    "samplewise_center:Invalid input type given for samplewise_center\n"
                )
                self.__print_error(error_msg)
        else:
            self.__not_supported_parameters("samplewise_center")
            self.__remove_error_method()

    def samplewise_std_normalization(self, samplewise_std_normalization: bool):
        """
        Boolean. Divide each input by its std.
        example: trainingObject.samplewise_std_normalization(True)
        default: False
        """
        if self.__framework != PYTORCH_FRAMEWORK:
            if type(samplewise_std_normalization) == bool:
                self.__samplewise_std_normalization = samplewise_std_normalization
                self.__remove_error_method()
            else:
                error_msg = "samplewise_std_normalization:Invalid input type given for samplewise_std_normalization\n"
                self.__print_error(error_msg)
        else:
            self.__not_supported_parameters("samplewise_std_normalization")
            self.__remove_error_method()

    def rotation_range(self, rotation_range: int):
        """
        Int. Degree range for random rotations.
        example: trainingObject.rotation_range(2)
        default: 0
        """
        if self.__framework != SKLEARN_FRAMEWORK:
            if type(rotation_range) == int:
                self.__rotation_range = rotation_range
                self.__remove_error_method()
            else:
                error_msg = (
                    "rotation_range:Invalid input type given for rotation_range\n"
                )
                self.__print_error(error_msg)
        else:
            self.__not_supported_parameters(
                "rotation_range", framework=SKLEARN_FRAMEWORK
            )
            self.__remove_error_method()

    def width_shift_range(self, width_shift_range):
        """
        Float or int
        float: fraction of total width, if < 1, or pixels if >= 1.
        int: integer number of pixels from interval (-width_shift_range, +width_shift_range)
        With width_shift_range=2 possible values are integers [-1, 0, +1], same as with width_shift_range=[-1, 0, +1],
        while with width_shift_range=1.0 possible values are floats in the interval [-1.0, +1.0).
        example: trainingObject.width_shift_range(0.1)
        default: 0.0
        """
        if type(width_shift_range) == float or type(width_shift_range) == int:
            self.__width_shift_range = width_shift_range
            self.__remove_error_method()
        else:
            error_msg = (
                "width_shift_range:Invalid input type given for width_shift_range\n"
            )
            self.__print_error(error_msg)

    def height_shift_range(self, height_shift_range):
        """
        Float or int
        float: fraction of total height, if < 1, or pixels if >= 1.
        int: integer number of pixels from interval (-height_shift_range, +height_shift_range)
        With height_shift_range=2 possible values are integers [-1, 0, +1], same as with height_shift_range=[-1, 0, +1],
        while with height_shift_range=1.0 possible values are floats in the interval [-1.0, +1.0).
        example: trainingObject.height_shift_range(0.1)
        default: 0.0
        """
        if type(height_shift_range) == float or type(height_shift_range) == int:
            self.__height_shift_range = height_shift_range
            self.__remove_error_method()
        else:
            error_msg = (
                "height_shift_range:Invalid input type given for height_shift_range\n"
            )
            self.__print_error(error_msg)

    def brightness_range(self, brightness_range):
        """
        Tuple or list of two floats. Range for picking a brightness shift value from.
        example: trainingObject.brightness_range((0.1,0.4))
        default: None
        """
        if self.__framework == TENSORFLOW_FRAMEWORK:
            if (type(brightness_range) == tuple and len(brightness_range) == 2) or (
                type(brightness_range) == list and len(brightness_range)
            ) == 2:
                if (
                    type(brightness_range[0]) == float
                    and type(brightness_range[1]) == float
                ):
                    brightness_range = str(brightness_range)
                    self.__brightness_range = brightness_range
                    self.__remove_error_method()
                else:
                    error_msg = (
                        "brightness_range:provide float values for brightness_range\n"
                    )
                    self.__print_error(error_msg)
            else:
                error_msg = "brightness_range:Please provide tuple of two floats for brightness_range\n"
                self.__print_error(error_msg)
        else:
            if type(brightness_range) == float:
                brightness_range = str(brightness_range)
                self.__brightness_range = brightness_range
                self.__remove_error_method()
            else:
                error_msg = (
                    "brightness_range:provide float value for brightness_range\n"
                )
                self.__print_error(error_msg)

    def shear_range(self, shear_range: float):
        """
        Float. Shear Intensity (Shear angle in counter-clockwise direction in degrees)
        example: trainingObject.shear_range(0.2)
        default: 0.0
        """
        if type(shear_range) == float:
            self.__shear_range = shear_range
            self.__remove_error_method()
        else:
            error_msg = "shear_range:Invalid input type given for shear_range\n"
            self.__print_error(error_msg)

    def zoom_range(self, zoom_range):
        """
        Float or [lower, upper]. Range for random zoom. If a float, [lower, upper] = [1-zoom_range, 1+zoom_range].
        example: trainingObject.zoom_range(0.2)
        default: 0.0
        """
        if type(zoom_range) == float or type(zoom_range) == list:
            self.__zoom_range = zoom_range
            self.__remove_error_method()
        else:
            error_msg = "zoom_range:Invalid input type given for zoom_range\n"
            self.__print_error(error_msg)

    def channel_shift_range(self, channel_shift_range: float):
        """
        Float. Range for random channel shifts.
        example: trainingObject.channel_shift_range(0.4)
        default: 0.0
        """
        if self.__framework == PYTORCH_FRAMEWORK and self.__image_type != "rgb":
            error_msg = "channel_shift_range:You can not set channel_shift_range if image type is not rgb\n"
            self.__print_error(error_msg)
        elif type(channel_shift_range) == float:
            self.__channel_shift_range = channel_shift_range
            self.__remove_error_method()
        elif self.__framework == SKLEARN_FRAMEWORK:
            self.__not_supported_parameters(
                "channel_shift_range", framework=SKLEARN_FRAMEWORK
            )
            self.__remove_error_method()
        else:
            error_msg = (
                "channel_shift_range:Invalid input type given for channel_shift_range\n"
            )
            self.__print_error(error_msg)

    def fill_mode(self, fill_mode: str):
        """
        Set fill mode
        parameters: string type values .
        default: 'constant'

        supported fill_mode functions: ["constant", "nearest", "reflect", "wrap"] for tensorflow
        supported fill_mode functions: ["constant", "edge", "symmetric", "reflect", "wrap"] for pytorch

        example: trainingObject.fill_mode("nearest")
        """
        if self.__framework == TENSORFLOW_FRAMEWORK:
            f = ["constant", "nearest", "reflect", "wrap"]
        elif self.__framework == PYTORCH_FRAMEWORK:
            f = ["constant", "edge", "symmetric", "reflect", "wrap"]
        else:
            f = ["mean", "median", "mode"]
        try:
            f.index(fill_mode.lower())
            self.__fill_mode = fill_mode.lower()
            if self.__fill_mode != f[0]:
                self.cval(0.0)
            self.__remove_error_method()
        except:
            error_msg = f"fill_mode:Please provide supported fill modes: {f}\n"
            self.__print_error(error_msg)

    def cval(self, cval: float):
        """
        Float or Int. Value used for points outside the boundaries when fill_mode = "constant".
        example: trainingObject.cval(0.3)
        default: 0.0
        """
        if type(cval) == float:
            self.__cval = cval
            self.__remove_error_method()
            if self.__framework == PYTORCH_FRAMEWORK:
                self.__fill_mode = "constant"
        elif self.__framework == SKLEARN_FRAMEWORK:
            self.__not_supported_parameters("cval", framework=SKLEARN_FRAMEWORK)
            self.__remove_error_method()
        else:
            error_msg = "cval:Invalid input type given for cval\n"
            self.__print_error(error_msg)

    def horizontal_flip(self, horizontal_flip: bool):
        """
        Boolean. Randomly flip inputs horizontally.
        example: trainingObject.horizontal_flip(True)
        default: False
        """
        if self.__framework == TENSORFLOW_FRAMEWORK:
            if type(horizontal_flip) == bool:
                self.__horizontal_flip = horizontal_flip
                self.__remove_error_method()
            else:
                error_msg = (
                    "horizontal_flip:Invalid input type given for horizontal_flip\n"
                )
                self.__print_error(error_msg)
        else:
            self.__not_supported_parameters(
                "horizontal_flip", framework=self.__framework
            )
            self.__remove_error_method()

    def vertical_flip(self, vertical_flip: bool):
        """
        Boolean. Randomly flip inputs vertically.
        example: trainingObject.vertical_flip(True)
        default: False
        """
        if self.__framework == TENSORFLOW_FRAMEWORK:
            if type(vertical_flip) == bool:
                self.__vertical_flip = vertical_flip
                self.__remove_error_method()
            else:
                error_msg = "vertical_flip:Invalid input type given for vertical_flip\n"
                self.__print_error(error_msg)
        else:
            self.__not_supported_parameters("vertical_flip", framework=self.__framework)
            self.__remove_error_method()

    def rescale(self, rescale: float):
        """
        rescaling factor. Defaults to None. If None, no rescaling is applied,
        otherwise we multiply the data by the value provided (after applying all other transformations).
        example: trainingObject.rescale(0.003921568627)
        default: None
        """
        if self.__framework == SKLEARN_FRAMEWORK:
            if isinstance(rescale, tuple) and rescale[0] < rescale[1]:
                self.__rescale = rescale
                self.__remove_error_method()
            else:
                error_msg = ("rescale: Please provide a tuple having min and max range where max is greater than min. "
                             "First min and then max in tuple\n")
                self.__print_error(error_msg)
        else:
            if isinstance(rescale, float):
                self.__rescale = rescale
                self.__remove_error_method()
            else:
                error_msg = "rescale:Invalid input type given for rescale\n"
                self.__print_error(error_msg)

    def shuffle(self, shuffle: bool):
        """
        whether to shuffle the data (default: True)
        example: trainingObject.shuffle(False)
        default: True
        """
        if type(shuffle) == bool:
            self.__shuffle = shuffle
            self.__remove_error_method()
        else:
            error_msg = "shuffle:Invalid input type given for shuffle\n"
            self.__print_error(error_msg)

    def get_features(self):
        feature_list = [
            "BP_CurrentCurve",
            "BP_VoltageCurve",
            "BP_ReferenceCurveLength",
            "BP_PSF",
            "BP_UIP",
            "BP_Energy",
            "BP_gunResistance",
            "BP_MaxResistance",
            "BP_ResistanceDrop",
            "BP_MeanVoltage",
            "BP_MeanPulse",
            "BP_MeanCurrent",
            "BP_meanCurrentSec",
            "BP_meanCurrentPrim",
            "BP_MeanResistance",
            "BP_Length",
            "BP_RmaxTime",
            "BP_ProtocolLogNo",
            "BP_spatterTime",
            "BP_MonitorStdActualValue",
            "BP_MonitorStdReferenceValue",
            "WP_WeldJobName",
            "WELD_ID",
            "WP_STCReference",
            "WP_GunResistance",
            "VEHICLE_ID",
            "WP_WeldTime",
            "WP_TimeMillisecond",
            "WP_TimerName",
            "WP_TipWearState",
            "WP_UnixEpoch",
            "WP_TipDressCount",
            "WP_TipWearCount",
            "WP_DiDt",
            "WP_Expulsion",
            "WP_Energy",
            "WP_Comment",
            "measurement_id",
            "inspection_id",
            "time_stamp_x",
            "nugget1",
            "nugget2",
            "indentation1",
            "indentation2",
            "frontplate1",
            "frontplate2",
            "stack1",
            "stack2",
            "pass_fg",
            "reason",
            "cscans",
            "meta_x",
            "time_stamp_y",
            "inspector_id",
            "inspection_mode",
            "meta_y",
            "update_status",
            "min_size",
            "setup_size",
            "min_ind",
            "max_ind",
            "stack_3T",
            "safety_fg",
            "robot_id",
            "robot_desc",
            "schedule",
            "cscans_integers",
            "cscan1",
            "cscan2",
            "resistance",
        ]
        method_list = [
            "product",
            "ratio",
            "sum",
            "polynomial",
            "outlier simulation",
            "shuffle",
            "pca",
        ]
        example = {
            "product": "{'feature1': feature1, 'feature2': feature2, 'method':product}",
            "ratio": "{'feature1': feature1, 'feature2': feature2, 'method':ratio}",
            "sum": "{'feature1': feature1, 'feature2': feature2, 'method':sum}",
            "polynomial": "{'feature1': feature1, 'feature2': feature2, 'method':polynomial}",
            "outlier simulation": "{'feature1': feature1, 'feature2': None, 'method':outlier simulation} or {'feature1': feature1, 'method':outlier simulation}",
            "shuffle": "{'feature1': feature1, 'feature2': None, 'method':shuffle} or {'feature1': feature1, 'method':shuffle}",
            "pca": "{'feature1': feature1, 'feature2': None, 'method':pca} or {'feature1': feature1, 'method':pca}",
        }
        pprint.pprint(f"The feature list is {feature_list}")
        pprint.pprint(f"The method options are: {method_list}")
        pprint.pprint(f"The example for each method use are: {example}")

    def feature_interaction(self, dict):
        """
        create new feature and provide both feature name and its interaction method
        example: trainingObject.feature_interaction({'feature1': feature1, 'feature2': feature2(can be None for 'outlier simulation', 'shuffle', 'pca'), 'method':method})
        default: None
        """
        feature_list = [
            "BP_CurrentCurve",
            "BP_VoltageCurve",
            "BP_ReferenceCurveLength",
            "BP_PSF",
            "BP_UIP",
            "BP_Energy",
            "BP_gunResistance",
            "BP_MaxResistance",
            "BP_ResistanceDrop",
            "BP_MeanVoltage",
            "BP_MeanPulse",
            "BP_MeanCurrent",
            "BP_meanCurrentSec",
            "BP_meanCurrentPrim",
            "BP_MeanResistance",
            "BP_Length",
            "BP_RmaxTime",
            "BP_ProtocolLogNo",
            "BP_spatterTime",
            "BP_MonitorStdActualValue",
            "BP_MonitorStdReferenceValue",
            "WP_WeldJobName",
            "WELD_ID",
            "WP_STCReference",
            "WP_GunResistance",
            "VEHICLE_ID",
            "WP_WeldTime",
            "WP_TimeMillisecond",
            "WP_TimerName",
            "WP_TipWearState",
            "WP_UnixEpoch",
            "WP_TipDressCount",
            "WP_TipWearCount",
            "WP_DiDt",
            "WP_Expulsion",
            "WP_Energy",
            "WP_Comment",
            "measurement_id",
            "inspection_id",
            "time_stamp_x",
            "nugget1",
            "nugget2",
            "indentation1",
            "indentation2",
            "frontplate1",
            "frontplate2",
            "stack1",
            "stack2",
            "pass_fg",
            "reason",
            "cscans",
            "meta_x",
            "time_stamp_y",
            "inspector_id",
            "inspection_mode",
            "meta_y",
            "update_status",
            "min_size",
            "setup_size",
            "min_ind",
            "max_ind",
            "stack_3T",
            "safety_fg",
            "robot_id",
            "robot_desc",
            "schedule",
            "cscans_integers",
            "cscan1",
            "cscan2",
            "resistance",
        ]
        method_list = [
            "product",
            "ratio",
            "sum",
            "polynomial",
            "outlier simulation",
            "shuffle",
            "pca",
        ]
        if dict["feature1"] not in feature_list:
            error_msg = "feature_interaction: Invalid feature name provided\n"
            self.__print_error(error_msg)
        elif "feature2" in dict.keys() and dict["feature2"] not in feature_list:
            error_msg = "feature_interaction: Invalid feature name provided\n"
            self.__print_error(error_msg)
        elif dict["method"] not in method_list:
            error_msg = "feature_interaction: Invalid method name provided\n"
            self.__print_error(error_msg)
        else:
            new_interaction = {
                "feature1": dict["feature1"],
                "feature2": dict["feature2"] if "feature2" in dict.keys() else None,
                "method": dict["method"],
            }
            interaction_exist = False
            for interaction in self.__feature_interaction:
                if new_interaction == interaction:
                    interaction_exist = True
            if not interaction_exist:
                self.__feature_interaction.append(new_interaction)
            self.__remove_error_method()

    # def category(self, category: str):
    #     """
    #     String.
    #     Category of experiment, like classification
    #     example:trainingObject.category('classification')
    #     default_value: 'Classification'
    #
    #     """
    #     if type(category) == str:
    #         self.__category = category
    #     else:
    #         print("Invalid input type given for category\n\n")
    #
    # def modelType(self, modelType: str):
    #     """
    #     String.
    #     Type of model used in the experiment, like VGGNET
    #     example:trainingObject.modelType('VGGNET')
    #
    #
    #     """
    #     if type(modelType) == str:
    #         self.__modelType = modelType
    #     else:
    #         print("Invalid input type given for modelType\n\n")
    #
    # def stepsPerEpoch(self, stepsPerEpoch: int):
    #     """
    #     Integer.
    #     Total number of steps (batches of samples) before declaring
    #     one epoch finished and starting the next epoch.
    #     example: setStepsPerEpoch(5)
    #     default: None
    #     """
    #     if type(stepsPerEpoch) == int and stepsPerEpoch >= 15:
    #         self.__stepsPerEpoch = stepsPerEpoch
    #     else:
    #         print(
    #             "Invalid input type or value less than 15 given for stepsPerEpoch\n\n"
    #         )
    #
    # def initialEpoch(self, initialEpoch: int):
    #     """
    #     Integer. Epoch at which to start training
    #     (useful for resuming a previous training run).
    #     example: setInitialEpoch(2)
    #     default: 0
    #     """
    #     if type(initialEpoch) == int:
    #         self.__initialEpoch = initialEpoch
    #     else:
    #         print("Invalid input type given for initialEpoch\n\n")
    #
    # def validationSteps(self, validationSteps: int):
    #     """
    #     Integer. Total number of steps (batches of samples) to draw before stopping
    #     when performing validation at the end of every epoch.
    #     example: setValidationSteps(20)
    #     default: None
    #     """
    #     if type(validationSteps) == int and validationSteps >= 15:
    #         self.__validationSteps = validationSteps
    #     else:
    #         print(
    #             "Invalid input type or value less than 15 given for validationSteps\n\n"
    #         )
    # def featurewise_center(self, featurewise_center: bool):
    #     """
    #     Boolean. Set input mean to 0 over the dataset, feature-wise.
    #     example: trainingObject.featurewise_center(True)
    #     default: False
    #
    #
    #     """
    #     if type(featurewise_center) == bool:
    #         self.__featurewise_center = featurewise_center
    #     else:
    #         print("Invalid input type given for featurewise_center\n\n")
    #
    # def featurewise_std_normalization(self, featurewise_std_normalization: bool):
    #     """
    #     Boolean. Divide inputs by std of the dataset, feature-wise.
    #     example: trainingObject.featurewise_std_normalization(True)
    #     default: False
    #
    #
    #     """
    #     if type(featurewise_std_normalization) == bool:
    #         self.__featurewise_std_normalization = featurewise_std_normalization
    #     else:
    #         print("Invalid input type given for featurewise_std_normalization\n\n")
    #
    # def zca_whitening(self, zca_whitening: bool):
    #     """
    #     Boolean. Apply ZCA whitening.
    #     example: trainingObject.zca_whitening(True)
    #     default: False
    #
    #
    #     """
    #     if type(zca_whitening) == bool:
    #         self.__zca_whitening = zca_whitening
    #     else:
    #         print("Invalid input type given for zca_whitening\n\n")
    #
    # def data_format(self, data_format: str):
    #     """
    #     String.
    #     Image data format, either "channels_first" or "channels_last".
    #     "channels_last" mode means that the images should have shape
    #     (samples, height, width, channels),
    #     "channels_first" mode means that the images should have shape
    #     (samples, channels, height, width).
    #     example: setDataFormat("channels_first")
    #     default: None
    #     """
    #     d = ["channels_last"]
    #     try:
    #         d.index(data_format.lower())
    #         self.__data_format = data_format.lower()
    #     except:
    #         print(f"Please provide supported fill modes: {d}\n\n")
    #
    # def dtype(self, dtype: str):
    #     """
    #     String.
    #     Dtype to use for the generated arrays.
    #     example: dtype('float32')
    #     default: None
    #     """
    #     d = ["float32", "float64"]
    #     try:
    #         d.index(dtype.lower())
    #         self.__dtype = dtype.lower()
    #     except:
    #         print(f"Please provide supported fill modes: {d}\n\n")
    #
    # def metrics(self,metrics:list):
    #   '''
    #   List of strings.
    #   List of metrics to be evaluated by the model
    #   during training and testing.
    #   example: setMetrics(['accuracy','mse'])
    #   default: ['accuracy']
    #   '''
    #   if type(metrics)== list and all(isinstance(sub, str) for sub in metrics):
    #       metrics = str(metrics)
    #       self.__metrics = metrics
    #   else:
    #       print("Provide values as list of strings")
    #
    #   def __display_time(self,seconds, granularity=5):
    #       intervals = (
    #       ('weeks', 604800),  # 60 * 60 * 24 * 7
    #       ('days', 86400),    # 60 * 60 * 24
    #       ('hours', 3600),    # 60 * 60
    #       ('minutes', 60),
    #       ('seconds', 1),)
    #       result = []
    #
    #       for name, count in intervals:
    #           value = seconds // count
    #           if value:
    #               seconds -= value * count
    #               if value == 1:
    #                   name = name.rstrip('s')
    #               result.append("{} {}".format(value, name))
    #       return ', '.join(result[:granularity])
    #
    #   def getEstimate(self):
    #
    #       header = {'Authorization' : f"Token {self.__token}"}
    #       re = requests.post(f"{self.__url}flops/",headers= header,data={'datasetId':self.__datasetId,
    #           'batchSize':self.__batchSize,'noOfEpochs':self.__epochs,'modelName':self.__modelName})
    # #         print(re.status_code)
    #       if re.status_code == 200:
    #
    #           body_unicode = re.content.decode('utf-8')
    #           content = int(json.loads(body_unicode))
    #           self.__upperboundTime = content
    #           cycleTime = content * self.__cycles
    #           display = self.__display_time(cycleTime)
    #
    #           print(f"It will take around {display} to complete {self.__cycles} cycles for given training plan.")

    def enable_lora(self, lora_enable: bool = False):
        assert isinstance(lora_enable, bool), "lora_enable must be a boolean."
        self.__lora_enable = lora_enable

    def set_lora_parameters(
        self, lora_r: int, lora_alpha: int, lora_dropout: float, q_lora: bool
    ):
        assert self.__lora_enable == True, "Enable lora first using enable_lora"
        """
        Set parameters related to LoRA.

        Parameters:
        - lora_r (int): The rank for the LoRA layer. Must be a positive integer.
        - lora_alpha (int): The scaling factor alpha for LoRA. Must be a positive integer.
        - lora_dropout (float): The dropout rate for LoRA layers. Must be a float between 0 and 1.
        - q_lora (bool): Whether to enable or disable Q LoRA.

        Examples:
            trainingObject.set_lora_parameters(256, 512, 0.05, False)

        Defaults:
            lora_r: 256, lora_alpha: 512, lora_dropout: 0.05, q_lora: False
        """
        if self.__category != TEXT_CLASSIFICATION:
            print(
                "Operation not allowed. This function only works for language models."
            )
            return  # Early exit

        try:
            assert (
                isinstance(lora_r, int) and lora_r > 0
            ), "lora_r must be a positive integer."
            assert (
                isinstance(lora_alpha, int) and lora_alpha > 0
            ), "lora_alpha must be a positive integer."
            assert (
                isinstance(lora_dropout, float) and 0 <= lora_dropout <= 1
            ), "lora_dropout must be a float between 0 and 1."
            assert isinstance(q_lora, bool), "q_lora must be a boolean."

            # If all assertions pass, set the parameters
            self.__lora_r = lora_r
            self.__lora_alpha = lora_alpha
            self.__lora_dropout = lora_dropout
            self.__q_lora = q_lora

            # Remove previous errors if any
            self.__remove_error_method()

        except AssertionError as e:
            self.__print_error(str(e))

    def __checkTrainingPlan(self):
        # call API to compare current training plan for duplication
        header = {"Authorization": f"Token {self.__token}"}
        data = self.__get_params_training()
        # print(data,"\n\n")
        re = requests.post(
            f"{self.__url}trainingplan/{self.__datasetId}/",
            headers=header,
            json=data,
        )
        # print(re.text)
        if re.status_code == 200:
            body_unicode = re.content.decode("utf-8")
            content = json.loads(body_unicode)
            # print(content)
            if content["status"]:
                userResponse = input(
                    "You already have an experiment with current Training Plan want to proceed?\n\n"
                )
                if userResponse.lower() == "yes" or userResponse.lower() == "y":
                    return True
                elif userResponse.lower() == "no" or userResponse.lower() == "n":
                    return False
                else:
                    text = colored(f"Training Plan:Please Enter Valid Input\n", "red")
                    print(text, "\n")
            else:
                return True

    def start(self):
        if not self.__eligibility_passed:
            text = colored(
                f"Error: Not all Training Parameters are set properly.\n", "red"
            )
            print(text, "\n")
            return
        # set callbacks
        self.__setCallbacks()
        # call checkTrainingPlan for duplication check
        duplication = self.__checkTrainingPlan()
        if duplication:
            # Create Experiment
            header = {"Authorization": f"Token {self.__token}"}
            re = requests.post(
                f"{self.__url}experiments/", headers=header, data=self.__getParameters()
            )
            if re.status_code == 201:
                body_unicode = re.content.decode("utf-8")
                content = json.loads(body_unicode)
                text = colored(
                    f"Experiment created with id:{content['experimentKey']}", "green"
                )
                print(text, "\n")
                explink = (
                    self.__experimenturl
                    + self.__datasetId
                    + "/"
                    + content["experimentKey"]
                    + "/"
                )
                # data = {"experiment_id": content["id"]}
                # Send training request to server
                # r = requests.post(f"{self.__url}training/", headers=header, data=data)
                # body_unicode = r.content.decode("utf-8")
                # content = json.loads(body_unicode)
                print("Training request sent....")
                print(
                    "Updated weights will be available to download once training completed"
                )
                print("\n")
                print(" Link to Experiment is : " + str(explink))
                print(" Training Plan Information for Experiment is :")
                self.getTrainingPlan()
            elif re.status_code == 403:
                body_unicode = re.content.decode("utf-8")
                content = json.loads(body_unicode)
                message = content["message"]
                text = colored(message, "red")
                print(text, "\n")
            elif re.status_code == 400:
                text = colored("Error:Mandatory Fields Missing", "red")
                print(text, "\n")
            else:
                if self._environment != "production":
                    print(re.content, "\n")
                text = colored(
                    "Error:Experiment creation Failed. Please ensure you have entered correct parameters.",
                    "red",
                )
                print(text, "\n")
            self.resetTrainingPlan()

    def __getParameters(self):
        parameters = {
            "message": "training",
            "datasetId": self.__datasetId,
            "epochs": self.__epochs,
            "cycles": self.__cycles,
            "modelName": self.__modelId,
            "optimizer": self.__optimizer,
            "lossFunction": json.dumps(self.__lossFunction),
            "learningRate": json.dumps(self.__learningRate),
            "batchSize": self.__batchSize,
            "seed": self.__seed,
            "featurewise_center": self.__featurewise_center,
            "samplewise_center": self.__samplewise_center,
            "featurewise_std_normalization": self.__featurewise_std_normalization,
            "samplewise_std_normalization": self.__samplewise_std_normalization,
            "zca_whitening": self.__zca_whitening,
            "rotation_range": self.__rotation_range,
            "width_shift_range": self.__width_shift_range,
            "height_shift_range": self.__height_shift_range,
            "brightness_range": self.__brightness_range,
            "shear_range": self.__shear_range,
            "zoom_range": self.__zoom_range,
            "channel_shift_range": self.__channel_shift_range,
            "fill_mode": self.__fill_mode,
            "cval": self.__cval,
            "horizontal_flip": self.__horizontal_flip,
            "vertical_flip": self.__vertical_flip,
            "rescale": self.__rescale,
            "validation_split": self.__validation_split,
            "shuffle": self.__shuffle,
            "layersFreeze": self.__layers_non_trainable,
            "metrics": self.__metrics,
            "objective": self.__objective,
            "name": self.__name,
            "model_type": self.__model_type,
            "category": self.__category,
            "upperboundTime": self.__upperboundTime,
            "callbacks": self.__callbacks,
            "pre_trained_weights": self.__weights,
            "subdataset": self.__subdataset,
            "images_per_edge": json.dumps(self.__images_per_edge),
            "images_per_class": self.__images_per_class,
            "image_shape": self.__image_shape,
            "image_type": self.__image_type,
            "framework": self.__framework,
            "model_id": self.__model_id,
            "hf_token": self.__hf_token,
            "lora_enabled": self.__lora_enable,
            "lora_r": self.__lora_r,
            "lora_alpha": self.__lora_alpha,
            "lora_dropout": self.__lora_dropout,
            "q_lora": self.__q_lora,
            "model_parameters": self.__model_params,
            "utilisation_category": self.__utilisation_category,
            "feature_interaction": json.dumps(self.__feature_interaction),
        }

        return parameters

    def __get_params_training(self):
        parameters = {
            "message": "training",
            "datasetId": self.__datasetId,
            "epochs": self.__epochs,
            "cycles": self.__cycles,
            "modelName": self.__modelId,
            "optimizer": self.__optimizer,
            "lossFunction": json.dumps(self.__lossFunction),
            "learningRate": json.dumps(self.__learningRate),
            "batchSize": self.__batchSize,
            "seed": self.__seed,
            "featurewise_center": self.__featurewise_center,
            "samplewise_center": self.__samplewise_center,
            "featurewise_std_normalization": self.__featurewise_std_normalization,
            "samplewise_std_normalization": self.__samplewise_std_normalization,
            "zca_whitening": self.__zca_whitening,
            "rotation_range": self.__rotation_range,
            "width_shift_range": self.__width_shift_range,
            "height_shift_range": self.__height_shift_range,
            "brightness_range": self.__brightness_range,
            "shear_range": self.__shear_range,
            "zoom_range": self.__zoom_range,
            "channel_shift_range": self.__channel_shift_range,
            "fill_mode": self.__fill_mode,
            "cval": self.__cval,
            "horizontal_flip": self.__horizontal_flip,
            "vertical_flip": self.__vertical_flip,
            "rescale": self.__rescale,
            "validation_split": self.__validation_split,
            "shuffle": self.__shuffle,
            "layersFreeze": self.__layers_non_trainable,
            "metrics": self.__metrics,
            "objective": self.__objective,
            "name": self.__name,
            "model_type": self.__model_type,
            "category": self.__category,
            "upperboundTime": self.__upperboundTime,
            "callbacks": self.__callbacks,
            "pre_trained_weights": self.__weights,
            "subdataset": self.__subdataset,
            "image_shape": self.__image_shape,
            "image_type": self.__image_type,
            "framework": self.__framework,
            "model_id": self.__model_id,
            "hf_token": self.__hf_token,
            "lora_enabled": self.__lora_enable,
            "lora_r": self.__lora_r,
            "lora_alpha": self.__lora_alpha,
            "lora_dropout": self.__lora_dropout,
            "q_lora": self.__q_lora,
            "model_parameters": self.__model_params,
            "utilisation_category": self.__utilisation_category,
            "feature_interaction": json.dumps(self.__feature_interaction),
        }

        return parameters

    def getTrainingPlan(self):
        if self.__eligibility_passed:
            print(
                f" \033[1mTraining Description\033[0m\n\n",
                f"experimentName: {self.__name}\n",
                f"modelName: {self.__modelName}\n",
                f"objective: {self.__objective}\n",
                f"\n \033[1mDataset Parameters\033[0m\n\n",
                f"datasetId: {self.__datasetId}\n",
                f"totalDatasetSize: {self.__totalDatasetSize}\n",
                f"allClasses: {self.__class_names}\n\n",
                f"trainingDatasetSize: {self.__trainingDatasetSize}\n",
                f"trainingClasses: {self.__trainingClasses}\n",
                f"imageShape: {self.__image_shape}\n",
                f"imageType: {self.__image_type}\n",
                f"seed: {self.__seed}\n",
                "\n \033[1mTraining Parameters\033[0m\n\n",
                f"epochs: {self.__epochs}\n",
                f"cycles: {self.__cycles}\n",
                f"batchSize: {self.__batchSize}\n",
                f"validation_split: {self.__validation_split}\n",
                "\n \033[1mHyperparameters\033[0m\n\n",
                f"optimizer: {self.__optimizer}\n",
                f"lossFunction: {self.__lossFunction}\n",
                f"learningRate: {self.__learningRate}\n",
                f"layersFreeze: {self.__layers_non_trainable}\n",
                f"earlystopCallback: {self.__earlystopCallback}\n",
                f"reducelrCallback: {self.__reducelrCallback}\n",
                f"modelCheckpointCallback: {self.__modelCheckpointCallback}\n",
                f"terminateOnNaNCallback: {self.__terminateOnNaNCallback}\n",
                "\n \033[1mAugmentation Parameters\033[0m\n\n",
                f"brightness_range: {self.__brightness_range}\n",
                f"channel_shift_range: {self.__channel_shift_range}\n",
                f"cval: {self.__cval}\n",
                f"fill_mode: {self.__fill_mode}\n",
                f"height_shift_range: {self.__height_shift_range}\n",
                f"horizontal_flip: {self.__horizontal_flip}\n",
                f"rescale: {self.__rescale}\n",
                f"rotation_range: {self.__rotation_range}\n",
                f"samplewise_center: {self.__samplewise_center}\n",
                f"samplewise_std_normalization: {self.__samplewise_std_normalization}\n",
                f"shear_range: {self.__shear_range}\n",
                f"shuffle: {self.__shuffle}\n",
                f"vertical_flip: {self.__vertical_flip}\n",
                f"width_shift_range: {self.__width_shift_range}\n",
                f"zoom_range: {self.__zoom_range}\n",
                f"feature_interaction: {self.__feature_interaction}\n",
                "\n \033[1mLLM Parameters\033[0m\n\n",
                f"model_id: {self.__model_id}\n",
                f"lora_enable: {self.__lora_enable}\n",
                f"lora_r: {self.__lora_r}\n",
                f"lora_alpha: {self.__lora_alpha}\n",
                f"lora_dropout: {self.__lora_dropout}\n",
                f"q_lora: {self.__q_lora}\n",
            )
        else:
            print("Error: Not all Training Parameters are set properly\n")
            return
