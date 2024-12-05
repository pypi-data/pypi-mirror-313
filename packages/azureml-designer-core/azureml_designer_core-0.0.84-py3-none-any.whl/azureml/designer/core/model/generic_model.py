import os
from pathlib import Path

from abc import abstractmethod

from azureml.designer.core.model.builtin_models.builtin_model import BuiltinModel
from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.designer.core.model.core_model import CoreModel
from azureml.designer.core.model.model_factory import ModelClassFactory
from azureml.designer.core.model.model_spec.local_dependency import LocalDependencyManager
from azureml.designer.core.model.model_spec.model_spec import ModelSpec
from azureml.designer.core.model.model_spec.serving_config import ServingConfig
from azureml.designer.core.model.model_spec.remote_dependency import RemoteDependencyManager
from azureml.studio.core.error import PathExistsError
from azureml.studio.core.logger import get_logger, TimeProfile
from azureml.studio.core.utils.fileutils import ensure_folder
from azureml.studio.core.utils.yamlutils import dump_to_yaml_file, load_yaml_file

logger = get_logger(__name__)


class GenericModel(object):
    """Generic Model does the flavor-independent things, in general, save/load/predict:
    1. Save/Load model with model_spec.yaml
    2. Handle dependencies.
    """

    def __init__(self,
                 core_model: CoreModel,
                 conda: dict = None,
                 local_dependencies: list = None,
                 serving_config: ServingConfig = None
                 ):
        self._core_model = core_model
        self._conda = conda
        self._local_dependencies = [Path(dependency) for dependency in (local_dependencies or [])]
        self._serving_config = serving_config
        if isinstance(core_model, BuiltinModel):
            self._flavor = core_model.flavor
        else:
            self._flavor = {
                ModelSpecConstants.FLAVOR_NAME_KEY: ModelSpecConstants.CUSTOM_MODEL_FLAVOR_NAME,
                ModelSpecConstants.MODEL_MODULE_KEY: core_model.__class__.__module__,
                ModelSpecConstants.MODEL_CLASS_KEY: core_model.__class__.__name__
            }

    @property
    def flavor(self):
        return self._flavor

    @property
    def core_model(self):
        return self._core_model

    @property
    def conda(self):
        return self._conda

    @property
    def local_dependencies(self):
        return self._local_dependencies

    @property
    def raw_model(self):
        if isinstance(self._core_model, BuiltinModel):
            return self._core_model.raw_model
        return None

    def save(
        self,
        artifact_path: str = ModelSpecConstants.DEFAULT_ARTIFACT_SAVE_PATH,
        model_relative_path: str = ModelSpecConstants.CUSTOM_MODEL_DIRECTORY,
        overwrite_if_exists: bool = True
    ):
        if os.path.exists(artifact_path) and not overwrite_if_exists:
            raise PathExistsError(artifact_path)
        ensure_folder(artifact_path)
        artifact_path = Path(artifact_path)
        model_path = artifact_path / model_relative_path
        self._core_model.save(model_path, overwrite_if_exists=overwrite_if_exists)

        conda_file_path = None
        if self._conda:
            conda_file_path = ModelSpecConstants.CONDA_FILE_NAME
            dump_to_yaml_file(self._conda, artifact_path / conda_file_path)
        else:
            # TODO: Provide the option to save result of "conda env export"
            pass

        copied_local_dependencies = None
        if self._local_dependencies:
            local_dependency_manager = LocalDependencyManager(self._local_dependencies)
            local_dependency_manager.save(artifact_path)
            copied_local_dependencies = local_dependency_manager.copied_local_dependencies

        builtin_model_meta = None
        if isinstance(self._core_model, BuiltinModel):
            builtin_model_meta = self._core_model.model_meta

        model_spec = ModelSpec(
            flavor=self.flavor,
            model_path=model_relative_path,
            conda_file_path=conda_file_path,
            local_dependencies=copied_local_dependencies,
            serving_config=self._serving_config,
            builtin_model_meta=builtin_model_meta
        )
        model_spec_file_path = artifact_path / ModelSpecConstants.MODEL_SPEC_FILE_NAME
        model_spec.save(model_spec_file_path)

    @classmethod
    def load(cls, artifact_path, install_dependencies=False):
        artifact_path = Path(artifact_path)
        model_spec_path = artifact_path / ModelSpecConstants.MODEL_SPEC_FILE_NAME
        logger.debug(f"MODEL_FOLDER: {os.listdir(artifact_path)}")
        model_spec = ModelSpec.load(model_spec_path)
        logger.info(f"Successfully loaded {model_spec_path}")
        conda = None
        if model_spec.conda_file_path:
            conda_yaml_path = artifact_path / model_spec.conda_file_path
            conda = load_yaml_file(conda_yaml_path)
            logger.info(f"Successfully loaded {conda_yaml_path}")

        if install_dependencies:
            if conda:
                with TimeProfile("Installing remote dependencies"):
                    remote_dependency_manager = RemoteDependencyManager()
                    remote_dependency_manager.load(conda)
                    remote_dependency_manager.install()

            if model_spec.local_dependencies:
                with TimeProfile("Installing local dependencies"):
                    local_dependency_manager = LocalDependencyManager()
                    local_dependency_manager.load(artifact_path, model_spec.local_dependencies)
                    local_dependency_manager.install()

        serving_config = None
        if model_spec.serving_config:
            serving_config = ServingConfig.from_dict(model_spec.serving_config)

        core_model_class = ModelClassFactory.get_model_class(model_spec.flavor)
        logger.info(f"core_model_class = {core_model_class}")
        core_model_path = artifact_path / model_spec.model_path
        logger.info(f"Trying to load core_model from {core_model_path}.")
        if issubclass(core_model_class, BuiltinModel):
            core_model = core_model_class.load_with_model_meta(core_model_path, model_spec.builtin_model_meta)
        else:
            core_model = core_model_class.load(core_model_path)

        return cls(
            core_model=core_model,
            conda=conda,
            local_dependencies=model_spec.local_dependencies,
            serving_config=serving_config
        )

    @abstractmethod
    def predict(self, *args, **kwargs):
        """Pass args to core_model, form result DataFrame with scored label

        :param args:
        :param kwargs:
        :return:
        """
        logger.debug(f"args = {args}, kwargs = {kwargs}")
        logger.debug(f"core_model = {self.core_model}")
        return self.core_model.predict(*args, **kwargs)
