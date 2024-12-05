from collections import defaultdict
import os

from ruamel.yaml import YAML, ruamel, RoundTripRepresenter, RoundTripDumper

from azureml.studio.core.utils.fileutils import ensure_folder


# ruamel supports dumping most of built-in python classes to yaml file,
# but with some exceptions. Add the missing ones here.
# NOTE: use add_multi_representer to add to super classes.
def register_yaml_representer(cls, representer):
    RoundTripRepresenter.add_representer(cls, representer)


# Set default supported classes which can dumped as yaml
register_yaml_representer(defaultdict, RoundTripRepresenter.represent_dict)

# A general entry for yaml operations.
# Put at top level so that we can share the instance across the project.
yaml = YAML()


class CustomizedDumper(RoundTripDumper):
    """This class is to enable the dumping of non-ascii strings on Windows platforms."""
    def __init__(self, stream, **kwargs):
        kwargs.pop('allow_unicode')
        super().__init__(stream, allow_unicode=False, **kwargs)


def dump_to_yaml(obj, stream):
    ruamel.yaml.round_trip_dump(obj, stream, Dumper=CustomizedDumper)


def dump_to_yaml_file(obj, filename):
    ensure_folder(os.path.dirname(os.path.abspath(filename)))
    with open(filename, 'w') as fout:
        dump_to_yaml(obj, fout)


def load_yaml(stream):
    return ruamel.yaml.safe_load(stream)


def load_yaml_file(filename):
    with open(filename, 'r') as fin:
        return load_yaml(fin)
