import sys
import subprocess
import time

from azureml.designer.core.model.constants import ModelSpecConstants, DEV_OPS_EXTRA_INDEX_URL_PREFIX,\
    DESIGNER_PIP_PACKAGE_PREFIX
from azureml.studio.core.logger import get_logger
from azureml.studio.core.package_info import PACKAGE_NAME
from azureml.studio.core.utils.yamlutils import dump_to_yaml_file

logger = get_logger(__name__)

PYTHON_VERSION = "{major}.{minor}.{micro}".format(major=sys.version_info.major,
                                                  minor=sys.version_info.minor,
                                                  micro=sys.version_info.micro)


def _run_with_conditional_retry(cmds, max_try_cnt=3, sleep_between_tries_in_sec=3):
    """Retry running cmds on specified frequent cases."""
    try_index = 0
    muted_cmds = cmds
    if max_try_cnt < 1:
        raise ValueError(f"max_try_cnt should be at least 1, got {max_try_cnt}.")
    while try_index < max_try_cnt - 1:
        result = subprocess.run(muted_cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.returncode == 0:
            return result
        else:
            logger.warning(f"{' '.join(cmds)} failed on try {try_index}, returncode={result.returncode}. "
                           f"stderr: {result.stderr}")
            if cmds and cmds[0] == 'pip' and \
                    "ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE." in result.stderr:
                muted_cmds = cmds + ["--no-cache-dir"]
                logger.info("Added --no-cache-dir to command to avoid using corrupted cache.")
                time.sleep(sleep_between_tries_in_sec)
            else:
                logger.info("Retry criteria not met, will return with non-zero status code.")
                break
        try_index += 1

    return result


def _run_install_cmds(cmds, command_name):
    logger.info(" ".join(cmds))
    result = _run_with_conditional_retry(cmds)
    if result.returncode == 0:
        logger.info(f"Finished to install {command_name} dependencies.")
    else:
        logger.warning(f"Failed to install {command_name} dependencies, returncode={result.returncode}. "
                       f"Please check the stderr to determine whether this is a transient error and retry.")
    logger.info(f"stdout: {result.stdout}")
    if result.stderr:
        logger.warning(f"stderr: {result.stderr}")


def _get_current_pip_package_version_dict() -> dict:
    """Run pip freeze and return a dict of {package_name: version}, packages installed from direct url are ignored"""

    result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True)
    content = result.stdout
    # In format package_name==version
    lines = content.strip().split('\n')
    # pip freeze return format like 'pycocotools @ git+https://github.com/xxx' in PEP 610 for package from direct URL
    # since 20.1b1(2020-04-21), https://www.python.org/dev/peps/pep-0610/
    # Packages installed from direct url are not concerned in our process of suffix injection and core-version fixing,
    # so we just ignore such cases
    version_dict = {fields_in_line[0]: fields_in_line[1] for fields_in_line in [line.split('==') for line in lines]
                    if len(fields_in_line) == 2}
    return version_dict


def _regulate_designer_packages_version(pip_dependencies_to_install, current_pip_package_version_dict) -> list:
    """Inject current azureml-designer-core into pip dependencies and remove existing core dependency if exists
    to prevent alteration. Also inject version suffix of current azureml-designer-core if in test env.
    """
    if not pip_dependencies_to_install:
        return []
    # Inject suffix to package version of azureml-designer-core if:
    # 1. azure-designer-core in current environment has a '.postxxx' suffix, and
    # 2. The package is azureml-designer package which is identified if its name has prefix of 'azureml-designer'
    suffix_injected_dependencies = pip_dependencies_to_install.copy()
    if PACKAGE_NAME not in current_pip_package_version_dict:
        logger.warning(f"{PACKAGE_NAME} doesn't exist in current environment, skip core version injection.")
        return suffix_injected_dependencies
    else:
        version_str = current_pip_package_version_dict[PACKAGE_NAME]
        core_package = f"{PACKAGE_NAME}=={version_str}"
        # For test env where package is from DevOps feed and postxxx suffix exists
        if 'post' in version_str:
            version_suffix = version_str.split('.')[-1]
            dev_ops_extra_index_url_provided = False
            for line in pip_dependencies_to_install:
                if line.startswith(DEV_OPS_EXTRA_INDEX_URL_PREFIX):
                    dev_ops_extra_index_url_provided = True
                    break
            if not dev_ops_extra_index_url_provided:
                logger.warning(f"DevOps extra-index-url not provided, skip core version fixing in test env.")
                return suffix_injected_dependencies
            for i in range(len(suffix_injected_dependencies)):
                # Will not inject post version number to dependencies already having one.
                if suffix_injected_dependencies[i].startswith(DESIGNER_PIP_PACKAGE_PREFIX) \
                        and 'post' not in suffix_injected_dependencies[i]:
                    if suffix_injected_dependencies[i].endswith('*'):
                        suffix_injected_dependencies[i] = suffix_injected_dependencies[i].replace('*', version_suffix)
                    else:
                        suffix_injected_dependencies[i] = f'{suffix_injected_dependencies[i]}.{version_suffix}'

        logger.info(f"Injected {core_package} into pip dependency and removed original "
                    f"azureml-designer-core dependency if exists.")
        return [core_package] + [dep for dep in suffix_injected_dependencies if not dep.startswith(PACKAGE_NAME)]


