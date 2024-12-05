from abc import ABC, abstractmethod
from pandas import DataFrame
from pathlib import Path
from typing import Tuple


class CoreModel(ABC):
    """CoreModel deals with flavor-specified behaviors.
    1. Save/Load raw_model
    2. Predict result with the input of given data
    """
    @abstractmethod
    def save(self, save_to: Path, overwrite_if_exists=True):
        """Save CoreModel object to path save_to

        :param save_to: path to save, can be file path or directory path
        :param overwrite_if_exists: Overwrite exist files if true, throw exception otherwise (default: {True})
        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def load(cls, load_from: Path):
        """Load a CoreModel object from path load_from

        :param load_from: path to file or directory
        :return: CoreModel
        """
        pass

    @abstractmethod
    def predict(self, df: DataFrame, columns_types: dict = None) -> Tuple[DataFrame, dict]:
        """Function which does prediction in memory.
        Not using xxDirectory because data directly because:
         1. xxDirectory is module level concept corresponding to port_type
         2. The implementation of ModelSDK is based on the assumption that both input and output are TabularData
         3. ModelSDK deal with data in memory as predict function in main stream ML framework models, thus
            not suitable for xxDirectory because it's referencing hard disk
         xxDirectory is batched into DataFrame before passing to this function

        :param df: dataframe in memory
        :param columns_types: dict of {column_name: column_type}, column_type is from a finite set consists of pd.dtypes
                             and complex types like image, dict, ndarray, etc.
        :return: a tuple consist of two element, the result dataframe and corresponding columns_types
        """
        pass
