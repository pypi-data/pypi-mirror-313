from azureml.studio.core.schema import ColumnTypeName


class ExtendedColumnTypeName(ColumnTypeName):
    IMAGE = 'Image'
    PYTORCH_TENSOR = 'PytorchTensor'