# Temporary workaround to reconstruct the python environment in training phase.
# Should deprecate when Module team support reading the conda.yaml in Model Folder and build image according to that
class RemoteDependencyManager(object):

    def __init__(
        self,
        additional_conda_channels: list = None,
        additional_conda_deps: list = None,
        additional_pip_deps: list = None
    ):
        self.conda_channels = ["defaults"] + (additional_conda_channels or [])
        self.conda_dependencies = [f"python={PYTHON_VERSION}"] + (additional_conda_deps or [])
        self.pip_dependencies = additional_pip_deps or []

    def save(self, artifact_path, overwrite_if_exists=True):
        conda_env = {
            "name": ModelSpecConstants.CONDA_ENV_NAME,
            "channels": self.conda_channels,
            "dependencies": self.conda_dependencies + [{"pip": self.pip_dependencies}]
        }
        conda_file_path = artifact_path / ModelSpecConstants.CONDA_FILE_NAME
        if conda_file_path.exists() and not overwrite_if_exists:
            raise FileExistsError(f"Target path {conda_file_path} exists. "
                                  f"Set overwrite_if_exists=True if you want to overwrite it.")
        dump_to_yaml_file(conda_env, conda_file_path)
        logger.info(f"Saved conda to {conda_file_path}")

    def load(self, conda: dict):
        if isinstance(conda["channels"], list):
            self.conda_channels = conda["channels"]
        else:
            self.conda_channels = [conda["channels"]]

        for entry in conda["dependencies"]:
            if isinstance(entry, dict) and "pip" in entry:
                self.pip_dependencies = entry["pip"]
            # TODO: Use regex for precision
            elif entry.startswith(("python=", "python>", "python<")):
                pass
            else:
                self.conda_dependencies.append(entry)
        logger.debug(f"conda_channels = {', '.join(self.conda_channels)}")
        logger.debug(f"conda_dependencies = {', '.join(self.conda_dependencies)}")
        logger.debug(f"pip_dependencies = {', '.join(self.pip_dependencies)}")

    def install(self):
        if not self.conda_dependencies:
            logger.info("No conda dependencies to install")
        else:
            conda_cmds = ["conda", "install", "-y"]
            for channel in self.conda_channels:
                conda_cmds += ["-c", channel]
            conda_cmds += self.conda_dependencies
            _run_install_cmds(conda_cmds, command_name="conda")

        if not self.pip_dependencies:
            logger.info("No pip dependencies to install")
        else:
            current_pip_package_version_dict = _get_current_pip_package_version_dict()
            regulated_pip_dependencies = _regulate_designer_packages_version(
                self.pip_dependencies, current_pip_package_version_dict)
            if regulated_pip_dependencies:
                pip_cmds = ["pip", "install"] + self._split_index_url_with_package_version(regulated_pip_dependencies)
                _run_install_cmds(pip_cmds, "pip")

        result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True)
        logger.info(f"pip freeze result:\n{result.stdout}")

    @staticmethod
    def _split_index_url_with_package_version(package_version: list):
        # If there is space between '--extra-index-url' or '--index-url' between the url, the split into two items.
        new_package_list = []
        for p in package_version:
            if '--extra-index-url' in p or '--index-url' in p:
                new_package_list += p.split(' ')
            else:
                new_package_list.append(p)
        return new_package_list
