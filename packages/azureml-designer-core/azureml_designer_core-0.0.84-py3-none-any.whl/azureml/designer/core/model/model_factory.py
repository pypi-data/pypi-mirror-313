import importlib
import inspect

from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.designer.core.model.builtin_models.builtin_model import BuiltinModel
from azureml.studio.core.error import ModelSpecKeyError, ModelSpecValueError
from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


class ModelClassFactory(object):
    """Get model class from flavor
    """
    @classmethod
    def get_model_class(cls, flavor: dict) -> type:
        if ModelSpecConstants.FLAVOR_NAME_KEY not in flavor:
            raise ModelSpecKeyError(
                load_from_path=None,
                detail=f"{ModelSpecConstants.FLAVOR_NAME_KEY} missing in flavor: {flavor}")
        flavor_name = flavor[ModelSpecConstants.FLAVOR_NAME_KEY].lower()
        if flavor_name == ModelSpecConstants.CUSTOM_MODEL_FLAVOR_NAME:
            try:
                module_path = flavor[ModelSpecConstants.MODEL_MODULE_KEY]
                class_name = flavor[ModelSpecConstants.MODEL_CLASS_KEY]
                module = importlib.import_module(module_path)
                return getattr(module, class_name)
            except KeyError as e:
                raise ModelSpecKeyError(
                    load_from_path=None,
                    detail=f"{ModelSpecConstants.MODEL_MODULE_KEY} and {ModelSpecConstants.MODEL_CLASS_KEY} "
                           f"are required in custom flavor, got {flavor}",
                    caused_ex=e
                ) from e
            except ModuleNotFoundError as e:
                raise ModelSpecValueError(
                    detail=f"Failed to load specified module {module_path}, "
                           f"please make sure the class definition exists in your dependencies. "
                           f"If you are loading an model in a new environment, "
                           f"please make sure to set install_dependencies=True",
                    caused_ex=e
                ) from e
            except AttributeError as e:
                raise ModelSpecValueError(
                    detail=f"{module_path} doesn't have attribute {class_name}",
                    caused_ex=e
                ) from e
        else:
            try:
                flavor_name = flavor[ModelSpecConstants.FLAVOR_NAME_KEY]
                serialization_method = flavor[ModelSpecConstants.SERIALIZATION_METHOD_KEY]
            except KeyError as e:
                raise ModelSpecKeyError(
                    detail=f"{ModelSpecConstants.FLAVOR_NAME_KEY} and {ModelSpecConstants.SERIALIZATION_METHOD_KEY} "
                           f"are required for builtin flavor. Got {flavor}",
                    caused_ex=e
                ) from e
            module_path = f"{__package__}.builtin_models.{flavor_name}.{serialization_method}"
            logger.info(f'module_path = {module_path}')
            try:
                module = importlib.import_module(module_path)
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if not inspect.isabstract(obj) and issubclass(obj, BuiltinModel):
                        return obj
                raise ModelSpecValueError(
                    f"Failed to load specified module {module_path}, "
                    f"please make sure the class definition exists in your dependencies. "
                    f"If you are loading a model in a new environment, "
                    f"please make sure to set install_dependencies=True")
            except ImportError as e:
                raise ModelSpecValueError(
                    detail=f"Failed to load builtin module {module_path}, please make sure you have the right value of "
                           f"{ModelSpecConstants.FLAVOR_NAME_KEY} and {ModelSpecConstants.SERIALIZATION_METHOD_KEY} in "
                           f"flavor: {flavor}",
                    caused_ex=e
                ) from e
