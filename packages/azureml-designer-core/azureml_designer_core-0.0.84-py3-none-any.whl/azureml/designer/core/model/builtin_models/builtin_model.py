import inspect
import sys
from abc import abstractmethod, ABCMeta
from pandas import DataFrame
from pathlib import Path
from typing import Tuple

from azureml.designer.core.model.core_model import CoreModel
from azureml.designer.core.model.constants import ModelSpecConstants, ScoreColumnConstants
from azureml.designer.core.model.extended_column_types import ExtendedColumnTypeName
from azureml.designer.core.model.model_spec.builtin_model_meta.builtin_model_meta import BuiltinModelMeta
from azureml.designer.core.model.model_spec.builtin_model_meta.task_type import TaskType
from azureml.studio.core.logger import get_logger


PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
logger = get_logger(__name__)


class BuiltinModelModuleStructureError(Exception):
    def __init__(self, detail=None):
        message = "BuiltinModel resides in a module which violates the design, " \
                  "please refer to BuiltinModelMetaClass for more info."
        if detail:
            message += f" Detail: {detail}."
        super().__init__(message)


class BuiltinModelMetaClass(ABCMeta):
    """Please note this is irrelevant with 'BuiltinModelMeta', which is meta information of BuiltinModel,
    while this is called 'MetaClass' only because it's a python metatclass.
    The builtin model modules are designed to locate at
    azureml.designer.core.model.builtin_models.flavor_name.serialization_method
    If the module path violates the design, exception would be thrown.
    """
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        if inspect.isabstract(cls):
            return
        module_path = cls.__module__
        # azureml.designer.core.model.builtin_models.flavor_name.serialization_method
        module_hierarchy = module_path.split('.')
        try:
            builtin_model_module_index = module_hierarchy.index('builtin_models')
        except ValueError as e:
            raise BuiltinModelModuleStructureError(
                detail=f'builtin_models missing in module path',
                caused_ex=e
            ) from e
        if len(module_hierarchy) != builtin_model_module_index + 3:
            raise BuiltinModelModuleStructureError('BuiltinModel class definition should reside in '
                                                   'builtin_models.flavor_name.serialization_method')
        cls.flavor_name = module_hierarchy[builtin_model_module_index + 1]
        cls.serialization_method = module_hierarchy[builtin_model_module_index + 2]


