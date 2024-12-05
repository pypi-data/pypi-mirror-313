import copy
import functools
import shutil
import time
from io import BytesIO
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from PIL import Image, PngImagePlugin, ImageFile

from azureml.studio.core.error import InvalidDirectoryError, UserError
from azureml.studio.core.io.any_directory import AnyDirectory, Meta, has_meta, os_io_error_handler
from azureml.studio.core.io.image_schema import (ImageAnnotationTypeName, ImageInfo, ImageSchema)
from azureml.studio.core.logger import logger
from azureml.studio.core.schema import (ColumnAttribute, ColumnTypeName, ElementTypeName)
from azureml.studio.core.utils.fileutils import ensure_folder, iter_files
from azureml.studio.core.utils.jsonutils import (dump_to_json_lines, load_json_file, load_json_lines)

# Increase max image size we could read from 1M to 100M.
LARGE_ENOUGH_NUMBER = 100
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (ImageFile.SAFEBLOCK)
# Support read truncated images for robustness.
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Allowed image extensions (lowercase), which is copied from torchvision.datasets.folder
IMG_EXTS = {'.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp'}


def is_image_file(file_name):
    if Path(file_name).suffix.lower() not in IMG_EXTS:
        return False
    # fix bug 966507. Use lazy function 'Image.open' to identify the file by reading metadata,
    # the actual image data is not read from the file until you try to process the data.
    # See https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#open
    try:
        with Image.open(file_name):
            return True
    except Exception as e:
        logger.warning(f"Failed to open '{file_name}' due to '{str(e.args[0])}'. Skip it.")
        return False


def image_to_bytes(image, file_format='png'):
    """Convert an image to a bytes array."""
    with BytesIO() as buffered:
        image.save(buffered, format=file_format)
        return buffered.getvalue()


def convert_to_rgb(image):
    return image.convert('RGB')


DEFAULT_CONVERTER = convert_to_rgb


def image_from_file(file, converter=DEFAULT_CONVERTER):
    """Get an image from a file path."""
    try:
        with Image.open(str(file)) as fin:
            return converter(fin)
    # fix bug 975464 Image.open from a file occasionally fails due to OSError or IOError caused by
    # "Transport endpoint is not connected". This error is due to transient network issue. Retry might make it work.
    except (OSError, IOError) as e:
        if "Transport endpoint is not connected" in str(e.args):
            raise InvalidDirectoryError(f"Failed to get an image from '{str(file)}'. Please retry later.") from e
        logger.warning(f"Failed to get image from {file} due to {e}.")
        raise e
    except BaseException as e:
        logger.warning(f"Failed to get image from {file} due to {e}.")
        raise e


def image_from_bytes(data, converter=DEFAULT_CONVERTER):
    """Get an image from a bytes array."""
    with BytesIO(data) as bytes_data:
        return converter(Image.open(bytes_data))


def bytes_from_file(file):
    with open(file, 'rb') as fin:
        return fin.read()


def bytes_from_url(url):
    """Get bytes from URL, retry N times."""
    N = 6
    backoffs = [2 ** i for i in range(N)]
    err = None
    for backoff in backoffs:
        try:
            with urlopen(url) as url_reader:
                return url_reader.read()
        except URLError as e:
            err = e
            logger.warning(f"Connection failed when loading '{url}', waiting {backoff} seconds to retry.")
            time.sleep(backoff)
    logger.error(f"Connection failed, cannot get data from '{url}'.")
    raise err


def image_from_url(url, converter=DEFAULT_CONVERTER):
    """Get an image from URL"""
    return image_from_bytes(bytes_from_url(url), converter)


# Convert bytes/BytesIO/Path-like to a PIL Image
def image_from(data, converter=DEFAULT_CONVERTER):
    if isinstance(data, Image.Image):
        return converter(data)
    elif isinstance(data, bytes):
        return image_from_bytes(data, converter)
    elif isinstance(data, (BytesIO, str, Path)):
        return image_from_file(data, converter)
    raise ValueError(f"Image value type '{type(data).__name__}' is not a valid image type.")


