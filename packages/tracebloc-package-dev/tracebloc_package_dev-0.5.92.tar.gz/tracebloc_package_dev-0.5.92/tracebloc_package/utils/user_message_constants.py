# Login user messages
USER_ARGUMENTS_ERROR = "The class does not take any arguments. Just run: user = User()"
USERNAME_POPUP_MESSAGE = "Enter your email address : "
PASSWORD_POPUP_MESSAGE = "Enter your password : "
LOGIN_SUCCESS = "Logged in as <username>"
LOGIN_FAILED = "Login credentials are not correct. Please try again."
LOGOUT_MESSAGE = "You have been logged out."
LOGOUT_FAILED = "Logout Failed. Retry!"
PROCEEDING_WITHOUT_LOGIN = (
    "You are not logged in. Please go back to ‘1. Connect to Tracebloc’ and proceed with "
    "logging in."
)

# uploading model and weights messages
# model checks messages
MyModel_MISSING = "Model file not provided as per docs: No function with name MyModel"
MyModel_ARGUMENTS_ERROR = (
    "Model file not provided as per docs: MyModel function receives no arguments"
)
LAYERS_SHAPE_ERROR = "Layers shape is not compatible with model input shape"
UNSUPPORTED_API = "Model file not provided as per docs: unsupported API used for Model"
UNSUPPORTED_LAYERS = "Layers in Model are not supported by Tensorflow"
TRAINING_ERROR = "Model doses-nt support training on image classification dataset."
MODEL_CHANNEL_ERROR = "Please provide model input shape with 3 channels"

# model file not found message
MODEL_NOT_FOUND = "Upload failed. There is no model with the name '<model name>' in your folder '<path given by user>'."

# model weights file not found message
WEIGHTS_NOT_FOUND = (
    "Weights Upload failed. No weights file found with the name '<modelname_weights.pkl>' in path "
    "'<path given by user>'. "
    "For more information check the [link=https://docs.tracebloc.io/user-uploadModel]docs[/link]"
)

# weights provided not compatible with model provided message
WEIGHTS_NOT_COMPATIBLE = (
    "Weights upload failed. Provide weights compatible with provided model."
    "For more information check the docs 'https://docs.tracebloc.io/weights'"
)

# Linking and setting Training plan
# setting training plan without uploading model
MODEL_NOT_UPLOADED = "Model not uploaded. Please first upload the model."
MODEL_LINK_FAILED = "Model Link Failed!"
DATASET_NOT_FOUND = (
    "Please provide a valid dataset ID.\n"
    "There is no dataset with ID: {datasetId} in your dataset table.\n"
)
LINKING_DATASET_MODEL_FAILED = (
    "Assignment failed!"
    "DataSet '<dataset Key>' expected parameters :"
    "classes : <dataset classes count>, shape: <shape required for provided dataset>"
    "classes : <model output classes>, shape: <model input shape>"
    "Please change your model parameters to match the datasets parameters."
    "Error Occured. Linking Failed!"
    "Communication Fail Error!"
)
LINKING_DATASET_MODEL_PASSED = "Assignment successful!" "Please set training plan."

