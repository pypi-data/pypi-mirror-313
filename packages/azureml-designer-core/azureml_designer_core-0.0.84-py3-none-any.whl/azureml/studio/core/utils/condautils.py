from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


def merge_envs(envs):
    if not envs:
        return {}

    valid_envs = list(filter(lambda x: isinstance(x, dict), envs))
    names = [env["name"] for env in valid_envs if "name" in env]
    channels_list = [env["channels"] for env in valid_envs if "channels" in env]
    dependencies_list = [env["dependencies"] for env in valid_envs if "dependencies" in env]

    merged_name = _merge_names(names)
    merged_channels = _merge_channels_lists(channels_list)
    merged_dependencies = _merge_dependencies_lists(dependencies_list)

    merged_env = {}
    if merged_name:
        merged_env["name"] = merged_name
    if merged_channels:
        merged_env["channels"] = merged_channels
    if merged_dependencies:
        merged_env["dependencies"] = merged_dependencies

    return merged_env


def _merge_names(names: list):
    for name in names:
        if name:
            return name


def _merge_channels_lists(channels_list: list):
    if not channels_list:
        return []

    merged_channels = []
    merged_channels_set = set()
    for channels in channels_list:
        for channel in channels:
            if channel not in merged_channels_set:
                merged_channels.append(channel)
                merged_channels_set.add(channel)

    return merged_channels


def _merge_dependencies_lists(dependencies_list):
    """Merge all dependencies to one list and return it.
    Two overlapping dependencies (e.g. package-a and package-a=1.0.0) are not
    unified, and both are left in the list (except cases of exactly the same
    dependency). Conda itself handles that very well so no need to do this ourselves,
    unless you want to prettify the output by hand.

    :param dependencies_list: list of lists dependencies
    :return: merged dependencies list
    """
    merged_dependencies = []
    pips_dependencies = []
    non_pip_dependencies_set = set()
    for dependencies in dependencies_list:
        for dependency in dependencies:
            if isinstance(dependency, dict):
                if "pip" in dependency:
                    pips_dependencies.append(dependency["pip"])
                else:
                    logger.warning(f"Ignored non-pip dict dependency {dependency}.")
            elif dependency not in non_pip_dependencies_set:
                merged_dependencies.append(dependency)
                non_pip_dependencies_set.add(dependency)
    merged_pip = _merge_pips(pips_dependencies)
    if merged_pip:
        merged_dependencies.append({"pip": merged_pip})
    return merged_dependencies


def _merge_pips(pips_list: list):
    """Simply concat all pip lists

    :param pips_list: list of list of pip dependencies
    :return:
    """
    return sum([pips for pips in pips_list], [])
