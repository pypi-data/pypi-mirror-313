import pickle
from pathlib import Path

from azureml.studio.core.logger import logger
from azureml.studio.core.utils.jsonutils import load_json_file, dump_to_json_file
from azureml.studio.core.io.any_directory import AnyDirectory, Meta
from azureml.studio.core.error import InvalidDirectoryError
from azureml.studio.core.io.any_directory import os_io_error_handler


class TransformationDirectory(AnyDirectory):
    TYPE_NAME = 'TransformationDirectory'
    TRANSFORM_TYPE = 'UNKNOWN'

    @classmethod
    def load(cls, load_from_dir, meta_file_path=None):
        directory = super().load(load_from_dir, meta_file_path)
        transform_type = directory.meta.get('transform_type')
        if transform_type is None:
            # This is for backward compatibility that old TransformationDirectory are all pickle based.
            logger.warning(f"Transform type is not specified, fallback to pickle based transformation directory.")
            return PickleTransformationDirectory.load(load_from_dir, meta_file_path)
        elif transform_type == ImageTransformationDirectory.TRANSFORM_TYPE:
            return ImageTransformationDirectory.load(load_from_dir, meta_file_path)
        elif transform_type == PickleTransformationDirectory.TRANSFORM_TYPE:
            return PickleTransformationDirectory.load(load_from_dir, meta_file_path)

    @classmethod
    def create_meta(cls, visualizers: list = None, extensions: dict = None):
        meta = super().create_meta(visualizers, extensions)
        meta.update_field('transform_type', cls.TRANSFORM_TYPE)
        return meta


class PickleTransformationDirectory(TransformationDirectory):
    TRANSFORM_TYPE = 'Pickle'
    PICKLE_FILE = 'transform.pkl'

    def __init__(self, data=None, meta=None):
        super().__init__(meta)
        self.data = data
        self.transform = data

    @property
    def file_path(self):
        return self.meta.file_path

    @classmethod
    def create(cls, transform, file_path=None, visualizers=None, extensions=None):
        meta = cls.create_meta(visualizers, extensions, file_path)
        return cls(data=transform, meta=meta)

    @classmethod
    def create_meta(cls, visualizers: list = None, extensions: dict = None, file_path=None):
        meta = super().create_meta(visualizers, extensions)
        if file_path is None:
            file_path = cls.PICKLE_FILE
        meta.update_field('file_path', file_path)
        return meta

    @classmethod
    def load(cls, load_from_dir, meta_file_path=None):
        meta = Meta.load(load_from_dir, meta_file_path)
        # None is OK because the legacy transformation directory doesn't have transform_type.
        if meta.get('transform_type') not in {cls.TRANSFORM_TYPE, None}:
            raise InvalidDirectoryError(reason="The input directory is not a pickle based TransformationDirectory.")
        try:
            with open(Path(load_from_dir) / meta.file_path, 'rb') as fin:
                transform = pickle.load(fin)
        # Module not found: ImportError
        # The class is not found in the module/the property is not found in the class: AttributeError
        except (ImportError, AttributeError, pickle.UnpicklingError) as e:
            raise InvalidDirectoryError(reason="The pickle data in the directory is not recognized.") from e

        return cls(data=transform, meta=meta)

    def dump(self, save_to, meta_file_path=None):
        with os_io_error_handler():
            super().dump(save_to, meta_file_path)
            with open(Path(save_to) / self.meta.file_path, 'wb') as fout:
                pickle.dump(self.transform, fout)


def save_pickle_transform_to_directory(save_to, transform, file_path=None, meta_file_path=None,
                                       **kwargs,
                                       ):
    PickleTransformationDirectory.create(
        transform=transform, file_path=file_path, **kwargs,
    ).dump(save_to, meta_file_path)


class ImageTransformationDirectory(TransformationDirectory):
    # These default values are from imagenet dataset.
    MEAN = [0.485, 0.456, 0.406]
    STD = [0.229, 0.224, 0.225]
    JSON_FILE = '_transforms.json'
    TRANSFORM_TYPE = 'Image'
    # Currently the operations are chosen from torchvision.
    # Reference: https://pytorch.org/docs/stable/torchvision/transforms.html
    VALID_OPS = {
        "ToTensor", "ToPILImage",
        "Normalize", "Resize", "CenterCrop", "Pad",
        "RandomCrop", "RandomHorizontalFlip", "RandomVerticalFlip", "RandomResizedCrop",
        "FiveCrop", "TenCrop",
        "ColorJitter", "RandomRotation", "RandomAffine",
        "Grayscale", "RandomGrayscale",
        "RandomPerspective", "RandomErasing",
    }

    def __init__(self, transforms, meta=None):
        super().__init__(meta)
        self.validate_transforms(transforms)
        self.transforms = transforms

    @classmethod
    def create(cls, transforms=None, visualizers=None, extensions=None):
        meta = cls.create_meta(visualizers, extensions)
        if transforms is None:
            transforms = []
        return cls(transforms, meta)

    @classmethod
    def load(cls, load_from_dir, meta_file_path=None):
        meta = Meta.load(load_from_dir, meta_file_path)
        if meta.get('transform_type') != cls.TRANSFORM_TYPE:
            raise InvalidDirectoryError(reason="The input directory is not an ImageTransformationDirectory.")
        load_from_dir = Path(load_from_dir)
        data_path = load_from_dir / cls.JSON_FILE
        if not data_path.is_file():
            raise InvalidDirectoryError(f"Transformation data file {data_path} is not found.")
        transforms = load_json_file(load_from_dir / cls.JSON_FILE)
        return cls(transforms=transforms, meta=meta)

    @classmethod
    def validate_op(cls, op, args):
        if op not in cls.VALID_OPS:
            raise ValueError(f"Operation {op} is not valid, valid ops are: {','.join(cls.VALID_OPS)}.")
        # TODO: Validate the operations according to the operation function signatures.
        if not isinstance(args, (dict, list, tuple, int, float)):
            raise ValueError(f"Operation arguments must be a kwargs dict or a list of args or one arg.")

    @classmethod
    def validate_transforms(cls, transforms):
        for op, args in transforms:
            cls.validate_op(op, args)

    def append(self, op, args=None):
        if args is None:
            args = {}
        self.validate_op(op, args)
        self.transforms.append([op, args])
        return self

    def append_normalize(self, mean=None, std=None, inplace=True):
        if mean is None:
            mean = self.MEAN
        if std is None:
            std = self.STD
        self.append('Normalize', [mean, std, inplace])
        return self

    def dump(self, save_to, meta_file_path=None):
        with os_io_error_handler():
            save_to = Path(save_to)
            dump_to_json_file(self.transforms, save_to / self.JSON_FILE)
            super().dump(save_to, meta_file_path)

    @property
    def torch_transform(self):
        return ImageTransformationDirectory.get_torch_transform(self.transforms)

    @staticmethod
    def get_torch_transform(transform_list):
        try:
            from torchvision import transforms
        except ImportError:
            raise ImportError("Package torchvision is required, "
                              "please install from https://pytorch.org/get-started/locally/")
        ops = []
        for op, args in transform_list:
            transform = getattr(transforms, op, None)
            if not transform:
                raise NotImplementedError(f'Unsupported torch operation: {op}')
            logger.info(f"Composing transform {op}, args={args}.")
            if isinstance(args, dict):
                # Keyword Arguments
                ops.append(transform(**args))
            elif isinstance(args, (list, tuple)):
                # List Arguments
                ops.append(transform(*args))
            elif args is None:
                # No Argument
                ops.append(transform())
            else:
                # One Argument
                ops.append(transform(args))
        return transforms.Compose(ops)
