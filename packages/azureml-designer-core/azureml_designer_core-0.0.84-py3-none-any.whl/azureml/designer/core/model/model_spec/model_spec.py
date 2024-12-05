from datetime import datetime, timezone
from pathlib import Path

from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.designer.core.model.model_spec.builtin_model_meta.builtin_model_meta import BuiltinModelMeta
from azureml.studio.core.error import ModelSpecKeyError
from azureml.studio.core.logger import get_logger
from azureml.studio.core.utils.yamlutils import load_yaml_file, dump_to_yaml_file

logger = get_logger(__name__)
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


class ModelSpec(object):
    """Handle model_spec.yaml
    Generally, if the entry in spec is not referencing other files, load it as corresponding object,
    otherwise, load as dict containing path without loading the referenced file
    """
    def __init__(self,
                 flavor: dict,
                 model_path: str = ModelSpecConstants.CUSTOM_MODEL_DIRECTORY,
                 conda_file_path: str = ModelSpecConstants.CONDA_FILE_NAME,
                 local_dependencies: list = None,
                 time_created: datetime = None,
                 serving_config: dict = None,
                 builtin_model_meta: BuiltinModelMeta = None
                 ):
        self._flavor = flavor
        # Relative path to artifact path
        self._model_path = model_path
        # Relative path to artifact path
        self._conda_file_path = conda_file_path
        # Relative path to zipped local_dependency folder path
        self._local_dependencies = local_dependencies
        self._serving_config = serving_config
        self._time_created = time_created or datetime.now(timezone.utc)
        self._builtin_model_meta = builtin_model_meta

    def save(self, save_to_path: Path):
        spec = {
            ModelSpecConstants.FLAVOR_KEY: self._flavor,
            ModelSpecConstants.MODEL_FILE_KEY: self._model_path,
            ModelSpecConstants.TIME_CREATED_KEY: self._time_created.strftime(TIME_FORMAT)
        }
        if self._local_dependencies:
            spec[ModelSpecConstants.LOCAL_DEPENDENCIES_KEY] = [str(d) for d in self._local_dependencies]
        if self._conda_file_path:
            spec[ModelSpecConstants.CONDA_FILE_KEY] = self._conda_file_path
        if self._serving_config:
            spec[ModelSpecConstants.SERVING_CONFIG_KEY] = self._serving_config
        if self._builtin_model_meta:
            artifact_path = save_to_path.parent
            builtin_model_meta_dict = self._builtin_model_meta.save_and_return_meta_dict(artifact_path)
            spec.update(**builtin_model_meta_dict)
        logger.debug(f"spec = {spec}")
        dump_to_yaml_file(spec, save_to_path)

    @classmethod
    def load(cls, load_from_path: Path):
        spec_dict = load_yaml_file(load_from_path)
        if ModelSpecConstants.FLAVOR_KEY not in spec_dict:
            raise ModelSpecKeyError(load_from_path, f"{ModelSpecConstants.FLAVOR_KEY} is missing.")
        if ModelSpecConstants.MODEL_FILE_KEY not in spec_dict:
            raise ModelSpecKeyError(load_from_path, f"{ModelSpecConstants.MODEL_FILE_KEY} is missing.")

        flavor = spec_dict[ModelSpecConstants.FLAVOR_KEY]
        model_path = spec_dict[ModelSpecConstants.MODEL_FILE_KEY]
        conda_file_path = spec_dict.get(ModelSpecConstants.CONDA_FILE_KEY, None)
        local_dependencies = spec_dict.get(ModelSpecConstants.LOCAL_DEPENDENCIES_KEY, None)
        serving_config = spec_dict.get(ModelSpecConstants.SERVING_CONFIG_KEY, None)
        time_created = None
        if ModelSpecConstants.TIME_CREATED_KEY in spec_dict:
            time_created = datetime.strptime(spec_dict[ModelSpecConstants.TIME_CREATED_KEY], TIME_FORMAT)

        # TODO: Decide whether or not add layer in model spec for model_meta
        irrelevant_keys = {ModelSpecConstants.MODEL_FILE_KEY, ModelSpecConstants.CONDA_FILE_KEY,
                           ModelSpecConstants.LOCAL_DEPENDENCIES_KEY, ModelSpecConstants.TIME_CREATED_KEY}
        builtin_model_meta_dict = {k: v for k, v in spec_dict.items() if k not in irrelevant_keys}
        artifact_path = load_from_path.parent
        builtin_model_meta = BuiltinModelMeta.load(
            artifact_path=artifact_path,
            meta_dict=builtin_model_meta_dict)

        return cls(
            flavor=flavor,
            model_path=model_path,
            conda_file_path=conda_file_path,
            local_dependencies=local_dependencies,
            time_created=time_created,
            serving_config=serving_config,
            builtin_model_meta=builtin_model_meta
        )

    @property
    def flavor(self):
        return self._flavor

    @property
    def model_path(self):
        return self._model_path

    @property
    def conda_file_path(self):
        return self._conda_file_path

    @property
    def local_dependencies(self):
        return self._local_dependencies

    @property
    def serving_config(self):
        return self._serving_config

    @property
    def time_created(self):
        return self._time_created

    @property
    def builtin_model_meta(self):
        return self._builtin_model_meta

    @property
    def task_type(self):
        if self._builtin_model_meta and self._builtin_model_meta.task_type:
            return self._builtin_model_meta.task_type
        else:
            return None
