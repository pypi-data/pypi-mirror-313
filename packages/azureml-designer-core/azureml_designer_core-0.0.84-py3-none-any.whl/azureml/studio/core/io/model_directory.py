"""This module provide classes and functions for reading/writing ModelDirectory."""
import os
import pickle
import traceback
from pathlib import Path

from azureml.studio.core.io.any_directory import AnyDirectory, Meta, os_io_error_handler
from azureml.studio.core.utils.yamlutils import load_yaml_file, dump_to_yaml_file
from azureml.studio.core.utils.fileutils import ensure_folder
from azureml.studio.core.logger import logger
from azureml.studio.core.error import InvalidDirectoryError, UserError
from azureml.designer.core.model.core_model import CoreModel
from azureml.designer.core.model.io import save_generic_model, load_generic_model, get_pytorch_state_dict_model
from azureml.designer.core.model.model_spec.builtin_model_meta.label_map import LabelMap
from azureml.designer.core.model.model_spec.builtin_model_meta.task_type import TaskType
from azureml.exceptions import AzureMLException, ServiceException


MODEL_SPEC_FILE = 'model_spec.yaml'

# Constants related to model deployment.
RUN_OUTPUT_FOLDER_NAME = 'trained_model_outputs'
REGISTER_MODEL_META_FIELD = 'registerModel'
MODEL_OUTPUT_PATH_META_FIELD = 'modelOutputPath'


def upload_folder_to_output(name, folder_path):
    try:
        # Lazy import Run to eliminate unnecessary dependencies, or service deployment will fail
        from azureml.core.run import Run
        run = Run.get_context()
        run.upload_folder(name=name, path=folder_path)
        run.flush()
    except (AzureMLException, ServiceException) as e:
        logger.warning(
            f"Failed to upload model directory. Reason: {e.message}")


