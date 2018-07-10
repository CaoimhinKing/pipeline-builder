from distutils.version import LooseVersion, StrictVersion
from functools import reduce


class Versioner():
    def compute_next_version(self, current, previous):
        current_major_minor = _remove_patch(current)
        prev_major_minor = _remove_patch(previous)
        patch = int(_get_patch(previous))
        next_patch = _get_next_patch(
            current_major_minor, prev_major_minor, patch)

        next_version = "{}.{}".format(current_major_minor, next_patch)

        if StrictVersion(next_version) <= StrictVersion(previous):
            raise InvalidVersionError("Computed version ({}) is less than or equal to previous version ({})".format(
                next_version, previous))

        return next_version


class InvalidVersionError(Exception):
    def __init__(self, message):
        super().__init__(message)


def _get_next_patch(current_major_minor, previous_major_minor, patch):
    return 0 if StrictVersion(current_major_minor) > StrictVersion(previous_major_minor) else patch + 1


def _get_patch(version):
    return version.split(".")[-1]


def _remove_patch(version):
    return _version_list_to_string(version.split(".")[:-1])


def _version_list_to_string(version_list):
    return reduce(lambda acc, val: "{}.{}".format(acc, val), version_list)
