from abc import abstractmethod
from pathlib import Path
from typing import Tuple

import torch
import torchvision
from pandas import DataFrame
from PIL import Image

from azureml.designer.core.model.builtin_models.builtin_model import BuiltinModel
from azureml.designer.core.model.constants import ModelSpecConstants, ScoreColumnConstants
from azureml.designer.core.model.extended_column_types import ExtendedColumnTypeName
from azureml.designer.core.model.model_spec.builtin_model_meta.builtin_model_meta import BuiltinModelMeta
from azureml.designer.core.model.model_spec.builtin_model_meta.task_type import TaskType
from azureml.studio.core.logger import get_logger


logger = get_logger(__name__)


def _get_main_version(version_str):
    """Remove the suffix specified by build, which may be not able to install on other platforms

    :param version_str: return value of torch.__version__, e.g. 0.4.0a0+6b959ee
    :return: The main version string 0.4.0
    """
    main_version = ''
    for c in version_str:
        if c.isalpha():
            break
        main_version += c
    return main_version


class PytorchBaseModel(BuiltinModel):

    def __init__(self, raw_model: torch.nn.Module, model_meta: BuiltinModelMeta):
        is_cuda = model_meta.flavor_extras.get(ModelSpecConstants.IS_CUDA_KEY, False)
        self._device = "cuda" if is_cuda and torch.cuda.is_available() else "cpu"
        super().__init__(raw_model, model_meta)

    def _predict(self, df: DataFrame, columns_types: dict = None) -> Tuple[DataFrame, dict]:
        logger.debug(f"df.shape = {df.shape}")
        self.raw_model.to(self._device)
        self.raw_model.eval()
        with torch.no_grad():
            model_inputs = self._pre_process(df, columns_types)
            logger.debug(f"len(model_inputs) = {len(model_inputs)}")
            model_output = self.raw_model(*model_inputs)
            pred_ret = self._post_process(model_output)
            return pred_ret

    def _pre_process(self, df: DataFrame, columns_types: dict = None) -> tuple:
        """
        Convert all elements to tensor, and stack tensors in each column into a 1-dim higher tensor
        e.g. input_tuple_list = [(PIL.Image(3 * 224 * 224), control_tensor0(1 * 5)),
                                 (PIL.Image(3 * 224 * 224), control_tensor1(1 * 5))]
             output would be (images_tensor(2 * 3 * 224 * 224), control_tensor(2 * 1 * 5))
        :param df:
        :param columns_types:
        :return: tuple of stacked tensors, which can be consumed by pytorch models
        """
        columns_types = columns_types or {}
        input_tensors_list = []
        for column_name in df.columns:
            column_type = columns_types.get(column_name, None)
            input_tensors_list.append([self._to_tensor(e, column_type) for e in df[column_name]])

        output_tensors_cnt = len(input_tensors_list)
        output_tensors = [None] * output_tensors_cnt
        for j in range(output_tensors_cnt):
            output_tensors[j] = torch.cat([item.unsqueeze(0) for item in input_tensors_list[j]])
        return tuple(output_tensors)

    def _post_process(self, model_output: torch.Tensor) -> Tuple[DataFrame, dict]:
        """
        Transform raw_model output to task-specified output format
        :param model_output:
        :return:
        """
        if self._model_meta.task_type == TaskType.MultiClassification:
            softmax = torch.nn.Softmax(dim=1)
            pred_probs_list = softmax(model_output).cpu().numpy().tolist()
            pred_index_list = torch.argmax(model_output, 1).cpu().numpy().tolist()
            result_df = DataFrame(
                {
                    ScoreColumnConstants.ScoredLabelIdsColumnName: pred_index_list,
                    ScoreColumnConstants.ScoredProbabilitiesMulticlassColumnName: pred_probs_list
                })
            result_columns_types = {
                ScoreColumnConstants.ScoredLabelIdsColumnName: ExtendedColumnTypeName.NUMERIC,
                ScoreColumnConstants.ScoredProbabilitiesMulticlassColumnName: ExtendedColumnTypeName.OBJECT
            }
            logger.debug(f"result_df = {result_df}")
            return result_df, result_columns_types
        else:
            result_df = DataFrame({ScoreColumnConstants.TensorScoredLabelColumnName: model_output.tolist()})
            result_columns_types = {
                ScoreColumnConstants.TensorScoredLabelColumnName: ExtendedColumnTypeName.PYTORCH_TENSOR
            }
            return result_df, result_columns_types

    def _to_tensor(self, element, element_type):
        if element_type == ExtendedColumnTypeName.IMAGE:
            if not isinstance(element, Image.Image):
                raise TypeError(f"Expecting PIL.Image.Image in Image column, got {type(element)}")
            transform = torchvision.transforms.ToTensor()
            return transform(element).to(self._device)
        return torch.Tensor(element).to(self._device)

    @abstractmethod
    def save(self, save_to: Path, overwrite_if_exists=True):
        pass

    @classmethod
    @abstractmethod
    def load_with_model_meta(cls, load_from: Path, model_meta: BuiltinModelMeta):
        pass