class ModelDirectory(AnyDirectory):
    """A ModelDirectory could store a machine learning model described by model spec."""
    TYPE_NAME = 'ModelDirectory'

    def __init__(self, model_loader=None, model_dumper=None, model=None, meta=None,
                 conda=None, local_dependencies=None,
                 ):
        super().__init__(meta)
        self.model_loader = model_loader
        self.model_dumper = model_dumper
        self.model = model
        self.conda = conda
        self.local_dependencies = local_dependencies
        # This field will only used when loading from a directory with generic model SDK.
        # TODO: Review the relationship of CoreModel, GenericModel, ModelDirectory and have a more clean design.
        self.generic_model = None

    @property
    def data(self):
        return self.model

    @classmethod
    def create(cls, model_dumper=None,
               model=None, conda=None, local_dependencies=None,
               visualizers=None, extensions=None,
               ):
        """A ModelDirectory is initialized by a model_dumper and other meta data.

        :param model_dumper: A function to write model by calling model_dumper(save_to),
                             it should return a spec dict to describe the specifications of the model.
        :param model: The model object.
        :param conda: See azureml.designer.core.model.generic_model.GenericModel
        :param local_dependencies: See azureml.designer.core.model.generic_model.GenericModel
        :param visualizers: See AnyDirectory
        :param extensions: See AnyDirectory
        """
        meta = cls.create_meta(visualizers, extensions)
        return cls(model_dumper=model_dumper, model=model, meta=meta,
                   conda=conda, local_dependencies=local_dependencies,
                   )

    @classmethod
    def create_meta(cls, visualizers: list = None, extensions: dict = None):
        meta = super().create_meta(visualizers, extensions)
        meta.update_field('model', MODEL_SPEC_FILE)
        return meta

    def dump_with_model_dumper(self, save_to, model_dumper: callable):
        # In default, we assume model_dumper will dump the model data and return a dict to store the model information,
        # then we use a yaml file to store such dict,.
        spec = model_dumper(save_to) or {}
        dump_to_yaml_file(spec, os.path.join(save_to, self.model_spec_file))

    def dump_with_generic_model(self, save_to):
        save_generic_model(
            self.model, save_to,
            conda=self.conda, local_dependencies=self.local_dependencies,
            overwrite_if_exists=True,
        )

    def _add_deployment_info_to_meta(self):
        self.meta.add_field(REGISTER_MODEL_META_FIELD, True)
        self.meta.add_field(MODEL_OUTPUT_PATH_META_FIELD, RUN_OUTPUT_FOLDER_NAME)

    def dump(self, save_to, meta_file_path=None, model_deployment_handler=None):
        """Dump the model to the directory 'save_to' and dump other meta data. Params are the same as AnyDirectory.

        :param save_to: destination directory path.
        :param meta_file_path: file path of the meta file.
        :param model_deployment_handler: If not None, also dump deployment-related files (such as score.py
                                         and conda-env.yaml files.) and upload the dumped directory to run output.
        """
        with os_io_error_handler():
            # If model_dumper of the model is provided, we directly dump the model with model_dumper.
            if callable(self.model_dumper):
                self.dump_with_model_dumper(save_to, model_dumper=self.model_dumper)
            # Otherwise, if it is a CoreModel, we use generic_model SDK to dump the model.
            elif isinstance(self.model, CoreModel):
                self.dump_with_generic_model(save_to)
            # If both are not OK, we use pickle to dump self.model.
            else:
                self.dump_with_model_dumper(save_to, model_dumper=pickle_dumper(self.model))

            # Add deployment-related fields into meta.
            # deploy_handler is an attribute of base learner.
            if not model_deployment_handler and hasattr(self.model, 'deployment_handler'):
                model_deployment_handler = self.model.deployment_handler

            if model_deployment_handler:
                self._add_deployment_info_to_meta()
                model_deployment_handler.dump_deployment_files(save_to)

            super().dump(save_to)

        if model_deployment_handler:
            upload_folder_to_output(RUN_OUTPUT_FOLDER_NAME, save_to)

    @property
    def model_spec_file(self):
        return self._meta.get('model', MODEL_SPEC_FILE)

    @classmethod
    def load_model_spec(cls, load_from_dir: str, model_spec_relative_path=None, meta_file_path=None):
        try:
            if model_spec_relative_path is None:
                meta = Meta.load(load_from_dir, meta_file_path)
                spec = cls.load_model_spec(load_from_dir, meta.model)
            else:
                spec = load_yaml_file(os.path.join(load_from_dir, model_spec_relative_path))
        except FileNotFoundError as ex:
            logger.warning(ex)
            spec = None
        return spec

    @classmethod
    def load_with_model_loader(cls, load_from_dir, model_loader, meta_file_path=None):
        """Load model with a provided model_loader."""
        directory = super().load(load_from_dir, meta_file_path)
        spec = cls.load_model_spec(load_from_dir, directory.meta.model)
        directory.model = model_loader(load_from_dir, spec)
        directory.model_loader = model_loader
        return directory

    @classmethod
    def load_with_pickle_loader(cls, load_from_dir, meta_file_path=None):
        return cls.load_with_model_loader(load_from_dir, pickle_loader, meta_file_path)

    @classmethod
    def load_with_generic_model(cls, load_from_dir, install_dependencies=True, meta_file_path=None):
        # In default, we assume that if conda/local_dependencies is dumped, we need to install such dependencies.
        # So the default value of install_dependencies is True
        generic_model = load_generic_model(load_from_dir, install_dependencies=install_dependencies)
        directory = super().load(load_from_dir, meta_file_path)
        directory.model = generic_model.core_model
        directory.conda = generic_model.conda
        directory.local_dependencies = generic_model.local_dependencies
        directory.generic_model = generic_model
        return directory

    @classmethod
    def _try_load_with_loader_method(cls, loader_method, load_from_dir, meta_file_path=None):
        try:
            return loader_method(load_from_dir, meta_file_path=meta_file_path)
        except BaseException as e:
            logger.debug(f"_try_load_with_loader_method will return None because "
                         f"try loading model from {load_from_dir} with '{loader_method.__qualname__}' failed, "
                         f"error='{e}'. This does not mean model loading failed. "
                         f"stack_trace:\n{traceback.format_exc()}")

    @classmethod
    def _try_load_with_loader_methods(cls, loader_methods, load_from_dir, meta_file_path=None):
        for loader_method in loader_methods:
            directory = cls._try_load_with_loader_method(loader_method, load_from_dir, meta_file_path=meta_file_path)
            if directory is not None:
                return directory

    @classmethod
    def load(cls, load_from_dir, meta_file_path=None, model_loader=None):
        """Load the directory as a ModelDirectory.

        :param load_from_dir: See AnyDirectory
        :param meta_file_path: See AnyDirectory
        :param model_loader: A function to load the model. Todo: Load the model according to meta data.
        :return: See AnyDirectory
        """
        # If model_loader is provided, we directly load the model with it;
        if model_loader:
            return cls.load_with_model_loader(load_from_dir, model_loader, meta_file_path)
        # We first assume it is a CoreModel and use generic_model SDK to load it,
        # then we assume it is dumped by pickle, use pickle_loader to load it.
        default_loader_methods = [
            cls.load_with_generic_model,
            cls.load_with_pickle_loader,
        ]
        directory = cls._try_load_with_loader_methods(default_loader_methods, load_from_dir, meta_file_path)
        if directory is not None:
            return directory
        # If all loaders failed, we return a model without model data,
        # the user could use directory.basedir to get the path and load his model data.
        logger.warning(f"All default loaders load model data failed, return a ModelDirectory with model=None.")
        return super().load(load_from_dir, meta_file_path)

    @classmethod
    def is_legacy_pickle_model(cls, load_from_dir, meta_file_path=None):
        """ To tell if a model is legacy model dumped by pickle."""
        spec = cls.load_model_spec(load_from_dir=load_from_dir, meta_file_path=meta_file_path)
        return 'file_name' in spec and (Path(load_from_dir)/spec['file_name']).is_file()

    @classmethod
    def load_instance(cls, load_from_dir, model_class, meta_file_path=None):
        # Currently we only have two kinds of models, legacy model(stored as pickle) and CoreModel
        is_legacy_model_class = not issubclass(model_class, CoreModel)
        err_msg = f"The model data is not compatible with expected model class: {model_class}."
        # First make sure whether the expected class is compatible with the directory
        if cls.is_legacy_pickle_model(load_from_dir, meta_file_path) != is_legacy_model_class:
            raise InvalidDirectoryError(err_msg)
        try:
            # Load model with specific according to the expected model type.
            # When loading with generic_model, set install_dependencies=False to avoid additional installation cost.
            # Since the class is provided, the dependencies must be compatible if the directory is correct.
            directory = cls.load_with_pickle_loader(load_from_dir, meta_file_path) if is_legacy_model_class else \
                cls.load_with_generic_model(load_from_dir, install_dependencies=False, meta_file_path=meta_file_path)
        except (UserError, ImportError, AttributeError) as e:
            # UserError indicate that some expected exception is raised when load generic model.
            # ImportError/AttributeError indicate that the dependencies are not compatible,
            # which means the directory is not expected.
            raise InvalidDirectoryError(err_msg) from e

        if not isinstance(directory.model, model_class):
            raise InvalidDirectoryError(
                f"The model data is not compatible, expect {model_class} got {type(directory.model)}."
            )
        return directory.model

    @classmethod
    def isinstance(cls, load_from_dir, model_class, meta_file_path=None):
        try:
            cls.load_instance(load_from_dir, model_class, meta_file_path)
        except BaseException:
            return False
        return True