class BuiltinModel(CoreModel, metaclass=BuiltinModelMetaClass):
    def __init__(self,
                 raw_model: object,
                 model_meta: BuiltinModelMeta = None
                 ):
        self._raw_model = raw_model
        self._model_meta = model_meta
        self._flavor = {
            ModelSpecConstants.FLAVOR_NAME_KEY: self.flavor_name,
            ModelSpecConstants.SERIALIZATION_METHOD_KEY: self.serialization_method
        }

    @property
    def raw_model(self):
        return self._raw_model

    @property
    def model_meta(self):
        return self._model_meta

    @property
    def flavor(self):
        return self._flavor

    @property
    def task_type(self):
        if self._model_meta and self._model_meta.task_type:
            return self._model_meta.task_type
        return None

    @property
    def label_map(self):
        if self._model_meta and self._model_meta.label_map:
            return self._model_meta.label_map
        return None

    @property
    def model_inputs(self):
        if self._model_meta and self._model_meta.model_inputs:
            return self._model_meta.model_inputs
        return None

    @abstractmethod
    def save(self, save_to: Path, overwrite_if_exists=True) -> BuiltinModelMeta:
        pass

    # Load without model_spec method shouldn't be called by Builtin models, instantiated to be placeholder
    @classmethod
    def load(cls, load_from: Path):
        raise ValueError("Load without model_spec method shouldn't be called for Builtin models.")

    @classmethod
    @abstractmethod
    def load_with_model_meta(cls, load_from: Path, model_meta: BuiltinModelMeta):
        pass

    def predict(self, df: DataFrame, columns_types: dict = None) -> Tuple[DataFrame, dict]:
        preprocessed_df, preprocessed_columns_types = self._builtin_pre_process(df, columns_types)
        predict_result_df, predict_result_columns_types = self._predict(preprocessed_df, preprocessed_columns_types)
        postprocessed_df, post_processed_columns_types = self._builtin_post_process(predict_result_df,
                                                                                    predict_result_columns_types)
        return postprocessed_df, post_processed_columns_types

    @abstractmethod
    def _predict(self, df: DataFrame, columns_types: dict = None) -> Tuple[DataFrame, dict]:
        pass

    def _builtin_pre_process(self, df: DataFrame, columns_types: dict = None) -> Tuple[DataFrame, dict]:
        """Flavor-independent pre-process operations

        :param df:
        :param columns_types:
        :return:
        """
        return_columns_types = columns_types.copy() if columns_types else {}
        if self.model_inputs:
            for model_input in self.model_inputs:
                if model_input.name in df.columns and model_input.pre_processor:
                    df[model_input.name] = df[model_input.name].apply(model_input.pre_processor.transform)
                    return_columns_types[model_input.name] = model_input.pre_processor.transformed_column_type
        return df, return_columns_types

    def _builtin_post_process(self, df: DataFrame, columns_types: dict = None) -> Tuple[DataFrame, dict]:
        """Flavor-independent post-process operations. Specifically, format the result dataframe so that the
        'Evaluate Model' module can understand the output

        :param df:
        :param columns_types:
        :return: (result_df, result_column_types)
        """
        if self.task_type == TaskType.MultiClassification:
            logger.info(f"MultiClass Classification Task, Result Contains Scored Label and Scored Probability")

            # From supervised_learner.py
            def _gen_scored_probability_column_name(label):
                """Generate scored probability column names with pattern "Scored Probabilities_label" """
                return '_'.join(
                    (ScoreColumnConstants.ScoredProbabilitiesMulticlassColumnNamePattern, str(label)))

            # MultiClassification core_model will return a DataFrame with column "Scored Label Ids" and
            # "Scored Probabilities List"(with a list inside)
            # row example: (label_id, [class_0_prob, class_1_prob, ...])
            label_ids = df[ScoreColumnConstants.ScoredLabelIdsColumnName].to_list()
            probs = df[ScoreColumnConstants.ScoredProbabilitiesMulticlassColumnName].to_list()
            if probs:
                class_cnt = len(probs[0])
            else:
                return DataFrame(), None
            if self.label_map:
                columns = [_gen_scored_probability_column_name(label) for label in
                           self.label_map.ids_to_names(range(class_cnt))]
            else:
                columns = [_gen_scored_probability_column_name(label) for label in
                           [str(i) for i in range(class_cnt)]]
            result_df = DataFrame(data=probs, columns=columns)
            if self.model_meta.label_map:
                result_df[ScoreColumnConstants.ScoredLabelsColumnName] = \
                    self.model_meta.label_map.ids_to_names(label_ids)
            else:
                result_df[ScoreColumnConstants.ScoredLabelsColumnName] = [str(i) for i in label_ids]
            result_column_types = {col: ExtendedColumnTypeName.NUMERIC for col in columns}
            result_column_types[ScoreColumnConstants.ScoredLabelIdsColumnName] = ExtendedColumnTypeName.STRING
            """
            example:
                result_df:
                Scored Probabilities_dog, Scored Probabilities_cat, Scored Probabilities_frog, Scored Labels
                0.4, 0.5, 0.1, cat
                0.9, 0, 0.1, dog

                result_column_types:
                {'Scored Probabilities_dog': 'Numeric', 'Scored Probabilities_cat': 'Numeric',
                 'Scored Probabilities_frog': 'Numeric', 'Scored Labels': 'String'}
            """
            return result_df, result_column_types
        else:
            # TODO: Follow Module Team's practice to post_process result to connect to Evaluate Module
            return df, columns_types
