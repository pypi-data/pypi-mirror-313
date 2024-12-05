import importlib
from abc import abstractmethod
from typing import List

from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.designer.core.model.extended_column_types import ExtendedColumnTypeName
from azureml.studio.core.error import ModelSpecKeyError


class PreProcessorFactory(object):
    @classmethod
    def get_pre_processor(cls, dct: dict):
        if ModelSpecConstants.PRE_PROCESSOR_MODULE_KEY not in dct or \
                ModelSpecConstants.PRE_PROCESSOR_CLASS_KEY not in dct:
            raise ModelSpecKeyError(detail=f"'{ModelSpecConstants.PRE_PROCESSOR_MODULE_KEY}' or "
                                           f"{ModelSpecConstants.PRE_PROCESSOR_CLASS_KEY}' "
                                           f"missing in pre_process_dict: {dct}")
        pre_process_module = importlib.import_module(dct[ModelSpecConstants.PRE_PROCESSOR_MODULE_KEY])
        pre_process_class = getattr(pre_process_module, dct[ModelSpecConstants.PRE_PROCESSOR_CLASS_KEY])
        parameters = dct.get(ModelSpecConstants.PRE_PROCESSOR_INIT_PARAMS_KEY, {})
        return pre_process_class(**parameters)


class PreProcessor(object):
    @abstractmethod
    def transform(self, element):
        pass

    @property
    @abstractmethod
    def original_column_type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def transformed_column_type(self):
        raise NotImplementedError

    def to_dict(self):
        dct = {
            ModelSpecConstants.PRE_PROCESSOR_MODULE_KEY: self.__class__.__module__,
            ModelSpecConstants.PRE_PROCESSOR_CLASS_KEY: self.__class__.__name__,
        }
        if self.__dict__:
            dct[ModelSpecConstants.PRE_PROCESSOR_INIT_PARAMS_KEY] = self.__dict__.copy()
        return dct


class ImageNormalizer(PreProcessor):
    """Normalize PIL.Image.Image(with 3 channels RGB), and transform to tensor with all values between 0-1"""
    def __init__(self,
                 mean: List = None,
                 std: List = None):
        """
        :param mean: Of format [float, float, float], each denotes the mean of normalization in that channel
        :param std: Same format with mean, each value in list denotes the std of normalization
        """
        # Use most commonly used parameters as default value
        self.mean = mean or [0.5, 0.5, 0.5]
        self.std = std or [0.5, 0.5, 0.5]

    @property
    def original_column_type(self):
        return ExtendedColumnTypeName.IMAGE

    @property
    def transformed_column_type(self):
        return ExtendedColumnTypeName.PYTORCH_TENSOR

    def transform(self, element):
        import torchvision
        transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize(mean=self.mean, std=self.std)
            ]
        )
        return transform(element)
