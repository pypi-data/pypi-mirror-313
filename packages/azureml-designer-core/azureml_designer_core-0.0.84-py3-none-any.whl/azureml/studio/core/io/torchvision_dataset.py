from PIL import Image
from azureml.studio.core.logger import logger
from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.studio.core.io.image_schema import ImageAnnotationTypeName


class TorchvisionDataset:
    DEFAULT_CLASS_NAME = 'Others'

    def __init__(self, directory: ImageDirectory,
                 transform=None, target_transform=None, transforms=None,
                 annotation_type=None,
                 ):
        try:
            from torchvision.transforms import ToTensor
        except ImportError:
            raise ImportError("Package torchvision is required, "
                              "please install from https://pytorch.org/get-started/locally/")

        self._directory = directory
        self._image_key = directory.get_image_column()
        self._ann_key = directory.get_annotation_column(annotation_type)
        # Only images with annotations can be used in a torchvision dataset
        self._valid_idx = directory.get_valid_annotation_indexes(self._ann_key)
        logger.info(f"TorchvisionDataset is generated, valid index count = {len(self._valid_idx)}.")

        self._categories = directory.schema_instance.get_categories(self._ann_key)
        if self._categories:
            # In COCO dataset, some category may be lost, so we cannot simply use len(self._categories)
            self._num_of_classes = max(category['id'] for category in self._categories) + 1
            self._classes = [self.DEFAULT_CLASS_NAME] * self._num_of_classes
            for category in self._categories:
                self._classes[category['id']] = category['name']
            self._class_to_idx = {self._classes[i]: i for i in range(self._num_of_classes)}
            logger.info(f"Classes are generated, num_of_classes={self._num_of_classes}.")
        else:
            # In some tasks, categories does not exist, such values are ignored.
            self._num_of_classes = 0
            self._classes = []
            self._class_to_idx = {}

        to_tensor = ToTensor()

        def getter(idx):
            item = self._directory.get_item_with_images(self._valid_idx[idx])
            image, ann = item[self._image_key], item[self._ann_key]
            if self._directory.get_annotation_type() == ImageAnnotationTypeName.CLASSIFICATION:
                # This is a hard code for classification scenario that
                # the annotation item is string but the target should be an int value.
                ann = self._class_to_idx[ann]

            if transforms:
                if transform or target_transform:
                    raise ValueError(f"If transforms is not None, transform and target_transform must be None.")
                return transforms(image, ann)

            image = transform(image) if transform else to_tensor(image)
            ann = target_transform(ann) if target_transform else to_tensor(ann) if isinstance(ann, Image.Image) else ann
            return image, ann
        self.image_getter = getter

    def __len__(self):
        return len(self._valid_idx)

    def __getitem__(self, item):
        try:
            return self.image_getter(item)
        except BaseException as e:
            logger.warning(f'Failed to get item {item} due to {e}. Return None.')
            return None

    @property
    def categories(self):
        return self._categories

    @property
    def classes(self):
        return self._classes

    @property
    def class_to_idx(self):
        return self._class_to_idx

    @property
    def num_of_classes(self):
        return self._num_of_classes