# training plan messages
INVALID_CATEGORY = "Invalid input type given for category"
INVALID_MODEL_TYPE = "Invalid input type given for modelType"
INVALID_OBJECTIVE = "Invalid input type given for objective"
INVALID_EPOCHS = "Invalid input type or value '0' given for epochs"
INVALID_CYCLES = "Invalid input type or value '0' given for cycles"
INVALID_OPTIMIZER = (
    "Please provide supported optimizers: <list of all supported optimizer>"
)
INVALID_LOSS_FUNCTION = (
    "Please provide supported loss functions: <list of all supported loss functions>"
)
INVALID_LEARNING_RATE = "Invalid input type or value '0' given for learningRate"
INVALID_BATCH_SIZE = (
    "Invalid input type given for batchSize"
    "Please choose smaller batch size as dataset selected have less images"
)
INVALID_FEATUREWISE_CENTRE = "Invalid input type given for featurewise_center"
INVALID_SAMPLEWISE_CENTRE = "Invalid input type given for samplewise_center"
INVALID_FEATUREWISE_STD_NORMALIZATION = (
    "Invalid input type given for featurewise_std_normalization"
)
INVALID_SAMPLEWISE_STD_NORMALIZATION = (
    "Invalid input type given for samplewise_std_normalization"
)
INVALID_ZCA_WHITENING = "Invalid input type given for zca_whitening"
INVALID_ROTATION_RANGE = "Invalid input type given for rotation_range"
INVALID_WIDTH_SHIFT_RANGE = "Invalid input type given for width_shift_range"
INVALID_HEIGHT_SHIFT_RANGE = "Invalid input type given for height_shift_range"
INVALID_BRIGHTNESS_RANGE = (
    "provide float values for brightness_range"
    "Please provide tuple of two floats for brightness_range"
)
INVALID_SHEAR_RANGE = "Invalid input type given for shear_range"
INVALID_ZOOM_RANGE = "Invalid input type given for zoom_range"
INVALID_CHANNEL_SHIFT_RANGE = "Invalid input type given for channel_shift_range"
INVALID_FILL_MODE = "Please provide supported fill modes: <supported fill modes>"
INVALID_CVAL = "Invalid input type given for cval"
INVALID_HORIZONTAL_FLIP = "Invalid input type given for horizontal_flip"
INVALID_VERTICAL_FLIP = "Invalid input type given for vertical_flip"
INVALID_RESCALE = "Invalid input type given for rescale"
INVALID_VALIDATION_SPLIT = (
    "Invalid input type or set value not less than <minimum value calculated> for "
    "validation_split "
)
INVALID_SHUFFLE = "Invalid input type given for shuffle"
INVALID_LAYERS_FREEZE = "Provide values as list of strings for layersFreeze"
INVALID_MODEL_CHECKPOINT_CALLBACK = (
    "Please provide supported monitor values: <monitor values>"
    "Invalid datatype for arguments given for save_best_only"
)
INVALID_EARLY_STOP_CALLBACK = (
    "Please provide supported monitor values: <monitor values>"
    "Invalid datatype for arguments given for patience"
)
INVALID_REDUCE_LEARNING_RATE_CALLBACK = (
    "Please provide supported monitor values: <monitor values>"
    "Invalid datatype for arguments given for reducelrCallback"
)

# training plan duplication check
TRAINING_PLAN_DUPLICATION = (
    "You already have an experiment with current Training Plan want to proceed?"
)

# create experiment messages
START_TRAINING_WITH_INVALID_VALUE = "All fields in training plan are not correct"
EXPERIMENT_CREATED_MESSAGE = (
    "Experiment created with id: <experiment key received from server>}"
    "Training request sent...."
    "Updated weights will be available to download once training completed"
    " Link to Experiment is : "
    "<link to the experiment on frontend>"
    " Training Plan Information for Experiment is :"
    "<print training plan>"
)
EXPERIMENT_CREATED_FAILED = (
    "Mandatory Fields Missing"
    "Experiment creation Failed. Please ensure you have entered correct parameters."
)


# User.help() messages
HELP_MESSAGES = (
    "User is a method in this package which authenticates the user, provides access to Tracebloc, "
    "lets you upload your model, set the training plan and more. "
    "Only registered Users are allowed to access this package."
    "In order to authenticate, run cell."
    "Enter email register on tracebloc and password."
    "Other user attributes are uploadModel() and linkModelDataset()"
    "uploadModel():"
    "This helps user to upload a compatible model and weights."
    "linkModelDataset():"
    "Link uploaded model with a dataset."
    "For more information check the [link=https://docs.tracebloc.io/user-uploadModel]docs[/link]"
)
