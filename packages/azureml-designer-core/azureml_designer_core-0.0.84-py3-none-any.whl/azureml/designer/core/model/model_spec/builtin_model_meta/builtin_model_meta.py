from typing import List
from pathlib import Path

from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.designer.core.model.model_spec.builtin_model_meta.model_input import ModelInput
from azureml.designer.core.model.model_spec.builtin_model_meta.model_output import ModelOutput
from azureml.designer.core.model.model_spec.builtin_model_meta.task_type import TaskType
from azureml.designer.core.model.model_spec.builtin_model_meta.label_map import LabelMap


class BuiltinModelMeta(object):
    def __init__(self,
                 flavor_extras: dict = None,
                 model_inputs: List[ModelInput] = None,
                 model_outputs: List[ModelOutput] = None,
                 task_type: TaskType = None,
                 label_map: LabelMap = None):
        self._flavor_extras = flavor_extras
        self._model_inputs = model_inputs
        self._model_outputs = model_outputs
        self._task_type = task_type
        self._label_map = label_map

    @classmethod
    def load(cls, artifact_path: Path, meta_dict: dict):
        """Load from artifact_path with info dict provided by model_spec

        :param artifact_path: Path the the folder containing GenericMode
        :param meta_dict: dict
        :return:
        """
        flavor_extras = meta_dict.get(ModelSpecConstants.FLAVOR_EXTRAS_KEY, None)
        model_inputs = None
        model_outputs = None
        task_type = None
        label_map = None

        if ModelSpecConstants.INPUTS_KEY in meta_dict:
            model_inputs = [ModelInput.from_dict(model_input) for model_input in
                            meta_dict[ModelSpecConstants.INPUTS_KEY]]
        if ModelSpecConstants.OUTPUTS_KEY in meta_dict:
            model_outputs = [ModelOutput.from_dict(model_output) for model_output in
                             meta_dict[ModelSpecConstants.OUTPUTS_KEY]]
        if ModelSpecConstants.TASK_TYPE_KEY in meta_dict:
            task_type = TaskType[meta_dict[ModelSpecConstants.TASK_TYPE_KEY]]
        if ModelSpecConstants.LABEL_MAP_FILE_KEY in meta_dict:
            label_map = LabelMap.create(artifact_path / meta_dict[ModelSpecConstants.LABEL_MAP_FILE_KEY])

        return cls(
            flavor_extras=flavor_extras,
            model_inputs=model_inputs,
            model_outputs=model_outputs,
            task_type=task_type,
            label_map=label_map
        )

    def save_and_return_meta_dict(self, artifact_path: Path) -> dict:
        """Save referenced files (e.g. label_map) to somewhere artifact_path and return the dict
        which can be used by ModelSpec

        :param artifact_path:
        :return:
        """
        meta_dict = {}
        if self._flavor_extras:
            meta_dict[ModelSpecConstants.FLAVOR_EXTRAS_KEY] = self._flavor_extras
        if self._task_type:
            meta_dict[ModelSpecConstants.TASK_TYPE_KEY] = self._task_type.name
        if self._label_map:
            self._label_map.save(artifact_path / ModelSpecConstants.LABEL_MAP_FILE_NAME)
            meta_dict[ModelSpecConstants.LABEL_MAP_FILE_KEY] = ModelSpecConstants.LABEL_MAP_FILE_NAME
        if self._model_inputs is not None:
            meta_dict[ModelSpecConstants.INPUTS_KEY] = [model_input.to_dict() for model_input in self._model_inputs]
        if self._model_outputs is not None:
            meta_dict[ModelSpecConstants.OUTPUTS_KEY] = [model_output.to_dict() for model_output in self._model_outputs]
        return meta_dict

    @property
    def flavor_extras(self):
        return self._flavor_extras

    @property
    def model_inputs(self):
        return self._model_inputs

    @property
    def model_outputs(self):
        return self._model_outputs

    @property
    def task_type(self):
        return self._task_type

    @property
    def label_map(self):
        return self._label_map
