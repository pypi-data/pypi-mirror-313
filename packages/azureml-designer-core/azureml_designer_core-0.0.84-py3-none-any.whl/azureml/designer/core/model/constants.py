# Copied from azureml.studio.modules.ml.common.constants
# TODO: Support image generation and other task type


class ModelSpecConstants:
    # Top level keys in model_spec
    FLAVOR_KEY = "flavor"
    FLAVOR_EXTRAS_KEY = "flavor_extras"
    MODEL_FILE_KEY = "model_file"
    CONDA_FILE_KEY = "conda_file"
    LOCAL_DEPENDENCIES_KEY = "local_dependencies"
    INPUTS_KEY = "inputs"
    OUTPUTS_KEY = "outputs"
    SERVING_CONFIG_KEY = "serving_config"
    DESCRIPTION_KEY = "description"
    TIME_CREATED_KEY = "time_created"

    # Flavor specified keys in model_spec
    FLAVOR_NAME_KEY = "name"
    SERIALIZATION_METHOD_KEY = "serialization_method"
    MODEL_CLASS_KEY = "class"
    MODEL_MODULE_KEY = "module"
    IS_CUDA_KEY = "is_cuda"
    INIT_PARAMS_KEY = "init_params"

    # Machine learning task specified keys in model_spec
    TASK_TYPE_KEY = "task_type"
    LABEL_MAP_FILE_KEY = "label_map_file"

    # Serving Config
    GPU_SUPPORT_KEY = "gpu_support"
    CPU_CORE_NUM_KEY = "cpu_core_num"
    MEMORY_IN_GB_KEY = "memory_in_GB"

    # Others
    DEFAULT_ARTIFACT_SAVE_PATH = "./AzureMLModel"
    CONDA_FILE_NAME = "conda.yaml"
    CONDA_ENV_NAME = "project_environment"
    MODEL_SPEC_FILE_NAME = "model_spec.yaml"
    LOCAL_DEPENDENCIES_PATH = "local_dependencies"
    LOCAL_DEPENDENCIES_ZIP_FILE_NAME = f"{LOCAL_DEPENDENCIES_PATH}.zip"
    CUSTOM_MODEL_FLAVOR_NAME = "custom"
    CUSTOM_MODEL_DIRECTORY = "model"
    PICKLE_MODEL_FILE_NAME = "model.pkl"
    PYTORCH_STATE_DICT_FILE_NAME = "state_dict.pt"
    LABEL_MAP_FILE_NAME = "index_to_label.csv"
    LOCAL_DEPENDENCIES_PY_FILES_PATH = "pyfiles"

    # Model Inputs
    MODEL_INPUT_NAME_KEY = "name"
    MODEL_INPUT_VALUE_TYPE_KEY = "value_type"
    MODEL_INPUT_DEFAULT_KEY = "default"
    MODEL_INPUT_DESCRIPTION_KEY = "description"
    MODEL_INPUT_OPTIONAL_KEY = "optional"
    MODEL_INPUT_PRE_PROCESSOR_KEY = "pre_processor"

    # PreProcessor
    PRE_PROCESSOR_MODULE_KEY = "module"
    PRE_PROCESSOR_CLASS_KEY = "class"
    PRE_PROCESSOR_INIT_PARAMS_KEY = "init_params"


class ScoreColumnConstants:
    # Label and Task Type Region
    BinaryClassScoredLabelType = "Binary Class Assigned Labels"
    MultiClassScoredLabelType = "Multi Class Assigned Labels"
    RegressionScoredLabelType = "Regression Assigned Labels"
    ClusterScoredLabelType = "Cluster Assigned Labels"
    ScoredLabelsColumnName = "Scored Labels"
    ClusterAssignmentsColumnName = "Assignments"
    # Probability Region
    CalibratedScoreType = "Calibrated Score"
    ScoredProbabilitiesColumnName = "Scored Probabilities"
    ScoredProbabilitiesMulticlassColumnNamePattern = "Scored Probabilities"
    # Distance Region
    ClusterDistanceMetricsColumnNamePattern = "DistancesToClusterCenter no."
    # PytorchTensor Region
    TensorScoredLabelColumnName = "Tensor Output"
    # Temporary Column Names for Intermediate Results
    ScoredLabelIdsColumnName = "Scored Label Ids"
    ScoredProbabilitiesMulticlassColumnName = "Scored Probabilities List"


# Others
# For test env where package is installed from DevOps feed
DEV_OPS_EXTRA_INDEX_URL_PREFIX = "--extra-index-url=https://azureml-modules"
DESIGNER_PIP_PACKAGE_PREFIX = "azureml-designer-"
