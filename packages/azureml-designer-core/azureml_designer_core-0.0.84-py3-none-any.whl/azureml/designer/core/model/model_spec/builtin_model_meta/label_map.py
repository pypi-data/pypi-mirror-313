import os

import pandas as pd
from pathlib import Path


class LabelMap(object):

    def __init__(self, index_to_label_dict=None):
        self._index_to_label_dict = index_to_label_dict or {}

    def save(self, save_to, overwrite_if_exists=True):
        if os.path.exists(save_to) and not overwrite_if_exists:
            raise FileExistsError(f"Target path {save_to} exists. "
                                  f"Set overwrite_if_exists=True if you want to overwrite it.")
        index_list = list(self._index_to_label_dict.keys())
        label_list = list(self._index_to_label_dict.values())
        df = pd.DataFrame(index=index_list, data={"label": label_list})
        df.to_csv(save_to)

    @classmethod
    def create_from_csv(cls, file_path):
        """create LabelMap from csv file. The csv file should be of format:
        ~~~
        , label
        label_id0, label0
        label_id1, label1
        ...
        label_idn, labeln
        ~~~

        :param file_path: path to csv file
        :return:
        """
        df = pd.read_csv(file_path, index_col=0)
        return LabelMap(df.to_dict()["label"])

    @classmethod
    def create_from_dict(cls, label_dict):
        return LabelMap(label_dict)

    @classmethod
    def create_from_list(cls, label_list):
        return LabelMap(dict(enumerate(label_list)))

    # TODO: Add input validation here
    @classmethod
    def create(cls, param):
        if isinstance(param, (str, Path)):
            return cls.create_from_csv(param)
        if isinstance(param, dict):
            return cls.create_from_dict(param)
        if isinstance(param, list):
            return cls.create_from_list(param)

    @property
    def index_to_label_dict(self):
        return self._index_to_label_dict.copy()

    # TODO: implement this
    def names_to_ids(self):
        raise NotImplementedError

    def ids_to_names(self, label_ids) -> list:
        """Transform label_ids to corresponding label_names.
        If element in label_ids is not present in self._index_to_label_dict, transform it into itself

        :param label_ids: list of label_id
        :return: list of label_name
        """
        return [self._index_to_label_dict.get(i, str(i)) for i in label_ids]
