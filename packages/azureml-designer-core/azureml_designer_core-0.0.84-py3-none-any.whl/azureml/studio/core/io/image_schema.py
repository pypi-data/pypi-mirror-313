import copy

from azureml.studio.core.utils.labeled_list import LabeledList
from azureml.studio.core.schema import Schema, ColumnTypeName, ElementTypeName, ColumnAttribute


class ImageAnnotationTypeName:
    CLASSIFICATION = 'COCO_classification'
    SEMANTIC_SEGMENTATION = 'COCO_semantic_segmentation'
    OBJECT_DETECTION = 'COCO_object_detection'
    KEYPOINT_DETECTION = 'COCO_keypoint_detection'
    CAPTION = 'COCO_image_caption'

    UNKNOWN = 'COCO_unknown'

    PREFIX = 'COCO_'


class ImageInfo:
    __slots__ = ['file_name', 'width', 'height', 'coco_url', 'base_file_name', 'id']

    def __init__(self, file_name, width=None, height=None, coco_url=None, base_file_name=None, id=None):
        self.file_name = file_name
        self.width = width
        self.height = height
        self.coco_url = coco_url
        self.base_file_name = base_file_name
        self.id = id

    def to_dict(self):
        result = {}
        for key in self.__slots__:
            val = getattr(self, key)
            if val is not None:
                result[key] = val

    @classmethod
    def from_dict(cls, data):
        data = {k: v for k, v in data.items() if k in cls.__slots__}
        return cls(**data)


class ImageSchema(Schema):

    MIME_TYPE_KEY = 'mime_type'
    IMAGE_REF_KEY = 'image_ref'
    ANNOTATION_KEY = 'annotation_type'
    CATEGORY_KEY = 'categories'

    DEFAULT_IMAGE_COL = 'image'
    DEFAULT_IMAGE_REF_COL = 'image_info'
    DEFAULT_MIME_TYPE = 'image/png'
    DEFAULT_ID_COL = 'id'

    DEFAULT_CLASSIFICATION_COL = 'category'

    DEFAULT_ATTRS = LabeledList.from_items([
        ColumnAttribute(
            name=DEFAULT_IMAGE_COL, column_type=ColumnTypeName.BYTES, element_type=ElementTypeName.BYTES,
            properties={
                MIME_TYPE_KEY: DEFAULT_MIME_TYPE,
                IMAGE_REF_KEY: DEFAULT_IMAGE_REF_COL,
            },
        ),
        ColumnAttribute(
            name=DEFAULT_ID_COL, column_type=ColumnTypeName.NUMERIC, element_type=ElementTypeName.INT, is_feature=False,
        ),
    ])

    def is_image_column(self, attr_or_col):
        attr = attr_or_col if isinstance(attr_or_col, ColumnAttribute) else self.column_attributes[attr_or_col]
        return attr.element_type == ElementTypeName.BYTES and \
            attr.properties.get(self.MIME_TYPE_KEY) == self.DEFAULT_MIME_TYPE

    def get_image_column(self):
        for attr in self.column_attributes:
            if self.is_image_column(attr):
                return attr.name
        raise ValueError(f"No valid image column is found in schema")

    def get_annotation_column(self, annotation_type=None):
        for attr in self.column_attributes:
            if self.ANNOTATION_KEY in attr.properties:
                attr_annotation_type = attr.properties[self.ANNOTATION_KEY]
                if annotation_type is None or attr_annotation_type == annotation_type:
                    return attr.name
        raise ValueError(f"No valid annotation column is found in schema.")

    def is_valid_annotation_value(self, attr_or_col, val):
        """Check whether a value is a valid annotation.
        TODO: More detailed check according to annotation type.
        """
        # All int values are valid annotations.
        if isinstance(val, int):
            return True
        # For dict or list, val should have at least 1 items
        if isinstance(val, (dict, list)) and len(val) > 0:
            return True
        # For other values, val should not be empty.
        if val:
            return True
        return False

    def get_annotation_type(self):
        column_name = self.get_annotation_column()
        return self.column_attributes[column_name].properties[self.ANNOTATION_KEY]

    def get_image_to_ref(self):
        image2ref = {}
        for attr in self.column_attributes:
            if self.is_image_column(attr):
                image2ref[attr.name] = attr.properties[self.IMAGE_REF_KEY]
        return image2ref

    def get_categories(self, annotation_name):
        return self.column_attributes[annotation_name].properties.get('categories', [])

    @classmethod
    def get_default_annotation_col(cls, annotation_type):
        if annotation_type.startswith(ImageAnnotationTypeName.PREFIX):
            annotation_type = annotation_type[len(ImageAnnotationTypeName.PREFIX):]
        return annotation_type + '_annotation'

    @classmethod
    def get_default_coco_annotation_attr(cls, annotation_type, categories):
        properties = {cls.ANNOTATION_KEY: annotation_type}
        if categories is not None:
            properties[cls.CATEGORY_KEY] = categories
        column_name = cls.get_default_annotation_col(annotation_type)
        return ColumnAttribute(
            name=column_name, column_type=ColumnTypeName.OBJECT, element_type=ElementTypeName.OBJECT,
            is_feature=False, properties=properties,
        )

    @classmethod
    def get_default_schema_coco(cls, annotation_type, categories=None, attr: ColumnAttribute = None):
        attrs = copy.deepcopy(cls.DEFAULT_ATTRS)
        if attr is None:
            attr = cls.get_default_coco_annotation_attr(annotation_type, categories)
        attrs.append(attr.name, attr)
        return ImageSchema(column_attributes=attrs)

    @classmethod
    def get_default_classification_schema(cls, categories):
        attr = ColumnAttribute(
            name=cls.DEFAULT_CLASSIFICATION_COL,
            column_type=ColumnTypeName.STRING, element_type=ElementTypeName.STRING,
            is_feature=False,
            properties={
                cls.ANNOTATION_KEY: ImageAnnotationTypeName.CLASSIFICATION,
                cls.CATEGORY_KEY: categories,
            })
        return cls.get_default_schema_coco(annotation_type=ImageAnnotationTypeName.CLASSIFICATION, attr=attr)

    @staticmethod
    def infer_coco_annotation_type(annotation):
        """Get annotation type according to the annotation data.
        See http://cocodataset.org/#format-data for more detail.
        """
        if 'caption' in annotation:
            return ImageAnnotationTypeName.CAPTION
        if 'keypoints' in annotation:
            return ImageAnnotationTypeName.KEYPOINT_DETECTION
        # For semantic segmentation case, another image is used as an annotation.
        if 'file_name' in annotation:
            return ImageAnnotationTypeName.SEMANTIC_SEGMENTATION
        if 'segmentation' in annotation or 'bbox' in annotation:
            return ImageAnnotationTypeName.OBJECT_DETECTION
        return ImageAnnotationTypeName.UNKNOWN
