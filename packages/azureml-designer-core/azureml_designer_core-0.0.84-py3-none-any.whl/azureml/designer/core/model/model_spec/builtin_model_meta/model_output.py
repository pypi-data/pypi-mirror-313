from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


class ModelOutput(object):

    def __init__(
        self,
        name: str,
        value_type: str = None,
        description: str = None
    ):
        self.name = name
        self.value_type = value_type
        self.description = description

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v}

    @classmethod
    def from_dict(cls, value_dict):
        return cls(
            name=value_dict.get("name", None),
            value_type=value_dict.get("value_type", None),
            description=value_dict.get("description", None)
        )
