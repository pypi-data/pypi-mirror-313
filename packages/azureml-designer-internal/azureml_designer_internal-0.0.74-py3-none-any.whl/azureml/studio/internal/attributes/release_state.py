from enum import Enum

from azureml.studio.core.utils.yamlutils import register_yaml_representer


class ReleaseState(Enum):
    # No quality assigned. This should be used only in the upload
    # tools to specify that all modules are to be uploaded.
    NONE = 0

    # Module is under development and may have no testing.
    Alpha = 1

    # Unit testing in place for supported inputs.
    Beta = 2

    # Module has full testing suite for positive, negative, performance, and stress tests.
    Release = 3

    # From outside the regular module process; no testing guarantees.
    Custom = 4

    # Used for internal test, test automation, etc.
    Diagnostic = 5

    # Scheduled to be removed in a future release.
    Deprecated = 6

    # Module needs to be deprecated after uploading
    # since this module needs to be hidden from user
    ReleaseHidden = 7

    @staticmethod
    def to_yaml(representer, obj):
        return representer.represent_str(obj.name)

    @staticmethod
    def from_name(name):
        """Given a name of ReleaseState, find a corresponding item in ReleaseState enum.

        :param name: The name of ReleaseState.
        :return: The corresponding item in ReleaseState enum.
        """
        for e in ReleaseState:
            if e.name.lower() == name.lower():
                return e
        else:
            raise ValueError(f"Unrecognized release state {name}")


register_yaml_representer(ReleaseState, ReleaseState.to_yaml)
