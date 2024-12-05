import os
import uuid

from abc import ABCMeta, abstractmethod

from azureml.studio.core.utils.jsonutils import dump_to_json_file

_VISUALIZATION_PREFIX = '_visualization'


class Visualizer(metaclass=ABCMeta):

    def __init__(self, vtype):
        self._type = vtype

    @abstractmethod
    def dump(self, basedir):
        pass

    @abstractmethod
    def path(self):
        pass

    @property
    def type(self):
        return self._type


class ExistFileVisualizer(Visualizer):

    def __init__(self, vtype, file_path):
        Visualizer.__init__(self, vtype)
        self._file_path = file_path

    @property
    def path(self):
        return self._file_path

    def dump(self, basedir):
        full_path = os.path.join(basedir, self.path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Visualizer not found: {full_path}")


class JsonVisualizer(Visualizer):

    def __init__(self, vtype, json_data, file_path=None):
        Visualizer.__init__(self, vtype)
        self._file_path = file_path
        if file_path is None:
            self._file_path = f'{_VISUALIZATION_PREFIX}_{str(uuid.uuid4())}.json'
        self._json_data = json_data

    @property
    def path(self):
        return self._file_path

    @property
    def json_data(self):
        return self._json_data

    def dump(self, basedir):
        full_path = os.path.join(basedir, self.path)
        if os.path.exists(full_path):
            raise FileExistsError(f"Visualizer data exists: {full_path}")
        try:
            dump_to_json_file(self.json_data, full_path)
        except TypeError:
            raise TypeError(f"Not a valid json object: {full_path}")
