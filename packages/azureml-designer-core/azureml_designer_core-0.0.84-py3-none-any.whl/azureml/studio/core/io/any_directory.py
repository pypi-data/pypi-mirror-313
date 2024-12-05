"""This module provide classes and functions for reading/writing AnyDirectory."""
import copy
import importlib
from pathlib import Path
from contextlib import contextmanager
from azureml.studio.core.error import DirectoryNotExistError, DirectoryEmptyError, InvalidDirectoryError
from azureml.studio.core.io.data_frame_visualizer import ElementEncoder
from azureml.studio.core.io.visualizer import Visualizer
from azureml.studio.core.utils.yamlutils import dump_to_yaml_file, load_yaml_file
from azureml.studio.core.utils.jsonutils import dump_to_json_file
from azureml.studio.core.error import UserError

_META_FILE_PATH = '_meta.yaml'

_KNOWN_DIRECTORY_CLASSES = [
    'azureml.studio.core.io.data_frame_directory.DataFrameDirectory',
    'azureml.studio.core.io.model_directory.ModelDirectory',
    'azureml.studio.core.io.image_directory.ImageDirectory',
    'azureml.studio.core.io.transformation_directory.TransformationDirectory',
]


class DirectoryIOError(Exception):
    MSG_TPL = "Error occurs when saving/loading the directory '{dir_name}', root cause: '{original_error}'."

    def __init__(self, dir_name, original_error):
        super().__init__(self.MSG_TPL.format(dir_name=dir_name, original_error=original_error))


class DirectorySaveError(DirectoryIOError):
    MSG_TPL = "Error occurs when saving the directory '{dir_name}', root cause: '{original_error}'."


class DirectoryLoadError(DirectoryIOError):
    MSG_TPL = "Error occurs when loading the directory '{dir_name}', root cause: '{original_error}'."


class Meta:
    VIS_KEY = 'visualization'
    EXT_KEY = 'extension'
    RESERVED_FIELDS = {'_dict', '_visualizers'}

    def __init__(self, meta_dict, visualizers=None):
        if not isinstance(meta_dict, dict):
            raise ValueError(f"meta_dict must be a dict, got '{type(meta_dict).__name__}'.")
        self._dict = meta_dict
        if visualizers is None:
            visualizers = []
        self._visualizers = visualizers

    def __eq__(self, other):
        if not isinstance(other, Meta):
            return False
        return self._dict == other.to_dict()

    def to_dict(self):
        return copy.deepcopy(self._dict)

    @property
    def type(self):
        return self._dict['type']

    @property
    def extension(self):
        if self.EXT_KEY not in self._dict:
            self._dict[self.EXT_KEY] = {}
        return self._dict[self.EXT_KEY]

    def update_extension(self, key, val, override=False):
        if not override and key in self.extension:
            raise KeyError(f"Cannot update existing key '{key}' in extension.")
        self.extension[key] = val

    @property
    def visualizers(self):
        return self._visualizers

    @visualizers.setter
    def visualizers(self, visualizers):
        if visualizers is None:
            visualizers = []
        if isinstance(visualizers, Visualizer):
            visualizers = [visualizers]
        self._visualizers = []
        for visualizer in visualizers:
            if not isinstance(visualizer, Visualizer):
                raise TypeError(f"Expected type: Visualizer, got {type(visualizer).__name__}")
            self._visualizers.append(visualizer)

        self._dict[self.VIS_KEY] = [{
            'type': visualizer.type,
            'path': visualizer.path,
        } for visualizer in visualizers]

        if not visualizers:
            self._dict.pop(self.VIS_KEY)

    def update_field(self, key, val, override=False):
        if not override and key in self._dict:
            raise KeyError(f"Cannot update existing key '{key}' in meta.")
        self._dict[key] = val

    def add_field(self, key, val):
        if key not in self._dict:
            self._dict[key] = val

    def __getattr__(self, item):
        # Access other fields from meta
        if item not in self.RESERVED_FIELDS and item in self._dict:
            return self._dict[item]
        return super().__getattribute__(item)

    def get(self, *args, **kwargs):
        return self._dict.get(*args, **kwargs)

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self.update_field(key, value)

    def dump(self, save_to, meta_file_path=_META_FILE_PATH):
        save_to = Path(save_to)
        dump_to_yaml_file(self._dict, save_to / meta_file_path)
        for visualizer in self.visualizers:
            visualizer.dump(save_to)

    @classmethod
    def load(cls, load_from_dir, meta_file_path=None):
        if not meta_file_path:
            meta_file_path = _META_FILE_PATH
        load_from_dir = Path(load_from_dir)

        if not load_from_dir.is_dir():
            raise DirectoryNotExistError(load_from_dir)

        if not list(load_from_dir.iterdir()):
            raise DirectoryEmptyError(load_from_dir)

        full_meta_path = load_from_dir / meta_file_path
        if not full_meta_path.is_file():
            raise InvalidDirectoryError(f"Meta file is not found in path '{load_from_dir}'.")

        meta = load_yaml_file(full_meta_path)
        dir_type_in_meta = meta.get('type')
        if not dir_type_in_meta:
            raise InvalidDirectoryError(f"Required field 'type' is not found in meta file in '{load_from_dir}'.")
        return cls(meta)

    @classmethod
    def exists(cls, path, meta_file_path=None):
        if not meta_file_path:
            meta_file_path = _META_FILE_PATH
        f = Path(path) / meta_file_path
        return f.exists() and f.is_file()