class ImageDirectory(AnyDirectory):
    """An ImageDirectory should store images and related meta data in the directory."""
    TYPE_NAME = 'ImageDirectory'

    META_IMAGE_LIST_KEY = 'image_list'
    IMAGE_LIST_FILE = 'images.lst'

    def __init__(self, image_list, schema, meta=None):
        if not image_list:
            raise ValueError(f"No valid image is provided. Allowed images must be with extensions {IMG_EXTS}"
                             " and identifiable.")
        super().__init__(meta)
        self._image_list = image_list
        self._schema_instance = schema \
            if isinstance(schema, ImageSchema) else ImageSchema.from_dict(schema)
        self._image2ref = self._schema_instance.get_image_to_ref()

    @property
    def image_list(self):
        if not isinstance(self._image_list, list):
            raise NotImplementedError()
        return self._image_list

    @property
    def size(self):
        return len(self._image_list)

    @property
    def schema_instance(self):
        return self._schema_instance

    @property
    def schema(self):
        return self._schema_instance.to_dict()

    @property
    def schema_names(self):
        return self._schema_instance.column_attributes.names

    @property
    def image2ref(self):
        return self._image2ref

    def get_schema_attr(self, name) -> ColumnAttribute:
        return self._schema_instance.column_attributes[name]

    def get_image_column(self):
        return self._schema_instance.get_image_column()

    def get_annotation_column(self, annotation_type=None):
        return self._schema_instance.get_annotation_column(annotation_type)

    def get_annotation_type(self):
        return self._schema_instance.get_annotation_type()

    def iter_images(self):
        for i in range(self.size):
            logger.info(f"Loading image item {i}.")
            result = self.get_item_with_images(i)
            logger.info(f"Image item {i} is loaded: {result}")
            yield result

    def to_torchvision_classification_dataset(self, transform=None, target_transform=None, transforms=None):
        return self.to_torchvision_dataset(
            transform=transform,
            target_transform=target_transform,
            transforms=transforms,
            annotation_type=ImageAnnotationTypeName.CLASSIFICATION,
        )

    def to_torchvision_dataset(self, transform=None, target_transform=None, transforms=None, annotation_type=None):
        # TODO: Support other kinds of datasets.
        from azureml.studio.core.io.torchvision_dataset import TorchvisionDataset
        return TorchvisionDataset(self, transform, target_transform, transforms, annotation_type)

    def get_val_in_item(self, index, name):
        """Get the raw value in one column at index."""
        raise NotImplementedError()

    def get_image_in_item(self, index, name):
        """Get the image in one image column at index."""
        raise NotImplementedError()

    def get_item_with_images(self, index):
        """Get an item at idx which and convert the bytes to images in the item."""
        data = self.image_list[index]
        return {
            name: self.get_image_in_item(index, name) if self.schema_instance.is_image_column(name) else data[name]
            for name in self.schema_names
        }

    def get_multiple_items_with_images(self, indexes):
        nthreads = min(len(indexes), cpu_count() * 2)
        with ThreadPool(nthreads) as pool:
            return pool.map(self.get_item_with_images, indexes)

    def get_item(self, index):
        """Get an item at idx.

        :param index:
        :return: A dict
        """
        return {name: self.get_val_in_item(index, name) for name in self.schema_names}

    def get_valid_annotation_indexes(self, ann_col):
        attr = self.schema_instance.column_attributes[ann_col]
        return [
            i for i, data in enumerate(self.image_list)
            if self.schema_instance.is_valid_annotation_value(attr, data.get(ann_col))
        ]

    def __len__(self):
        """Return the item count of the directory."""
        return self.size

    @classmethod
    def load(cls, load_from_dir, meta_file_path=None):
        """Load images from a directory as an ImageDirectory.

        :param load_from_dir: See AnyDirectory.
        :param meta_file_path: See AnyDirectory.
        :return: An ImageDirectory instance.
        """
        meta, image_list, schema = cls.get_meta(base_dir=load_from_dir, meta_file_path=meta_file_path)
        if image_list and schema:
            # image list and schema are required to initialize a ImageDirectory,
            # so if they can be correctly loaded from meta then it is a image directory.
            return FolderBasedImageDirectory(basedir=load_from_dir, image_list=image_list, schema=schema, meta=meta)
        else:
            # load with default parsers if not a image directory.
            image_list, schema = FolderBasedImageDirectory.parse_with_default_parsers(load_from_dir)
            return FolderBasedImageDirectory(basedir=load_from_dir, image_list=image_list, schema=schema)

    @classmethod
    def create_from_data(cls, data, schema):
        """Create a directory from data and described schema.

        :param data: example: {'attr1': [b'abc', b'def'], 'attr2': [123, 456]}
        :param schema: example:
        {ColumnAttributes: [{'name': 'attr1', 'type': 'bytes'} {'name': 'attr2', 'type': 'int'}]}
        :return: A directory instance.
        """
        schema = ImageSchema.from_dict(schema)
        if isinstance(data, dict):
            size = len(data[schema.column_attributes.names[0]])
            data = [{name: data[name][i] for name in schema.column_attributes.names} for i in range(size)]
        return MemoryBasedImageDirectory(schema=schema, datas=data)

    def dump_image(self, save_to, index):
        items = self.get_item_with_images(index)
        for name, val in items.items():
            if isinstance(val, Image.Image):
                dump_path = save_to / self.get_image_info(name, index).file_name
                ensure_folder(dump_path.parent)
                val.save(dump_path)
                logger.debug(f"Image {name}-{index} is dumped to '{dump_path}'.")

    def dump_image_list(self, save_to):
        # Before dump the image.lst file,
        # we need to drop the value base_file_name since it is only valid in current directory.
        image_list = copy.deepcopy(self._image_list)
        refs = list(self.image2ref.values())
        for data in image_list:
            for ref in refs:
                if 'base_file_name' in data[ref]:
                    data[ref].pop('base_file_name')

        dump_to_json_lines(image_list, save_to / self.IMAGE_LIST_FILE)
        logger.info(f"File {self.IMAGE_LIST_FILE} is dumped.")

    def dump(self, save_to, meta_file_path=None):
        with os_io_error_handler():
            save_to = Path(save_to)

            # Use multi thread to dump images faster.
            # If the image is from url, we use 64 threads to parallel downloading data.
            # If the image is not from url, we only need 2*cpu_count threads to load images.
            upper = 64 if isinstance(self,
                                     FolderBasedImageDirectory) and self.use_url_as_image_source else cpu_count() * 2
            nthread = min(self.size, upper)
            logger.info(f"Start dumping {self.size} image items with {nthread} threads.")
            with ThreadPool(nthread) as p:
                p.map(functools.partial(self.dump_image, save_to), range(self.size))
            logger.info(f"{self.size} image items are dumped to {save_to}.")

            self.dump_image_list(save_to)

            super().dump(save_to)

    def get_image_info(self, name, index):
        return ImageInfo.from_dict(self._image_list[index][self._image2ref[name]])

    def apply_to_images(self, transform):
        if not callable(transform):
            raise TypeError(f"Transform must be a callable wich could be applied to images.")
        return TransformedImageDirectory(self, transform)

    @classmethod
    def create_meta(cls, visualizers: list = None, extensions: dict = None):
        meta = super().create_meta(visualizers, extensions)
        meta.update_field(cls.META_IMAGE_LIST_KEY, cls.IMAGE_LIST_FILE)
        return meta

    @classmethod
    def get_meta(cls, base_dir, meta_file_path):
        # Make sure basedir is a Path object.
        base_dir = Path(base_dir)
        meta = cls.create_meta()
        image_list = None
        schema = None
        try:
            if has_meta(base_dir, meta_file_path):
                meta = Meta.load(base_dir, meta_file_path)
            image_list = load_json_lines(base_dir / meta[cls.META_IMAGE_LIST_KEY])
            schema = load_json_file(base_dir / meta.schema)
        except Exception as e:
            logger.info(f"Failed to get meta from '{base_dir}' because {type(e)} {e}.")

        return meta, image_list, schema