def save_model_to_directory(save_to, model_dumper=None,
                            model=None, conda=None, local_dependencies=None,
                            visualizers=None, extensions=None,
                            meta_file_path=None, model_deployment_handler=None
                            ):
    """Save a model to the specified folder 'save_to' with AnyDirectoryDirectory.dump()."""
    ModelDirectory.create(
        model_dumper=model_dumper,
        model=model, conda=conda, local_dependencies=local_dependencies,
        visualizers=visualizers, extensions=extensions,
    ).dump(save_to, meta_file_path, model_deployment_handler)


def save_pytorch_state_dict_model(
        save_to,
        pytorch_model,
        init_params: dict = None,
        conda=None,
        local_dependencies: list = None,
        inputs: list = None,
        outputs: list = None,
        task_type: TaskType = None,
        label_map: LabelMap = None,
        deployment_handler=None,
):
    model = get_pytorch_state_dict_model(
        pytorch_model=pytorch_model,
        init_params=init_params,
        inputs=inputs,
        outputs=outputs,
        task_type=task_type,
        label_map=label_map,
    )
    save_model_to_directory(
        save_to=save_to, model=model,
        conda=conda,
        local_dependencies=local_dependencies,
        model_deployment_handler=deployment_handler,
    )


def load_model_from_directory(load_from_dir, meta_file_path=None, model_loader=None):
    """Load a model in the specified folder 'load_from_dir' with ModelDirectory.load()."""
    return ModelDirectory.load(load_from_dir, meta_file_path, model_loader)


def pickle_loader(load_from_dir, model_spec):
    """Load the pickle model by reading the file indicated by file_name in model_spec."""
    file_name = model_spec['file_name']
    try:
        with open(os.path.join(load_from_dir, file_name), 'rb') as fin:
            return pickle.load(fin)
    except (ImportError, AttributeError) as ex:
        raise InvalidDirectoryError(reason='The pickle data in the directory is not recognized.') from ex


def pickle_dumper(data, file_name=None):
    """Return a dumper to dump a model with pickle."""
    if not file_name:
        file_name = '_data.pkl'

    def model_dumper(save_to):
        full_path = os.path.join(save_to, file_name)
        ensure_folder(os.path.dirname(os.path.abspath(full_path)))
        with open(full_path, 'wb') as fout:
            pickle.dump(data, fout)

        model_spec = {'model_type': 'pickle', 'file_name': file_name}
        return model_spec

    return model_dumper
