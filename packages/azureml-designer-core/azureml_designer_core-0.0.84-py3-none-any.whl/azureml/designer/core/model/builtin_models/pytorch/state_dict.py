import importlib
from pathlib import Path

import torch

from azureml.designer.core.model.builtin_models.pytorch.base import PytorchBaseModel
from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.designer.core.model.model_spec.builtin_model_meta.builtin_model_meta import BuiltinModelMeta
from azureml.studio.core.logger import get_logger
from azureml.studio.core.error import PathExistsError, ModelSpecKeyError, ModelSpecValueError

logger = get_logger(__name__)


class PytorchStateDictModel(PytorchBaseModel):

    def save(self, save_to: Path, overwrite_if_exists=True):
        if save_to.exists() and not overwrite_if_exists:
            raise PathExistsError(save_to)
        state_dict = self.raw_model.state_dict()
        torch.save(state_dict, save_to)

    @classmethod
    def load_with_model_meta(cls, load_from: Path, model_meta: BuiltinModelMeta):
        flavor_extras = model_meta.flavor_extras or {}
        model_module_name = flavor_extras.get(ModelSpecConstants.MODEL_MODULE_KEY, None)
        if not model_module_name:
            logger.warning("No model_module specified, using nn.Module as default.")
            model_class = torch.nn.Module
        else:
            model_class_name = flavor_extras.get(ModelSpecConstants.MODEL_CLASS_KEY, None)
            if not model_class_name:
                raise ModelSpecKeyError(detail=f'model_class has to be specified if model_module is specified. '
                                               f'flavor_extras = {flavor_extras}')
            try:
                logger.info(f"Trying to import {model_module_name}")
                model_module = importlib.import_module(model_module_name)
                model_class = getattr(model_module, model_class_name)
            except (ImportError, AttributeError) as e:
                raise ModelSpecValueError(
                    detail=f"Failed to load {model_class_name} from {model_module_name}. "
                           f"flavor_extras = {flavor_extras}",
                    caused_ex=e
                ) from e

        init_params = flavor_extras.get(ModelSpecConstants.INIT_PARAMS_KEY, {})
        logger.info(f"Trying to initialize model by calling {model_class}({init_params})")
        model = model_class(**init_params)
        model.load_state_dict(torch.load(str(load_from), map_location=torch.device('cpu')))

        return cls(model, model_meta)