class FolderBasedImageDirectory(ImageDirectory):
    def __init__(self, basedir, image_list, schema, meta=None):
        # Make sure basedir is a Path object.
        basedir = Path(basedir)
        logger.info(f"Start loading images from '{basedir}'.")
        super().__init__(image_list=image_list, schema=schema, meta=meta)
        self._basedir = basedir
        image_col = self.get_image_column()
        path = self.get_image_file(0, image_col)
        url = self.get_image_url(0, image_col)
        try:
            if not path.exists() and url is None:
                raise FileNotFoundError(f"Invalid image directory, '{path}' should exist "
                                        "or image url must be provided.")
        except PermissionError as e:
            raise UserError(f"Failed to access files. Reason: {str(e)}. Please change the file permission "
                            "of your compute or use another compute with sufficient access.")
        # If the source file doesn't exist and the url is provided, the folder is using url as image source.
        self._use_url_as_image_source = not path.exists()

    @staticmethod
    def get_invalid_file_extensions(dir_path):
        return set([Path(f).suffix for f in iter_files(dir_path) if not is_image_file(f)])

    @property
    def use_url_as_image_source(self):
        """Indicate whether the folder use url to get image data."""
        return self._use_url_as_image_source

    def get_sub_dir(self, indexes):
        new_dir = copy.deepcopy(self)
        new_dir._image_list = [new_dir._image_list[i] for i in indexes]
        return new_dir

    def get_image_file(self, index, name):
        info = ImageInfo.from_dict(self._image_list[index][self._image2ref[name]])
        image_file = info.base_file_name if info.base_file_name else info.file_name
        return self._basedir / image_file

    def get_image_url(self, index, name):
        return ImageInfo.from_dict(self._image_list[index][self._image2ref[name]]).coco_url

    def get_image_in_item(self, index, name):
        if self.use_url_as_image_source:
            return image_from_url(self.get_image_url(index, name))
        return image_from_file(self.get_image_file(index, name))

    def get_val_in_item(self, index, name):
        if not self.schema_instance.is_image_column(name):
            return self.image_list[index][name]

        if self.use_url_as_image_source:
            return bytes_from_url(self.get_image_url(index, name))
        return bytes_from_file(self.get_image_file(index, name))

    def dump_image(self, save_to, index):
        lst = self._image_list[index]
        for name, ref_key in self._image2ref.items():
            info = ImageInfo.from_dict(lst[ref_key])
            image_path = info.base_file_name if info.base_file_name else info.file_name
            src_path = self._basedir / image_path
            if info.coco_url and not src_path.exists():
                logger.debug(f"Image {name}-{index} is stored with URL, skipped.")
                continue
            dst_path = save_to / info.file_name
            if dst_path != src_path:
                ensure_folder(dst_path.parent)
                shutil.copyfile(str(src_path), str(dst_path))
            logger.debug(f"Image {name}-{index} is copied from '{src_path}' to '{dst_path}'.")

    @classmethod
    def load_with_parser(cls, load_from_dir, parser):
        """Load a directory with a specific parser."""
        image_list, schema = parser(load_from_dir)
        return cls(basedir=load_from_dir, image_list=image_list, schema=schema)

    @classmethod
    def load_with_default_parsers(cls, load_from_dir):
        image_list, schema = cls.parse_with_default_parsers(load_from_dir)
        return cls(basedir=load_from_dir, image_list=image_list, schema=schema)

    @classmethod
    def parse_with_default_parsers(cls, load_from_dir):
        load_from_dir = Path(load_from_dir)
        parsers = [cls.parse_coco_folder, cls.parse_image_folder, cls.parse_images_in_one_folder]
        for parser in parsers:
            try:
                return parser(load_from_dir)
            except Exception as e:
                logger.info(f"'{load_from_dir} could not be parsed by '{parser.__name__}' due to {e}, try next parser.")
        raise ValueError(f"'{load_from_dir}' could not be parsed.")

    @classmethod
    def parse_images_in_one_folder(cls, load_from_dir):
        load_from_dir = Path(load_from_dir)
        # recursively detect image files to make thrown errors easier to understand. For example, for wrongly structured
        # image classification dataset, will return all available image files in recursive search.
        # Rather than previously 'InvalidDataset' error, 'NotLabeledDataset' error is thrown and remind user to correct
        # dataset structure in training while success in inference.
        files = (f for f in load_from_dir.glob('**/*') if is_image_file(f))

        def to_relative_path_str(f):
            return str(f.relative_to(load_from_dir).as_posix())

        image_list = [{
            ImageSchema.DEFAULT_IMAGE_REF_COL: {
                'base_file_name': to_relative_path_str(f),
                'file_name': 'image/' + to_relative_path_str(f),
            },
            ImageSchema.DEFAULT_ID_COL: i,
        } for i, f in enumerate(files)]
        id_attr = ColumnAttribute(
            name=ImageSchema.DEFAULT_ID_COL,
            # unify 'id' type to be int as other parsers.
            column_type=ColumnTypeName.NUMERIC,
            element_type=ElementTypeName.INT,
            is_feature=False,
        )
        attrs = copy.deepcopy(ImageSchema.DEFAULT_ATTRS)
        attrs[ImageSchema.DEFAULT_ID_COL] = id_attr
        return image_list, ImageSchema(column_attributes=attrs)

    @classmethod
    def load_images_in_one_folder(cls, load_from_dir):
        return cls.load_with_parser(load_from_dir, cls.parse_images_in_one_folder)

    @classmethod
    def parse_coco_folder(cls, load_from_dir, coco_json_file=None):
        load_from_dir = Path(load_from_dir)
        if coco_json_file is None:
            coco_json_file = next((f.name for f in load_from_dir.iterdir() if f.suffix == '.json'), None)
        coco_data = load_json_file(load_from_dir / coco_json_file) if coco_json_file else {}

        images, annotations = coco_data.get('images'), coco_data.get('annotations')
        if not images or not annotations:
            if coco_json_file is None:
                raise ValueError(f"coco_json_file '{coco_json_file}' is not a valid coco_json_file.")
        logger.info(f"COCO data is parsed, {len(images)} images are found, {len(annotations)} annotations are found.")

        annotation_type = ImageSchema.infer_coco_annotation_type(annotations[0])
        annotation_name = ImageSchema.get_default_annotation_col(annotation_type)
        image_list = []
        image_id2idx = {}
        # Build image_list data with images in COCO
        for image in images:
            image_id = image['id']
            base_file_name = image['file_name']
            image['base_file_name'] = base_file_name
            image['file_name'] = f'{ImageSchema.DEFAULT_IMAGE_COL}/{image_id}{Path(base_file_name).suffix}'
            image_id2idx[image_id] = len(image_list)
            image_list.append({
                ImageSchema.DEFAULT_IMAGE_REF_COL: image,
                annotation_name: [],
                ImageSchema.DEFAULT_ID_COL: image_id,
            })

        # Add annotations to each image.
        for annotation in annotations:
            image_id = annotation['image_id']
            if image_id not in image_id2idx:
                continue
            image_list[image_id2idx[image_id]][annotation_name].append(annotation)

        logger.info(f"{len(image_list)} json lines are built.")
        return image_list, ImageSchema.get_default_schema_coco(annotation_type, coco_data.get('categories'))

    @classmethod
    def load_coco_folder(cls, load_from_dir, coco_json_file=None):
        """Load a directory with images organized as COCO dataset.

        :param load_from_dir: The directory which stores images and a COCO label file.
        :param coco_json_file: The relative path of COCO label file, see http://cocodataset.org/#format-data.
        :return: An ImageDirectory.
        """
        return cls.load_with_parser(
            load_from_dir,
            functools.partial(cls.parse_coco_folder, coco_json_file=coco_json_file),
        )

    @classmethod
    def parse_image_folder(cls, load_from_dir):
        """Parse a directory with images organized as torchvision ImageFolder.
        Reference: https://pytorch.org/docs/stable/torchvision/datasets.html#imagefolder

        :param load_from_dir: The directory which stores images.
        :return: image_list: a list of json; schema: the schema of the directory.
        """

        def subdir_to_category(path):
            """Return the category from the subdir name of a path.
            Here path should be a relative path.
            ./aaa/xx.jpg => aaa
            ./bbb/yy.jpg => bbb
            ./aaa/bbb/xx.jpg => None
            ./xx.jpg => None
            """
            path = Path(path)
            base = Path('.')
            if path.parent != base and path.parent.parent == base:
                return str(path.parent)
            return None

        dir_path = Path(load_from_dir)
        logger.info(f"Start scanning path '{dir_path}'.")
        files = []
        categories = set()
        for i, f in enumerate(iter_files(dir_path, predicate=is_image_file)):
            relative = str(Path(f).relative_to(dir_path).as_posix())
            category = subdir_to_category(relative)
            logger.info(f"Image {i} is found, path='{f}', category='{category}'.")
            if category is None:
                logger.warning(f"The path '{f}' is not a valid ImageFolder path, ignore the file.")
                continue
            categories.add(category)
            files.append(relative)
        if len(files) == 0:
            raise FileNotFoundError(f"No valid image found in path '{dir_path}'.")
        logger.info(f"{len(files)} valid files are found in folder {load_from_dir}.")

        files.sort()
        categories = sorted(list(categories))
        category_to_id = {category: idx for idx, category in enumerate(categories)}
        schema = ImageSchema.get_default_classification_schema([{
            'id': i,
            'name': category
        } for i, category in enumerate(categories)])
        image_col = schema.column_attributes[0].name

        image_list = [
            {
                ImageSchema.DEFAULT_IMAGE_REF_COL: {
                    'file_name': f'{image_col}/{category_to_id[subdir_to_category(f)]}_{i}{Path(f).suffix}',
                    # file_name is the file_name which is used when dumping files,
                    # base_file_name is the file name in basedir.
                    # This is a walk around because dataset team cannot handle multiple folders,
                    # so we must keep all image files in the same folder.
                    # It would be better to keep the original file_name.
                    'base_file_name': f,
                },
                ImageSchema.DEFAULT_CLASSIFICATION_COL: subdir_to_category(f),
                ImageSchema.DEFAULT_ID_COL: i,
            } for i, f in enumerate(files)
        ]
        return image_list, schema

    @classmethod
    def load_image_folder(cls, load_from_dir):
        """Load a directory with images organized as torchvision ImageFolder.

        :param load_from_dir: The directory which stores images.
        :return: An ImageDirectory.
        """
        return cls.load_with_parser(load_from_dir, cls.parse_image_folder)