class AnyDirectory:
    """An AnyDirectory may store anything in the directory."""
    TYPE_NAME = 'AnyDirectory'
    _SCHEMA_FILE_PATH = '_schema.json'
    _SAMPLES_FILE_PATH = '_samples.json'

    def __init__(self, meta: Meta = None):
        """Initialize the directory."""
        if meta is None:
            meta = self.create_meta()
        self._meta = meta
        self._basedir = None

    @property
    def meta(self):
        return self._meta

    @property
    def basedir(self):
        return self._basedir

    @basedir.setter
    def basedir(self, val):
        self._basedir = val

    @property
    def type(self):
        return self._meta.type

    @property
    def schema(self):
        return None

    @classmethod
    def create_meta(cls, visualizers: list = None, extensions: dict = None):
        meta = Meta({'type': cls.TYPE_NAME})
        meta.visualizers = visualizers
        if extensions is None:
            extensions = {}
        meta.extension.update(extensions)
        return meta

    @classmethod
    def create(cls, visualizers: list = None, extensions: list = None):
        """Create an AnyDirectory instance with visualizers and extensions."""
        return AnyDirectory(cls.create_meta(visualizers, extensions))

    def dump(self, save_to, meta_file_path=None):
        """Dump the visualization data in the directory 'save_to' and store the yaml file for meta.

        :param save_to: The path of the directory to dump data.
        :param meta_file_path: The relative path of the meta file, use the default path if it is None.
        """
        if not meta_file_path:
            meta_file_path = _META_FILE_PATH
        self.dump_samples(save_to)
        self.dump_schema(save_to)
        self.meta.dump(save_to, meta_file_path)

    def dump_schema(self, save_to):
        save_to = Path(save_to)
        if self.schema:
            self.meta.update_field('schema', self._SCHEMA_FILE_PATH, override=True)
            dump_to_json_file(self.schema, save_to / self._SCHEMA_FILE_PATH)

    def dump_samples(self, save_to):
        try:
            samples = self.get_samples()
        # If get_samples() is not implemented, no samples will be dumped.
        except NotImplementedError:
            return
        save_to = Path(save_to)
        self.meta.update_field('samples', self._SAMPLES_FILE_PATH, override=True)
        dump_to_json_file(samples, save_to / self._SAMPLES_FILE_PATH)

    def get_extension(self, key, default_value=None):
        return self.meta.extension.get(key, default_value)

    def update_extension(self, key, val, override=False):
        self.meta.update_extension(key, val, override)

    def __repr__(self):
        # If meta is not initialized, do not use meta as the representation.
        # This case may happen when the code failed in __init__ before _meta is set,
        # while the object need to be printed in logs.
        if not hasattr(self, '_meta'):
            return super().__repr__()
        return f"{self.TYPE_NAME}(meta={self._meta.to_dict()})"

    @classmethod
    def load(cls, load_from_dir, meta_file_path=None):
        """Load the directory as an AnyDirectory instance.

        :param load_from_dir: The path of the directory to load.
        :param meta_file_path: The relative path of the meta file, use the default path if it is None.
        :return: An instance of AnyDirectory
        """
        directory = cls(meta=Meta.load(load_from_dir, meta_file_path))
        if cls != AnyDirectory:
            # If the class is not AnyDirectory, make sure the type in meta is the same.
            directory.assert_type()
        directory.basedir = load_from_dir
        # Todo: load visualizations and other data described in yaml to make sure a loaded directory can be dumped.
        return directory

    @classmethod
    def load_dynamic(cls, load_from_dir, meta_file_path=None):
        """Dynamically load the directory with the type in meta.
        For example, a directory could be DataFrameDirectory,
        the codes will get the python method 'DataFrameDirectory.load',
        then call `DataFrameDirectory.load(load_from_dir, meta_file_path)`.
        """
        meta = Meta.load(load_from_dir, meta_file_path)
        loader = cls
        # Here we try importing the inherited classes because of the following reasons:
        # 1. We should make sure we use XXDirectory.TYPE_NAME to compare;
        # 2. Some class may import fail due to dependency issues, so we need to try load possible classes.
        for class_path in _KNOWN_DIRECTORY_CLASSES:
            try:
                loader_candidate = cls.get_class_by_path(class_path)
                if loader_candidate.TYPE_NAME == meta.type:
                    loader = loader_candidate
                    break
            except ImportError:
                pass
        return loader.load(load_from_dir, meta_file_path)

    @classmethod
    def get_class_by_path(cls, class_path):
        items = class_path.split('.')
        module_path, class_name = '.'.join(items[:-1]), items[-1]
        module = importlib.import_module(module_path)
        loaded_class = getattr(module, class_name, None)
        if not loaded_class:
            raise ImportError()
        return loaded_class

    def assert_type(self):
        """Make sure the directory type is the same as the type in meta."""
        if self.TYPE_NAME != self.type:
            raise TypeError(f"Type not match, instance type='{self.TYPE_NAME}', type in meta='{self.type}'")

    @classmethod
    def create_from_data(cls, data, schema):
        """Create a directory from data and described schema.

        :param data: example: {'attr1': [b'abc', b'def'], 'attr2': [123, 456]}
        :param schema: example:
        {ColumnAttributes: [{'name': 'attr1', 'type': 'bytes'} {'name': 'attr2', 'type': 'int'}]}
        :return: A directory instance.
        """
        raise NotImplementedError()

    def __len__(self):
        """Return the item count of the directory."""
        raise NotImplementedError()

    def get_item(self, idx):
        """Get an item at idx.

        :param idx: An index.
        :return: An dict, example: {'attr1': xx, 'attr2': xx}
        """
        raise NotImplementedError()

    def iter_items(self):
        """Return all items in the directory."""
        for i in range(len(self)):
            yield self.get_item(i)

    def get_samples(self, count=3):
        """Return some samples of the directory with json format."""
        if count > len(self):
            count = len(self)
        return [{k: ElementEncoder.encode(v) for k, v in self.get_item(i).items()} for i in range(count)]

    def to_data(self):
        """Return data of all items in the directory."""
        return [self.get_item(i) for i in range(len(self))]

    def to_serializable(self):
        """Return json-serializable object encoded from all items in the directory."""

        # TODO: may need to improve perf.
        # Currently for data frame with 1000 rows and columns, this method takes about 2 seconds.
        return ElementEncoder.encode(self.to_data(), raise_error_for_unknown_object=True)


def has_meta(load_from_dir, meta_file_path=None):
    return Meta.exists(load_from_dir, meta_file_path)


@contextmanager
def os_io_error_handler():
    try:
        yield
    except OSError as ex:
        if ex.errno == 5 and 'input/output error' in str(ex.args).lower():
            raise UserError(f"Failed to write output files to disk. Reason: {str(OSError)}. "
                            f"Possibly caused by not enough space left on disk. "
                            "Please upgrade VM Sku or use another compute with more disk space.")
        else:
            raise ex
