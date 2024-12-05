from azureml.designer.core.model.model_spec.builtin_model_meta.pre_processor import PreProcessor, PreProcessorFactory
from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


class ModelInput(object):

    def __init__(
        self,
        name: str,
        value_type: str = None,
        default: object = None,
        description: str = None,
        optional: bool = False,
        pre_processor: PreProcessor = None
    ):
        self.name = name
        self.value_type = value_type
        self.default = default
        self.description = description
        self.optional = optional
        self.pre_processor = pre_processor

    def to_dict(self):
        dct = {k: v for k, v in self.__dict__.items() if v}
        if self.pre_processor:
            dct[ModelSpecConstants.MODEL_INPUT_PRE_PROCESSOR_KEY] = self.pre_processor.to_dict()
        return dct

    @classmethod
    def from_dict(cls, dct):
        pre_processor = None
        if ModelSpecConstants.MODEL_INPUT_PRE_PROCESSOR_KEY in dct:
            pre_processor = PreProcessorFactory.get_pre_processor(dct[ModelSpecConstants.MODEL_INPUT_PRE_PROCESSOR_KEY])
        return cls(
            name=dct.get(ModelSpecConstants.MODEL_INPUT_NAME_KEY, None),
            value_type=dct.get(ModelSpecConstants.MODEL_INPUT_VALUE_TYPE_KEY, None),
            default=dct.get(ModelSpecConstants.MODEL_INPUT_DEFAULT_KEY, None),
            description=dct.get(ModelSpecConstants.MODEL_INPUT_DESCRIPTION_KEY, None),
            optional=dct.get(ModelSpecConstants.MODEL_INPUT_OPTIONAL_KEY, False),
            pre_processor=pre_processor
        )