class MemoryBasedImageDirectory(ImageDirectory):
    def __init__(self, schema, datas):
        super().__init__(image_list=copy.deepcopy(datas), schema=schema)
        self._image_data = {name: [] for name in self._image2ref}
        for i, data in enumerate(self._image_list):
            for name, ref_key in self._image2ref.items():
                self._image_data[name].append(image_from(data.pop(name)))
                data[ref_key] = {'file_name': f"{name}/{i}.png"}

    @property
    def image_data(self):
        return self._image_data

    def get_image_in_item(self, index, name):
        return self._image_data[name][index]

    def get_val_in_item(self, index, name):
        if self.schema_instance.is_image_column(name):
            return image_to_bytes(self.get_image_in_item(index, name))
        return self.image_list[index][name]


class TransformedImageDirectory(ImageDirectory):
    def __init__(self, src_dir: ImageDirectory, transform: callable):
        super().__init__(copy.deepcopy(src_dir.image_list), src_dir.schema, src_dir.meta)
        if not callable(transform):
            raise ValueError(f"Callable is expected, got '{transform}'")
        self._src_dir = src_dir
        self._transform = transform
        # In a transformed ImageDirectory, base_file_name will be invalid.
        # The dumping format must be 'png' to guarantee the image data is the same.
        for data in self._image_list:
            for ref_key in self._image2ref.values():
                for key_to_pop in ['base_file_name', 'coco_url']:
                    if key_to_pop in data[ref_key]:
                        data[ref_key].pop(key_to_pop)
                    data[ref_key]['file_name'] = str(Path(data[ref_key]['file_name']).with_suffix('.png'))

    @property
    def src_dir(self):
        return self._src_dir

    @property
    def transform(self):
        return self._transform

    def get_image_in_item(self, index, name):
        return self._transform(self.src_dir.get_image_in_item(index, name))

    def get_val_in_item(self, index, name):
        if self.schema_instance.is_image_column(name):
            return image_to_bytes(self.get_image_in_item(index, name))
        return self.image_list[index][name]
