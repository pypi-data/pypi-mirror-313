import os
import sys
import shutil
import tempfile
from pathlib import Path

from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.studio.core.error import LocalDependencyValueError
from azureml.studio.core.logger import get_logger
from azureml.studio.core.utils.fileutils import ensure_folder, make_zipfile, unzip_dir

logger = get_logger(__name__)


def _is_python_module(directory_path) -> bool:
    """Determine whether a directory is python module, i.e. contains __init__.py"""
    return "__init__.py" in os.listdir(directory_path)


class LocalDependencyManager(object):
    """Manage local code dependencies of the model."""

    def __init__(self, local_dependencies: list = None):
        """Instantiate LocalDependencyManager with list of dependencies

        :param local_dependencies: list contains python file path or python module search path (as in PYTHONPATH)
        """
        self.local_dependencies = local_dependencies or []
        self.copied_local_dependencies = []

    def save(self, artifact_path, overwrite_if_exists=True):
        self.copied_local_dependencies = []
        src_abs_paths = [dependency.resolve() for dependency in self.local_dependencies]
        logger.debug(f"src_abs_paths = {src_abs_paths}")
        with tempfile.TemporaryDirectory() as temp_dir_path:
            logger.debug(f"Created temp dir {temp_dir_path}")
            dst_root_dir = Path(temp_dir_path)
            # Copy pyfiles
            src_py_files = list(filter(lambda x: str(x).endswith(".py"), src_abs_paths))
            if src_py_files:
                py_filenames = [file_path.name for file_path in src_py_files]
                if len(set(py_filenames)) < len(py_filenames):
                    raise LocalDependencyValueError("There are duplication in dependency py file name, "
                                                    "which is not allowed.")
                pyfiles_basepath = dst_root_dir / ModelSpecConstants.LOCAL_DEPENDENCIES_PY_FILES_PATH
                for filename, src_path in zip(py_filenames, src_py_files):
                    shutil.copyfile(src_path, str(pyfiles_basepath / filename))
                self.copied_local_dependencies.append(Path(ModelSpecConstants.LOCAL_DEPENDENCIES_PATH) /
                                                      ModelSpecConstants.LOCAL_DEPENDENCIES_PY_FILES_PATH)

            # Copy directories
            src_directories = list(filter(lambda x: not str(x).endswith(".py"), src_abs_paths))
            if src_directories:
                dirname_cnt_dict = {}
                for directory in src_directories:
                    if not directory.is_dir():
                        raise LocalDependencyValueError(
                            f"Only py files and directories are supported, got {directory}.")

                for src_dir_path in src_directories:
                    is_effective = False
                    dst_dir_name = src_dir_path.name
                    dirname_cnt_dict[dst_dir_name] = dirname_cnt_dict.get(dst_dir_name, 0) + 1
                    if dirname_cnt_dict[dst_dir_name] > 1:
                        dst_dir_name = f"{dst_dir_name}_{dirname_cnt_dict[dst_dir_name] - 1}"
                    dst_dir_path = dst_root_dir / dst_dir_name
                    for sub_item_name in os.listdir(src_dir_path):
                        src_sub_item_path = src_dir_path / sub_item_name
                        dst_sub_item_path = dst_dir_path / sub_item_name
                        if src_sub_item_path.is_file() and sub_item_name.endswith(".py"):
                            is_effective = True
                            ensure_folder(dst_sub_item_path.parent)
                            shutil.copyfile(str(src_sub_item_path), str(dst_sub_item_path))
                        if src_sub_item_path.is_dir() and _is_python_module(src_sub_item_path):
                            is_effective = True
                            shutil.copytree(src_sub_item_path, dst_sub_item_path,
                                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                    if is_effective:
                        self.copied_local_dependencies.append(
                            Path(ModelSpecConstants.LOCAL_DEPENDENCIES_PATH) / dst_dir_name)

            if dst_root_dir.is_dir():
                zip_file_path = artifact_path / ModelSpecConstants.LOCAL_DEPENDENCIES_ZIP_FILE_NAME
                if zip_file_path.exists() and not overwrite_if_exists:
                    raise FileExistsError(f"Save target path {artifact_path} exists."
                                          f"Set overwrite_if_exists=True if you want to overwrite it.")
                make_zipfile(zip_file_path, dst_root_dir)
                logger.info(f"Zipped local_dependencies into {zip_file_path}. Removing original directory.")

    def load(self, artifact_path, relative_paths):
        temp_local_dependency_path = None
        if relative_paths:
            zip_file_path = artifact_path / ModelSpecConstants.LOCAL_DEPENDENCIES_ZIP_FILE_NAME
            if not zip_file_path.is_file():
                raise FileNotFoundError(f"Failed to load local_dependencies because {zip_file_path} is missing.")
            temp_local_dependency_path = Path(tempfile.mkdtemp())
            self.local_dependencies = [(temp_local_dependency_path / path).resolve() for path in relative_paths]
            logger.info(f"local_dependencies = {self.local_dependencies}")
            unzip_dir(zip_file_path, temp_local_dependency_path / ModelSpecConstants.LOCAL_DEPENDENCIES_PATH)
            logger.info(f"Unzipped {zip_file_path} to {temp_local_dependency_path}.")
        return temp_local_dependency_path

    def install(self):
        for local_dependency_path in self.local_dependencies:
            sys.path.append(str(local_dependency_path))
            logger.info(f"Appended {local_dependency_path} to sys.path")
