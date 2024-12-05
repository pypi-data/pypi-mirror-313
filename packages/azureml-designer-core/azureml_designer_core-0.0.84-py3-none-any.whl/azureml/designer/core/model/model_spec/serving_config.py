from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


class ServingConfig(object):

    # TODO: Set the object variables to be properties and verify on set method
    def __init__(
        self,
        gpu_support: bool = False,
        cpu_core_num: float = 1.0,
        memory_in_GB: float = 0.5
    ):
        self.gpu_support = gpu_support
        self.cpu_core_num = cpu_core_num
        self.memory_in_GB = memory_in_GB

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, value_dict):
        return cls(
            gpu_support=value_dict.get(ModelSpecConstants.GPU_SUPPORT_KEY, False),
            cpu_core_num=value_dict.get(ModelSpecConstants.CPU_CORE_NUM_KEY, 1.0),
            memory_in_GB=value_dict.get(ModelSpecConstants.MEMORY_IN_GB_KEY, 0.5)
        )
