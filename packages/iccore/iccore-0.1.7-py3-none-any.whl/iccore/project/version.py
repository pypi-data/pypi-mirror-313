"""
This module has functionality for representing and
manipulating project version numbers.
"""

from copy import deepcopy

from pydantic import BaseModel


class Version(BaseModel):
    """
    Representation of a package version number.

    This resembles a semver scheme but doesn't necessarily
    follow one.

    Args:
        content (str): Version in string form x.y.zzzz
        scheme (str): The versioning scheme to use, 'semver' or 'date'

    Attributes:
        major (int): Major version number
        minor (int): Minor version number
        patch (int): Path version number
        scheme (str): Versioning scheme to use
    """

    major: int
    minor: int
    patch: int
    scheme: str = "semver"

    def increment(self, field="patch"):
        """
        Increment the version number, depending on the provided field.

        Args:
            field (str): The field to increment, can be 'major', 'minor', 'patch'.
        """

        if self.scheme == "semver":
            if field == "patch":
                self.patch += 1
            elif field == "minor":
                self.patch = 0
                self.minor += 1
            elif field == "major":
                self.major += 1
                self.minor = 0
                self.patch = 0

    def as_string(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def increment(version: Version, field="patch") -> Version:
    ret = deepcopy(version)
    ret.increment(field)
    return ret


def parse(content: str, scheme: str = "semver") -> Version:
    """
    Parse the version from the input content, assumes 'major.minor.patch' format.
    """
    major, minor, patch = content.split(".")
    return Version(major=int(major), minor=int(minor), patch=int(patch), scheme=scheme)
