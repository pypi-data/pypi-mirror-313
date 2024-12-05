from azureml.studio.core.utils.strutils import parse_version_str


class Version:
    """A class represents a semantic version."""

    __slots__ = ('major', 'minor', 'patch', 'build')

    def __init__(self, major: int = 0, minor: int = 0, patch: int = 0, build: int = 0):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.build = build

    @classmethod
    def parse(cls, string):
        return Version(*parse_version_str(string))

    @property
    def version_str(self):
        result = f"{self.major}.{self.minor}.{self.patch}"
        if self.build != 0:
            result = f"{result}.{self.build}"
        return result

    def __repr__(self):
        return self.version_str

    def __eq__(self, other):
        if isinstance(other, Version):
            return self.version_str == other.version_str
        return NotImplemented
