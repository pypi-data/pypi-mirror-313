from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.designer.core.model.core_model import CoreModel
from azureml.designer.core.model.model_spec.builtin_model_meta.builtin_model_meta import BuiltinModelMeta
from azureml.designer.core.model.model_spec.builtin_model_meta.label_map import LabelMap
from azureml.designer.core.model.model_spec.builtin_model_meta.task_type import TaskType
from azureml.designer.core.model.model_spec.serving_config import ServingConfig
from azureml.designer.core.model.generic_model import GenericModel
from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


def save_generic_model(
    model: CoreModel,
    path: str = ModelSpecConstants.DEFAULT_ARTIFACT_SAVE_PATH,
    conda: dict = None,
    local_dependencies: list = None,
    serving_config: ServingConfig = None,
    overwrite_if_exists: bool = True
):
    generic_model = GenericModel(
        core_model=model,
        conda=conda,
        local_dependencies=local_dependencies,
        serving_config=serving_config
    )
    generic_model.save(
        artifact_path=path,
        model_relative_path=ModelSpecConstants.CUSTOM_MODEL_DIRECTORY,
        overwrite_if_exists=overwrite_if_exists
    )


def load_generic_model(
    path: str = ModelSpecConstants.DEFAULT_ARTIFACT_SAVE_PATH,
    install_dependencies: bool = False
):
    return GenericModel.load(artifact_path=path, install_dependencies=install_dependencies)


def get_pytorch_state_dict_model(
        pytorch_model,
        init_params: dict = None,
        inputs: list = None,
        outputs: list = None,
        task_type: TaskType = None,
        label_map=None,
):
    from .builtin_models.pytorch.state_dict import PytorchStateDictModel
    nn_module_model = pytorch_model
    is_cuda = next(nn_module_model.parameters()).is_cuda
    logger.info(f"Saving model with is_cuda={is_cuda}")
    flavor_extras = {
        ModelSpecConstants.MODEL_MODULE_KEY: nn_module_model.__class__.__module__,
        ModelSpecConstants.MODEL_CLASS_KEY: nn_module_model.__class__.__name__,
        ModelSpecConstants.IS_CUDA_KEY: is_cuda,
        ModelSpecConstants.INIT_PARAMS_KEY: init_params
    }
    label_map = LabelMap.create(label_map)
    builtin_model_meta = BuiltinModelMeta(
        flavor_extras=flavor_extras,
        model_inputs=inputs,
        model_outputs=outputs,
        task_type=task_type,
        label_map=label_map
    )
    return PytorchStateDictModel(nn_module_model, builtin_model_meta)


def save_pytorch_state_dict_model(
        pytorch_model,
        init_params: dict = None,
        path: str = ModelSpecConstants.DEFAULT_ARTIFACT_SAVE_PATH,
        conda=None,
        local_dependencies: list = None,
        inputs: list = None,
        outputs: list = None,
        task_type: TaskType = None,
        label_map=None,
        serving_config: ServingConfig = None,
        overwrite_if_exists: bool = True
):
    save_generic_model(
        model=get_pytorch_state_dict_model(
            pytorch_model=pytorch_model,
            init_params=init_params,
            inputs=inputs,
            outputs=outputs,
            task_type=task_type,
            label_map=label_map,
        ),
        path=path,
        conda=conda,
        local_dependencies=local_dependencies,
        serving_config=serving_config,
        overwrite_if_exists=overwrite_if_exists
    )
