from pathlib import Path
from typing import Any, Optional

from ._version import __current_version__, __package_name__

"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// IO Errors and Warnings
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""


class InvalidFilenameError(ValueError):
    """
    Raised when an invalid filename is used

    :param key: key of the argument

    :param filename: filename that is invalid
    :type filename: :class:`str` or :class:`Path <pathlib.Path>`
    """
    def __init__(self, key: str, filename: str | Path):
        self.key = key
        self.filename = filename
        super().__init__(f"Argument {self.key} has invalid filename {self.filename}."
                         f"Please use only alphanumeric characters, spaces, and underscores.")


class InvalidExtensionWarning(UserWarning):
    """
    Raised when an invalid file extension is used

    :param key: key of the argument

    :param extension: extension that is invalid

    :param permitted: permitted extension/s
    :type permitted: :class:`str` or :class:`tuple`\[:class:`str`\]

    :param coerced: coerced extension
    :type coerced: :class:`Optional <typing.Optional>`\[:class:`str`\], default: ```None```
    """
    def __init__(self,
                 key: str,
                 extension: str,
                 permitted: str | tuple[str, ...],
                 coerced: Optional[str] = None):
        self.key = key
        self.extension = extension
        self.permitted = permitted
        self.coerced = coerced if coerced else permitted
        super().__init__(f"Argument {self.key} has invalid file extension {self.extension}. "
                         f"Expected extension {self.permitted} and coerced to {self.permitted}.")


class MissingFilesError(FileNotFoundError):
    """
    Raised when multiple files are missing
    """
    def __init__(self, missing_files: dict[str, Path]):
        self.missing_files = missing_files
        super().__init__(self.generate_message())

    def generate_message(self) -> str:
        message = "The following files are missing:\n"
        for name, file in self.missing_files.items():
            message += f"{name}: {file}"
            message += "\n"
        return message


"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Validation Errors and Warnings
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""


class EnumNameValueMismatchError(ValueError):
    """
    Raised when the name and value of a serialized enumeration do not match

    :param name: name of the enumeration

    :param value: value of the enumeration
    """
    def __init__(self, enum: Any, name: str, value: int):
        self.name = name
        self.value = value
        # noinspection PyCallingNonCallable
        super().__init__(f"Name {self.name} and value {self.value} of the enumeration do not match."
                         f"Expected {enum.__name__}({self.name}, {enum(value)}).")


class DuplicateExperimentError(ValueError):
    """
    Raised when an experiment is already included in the experiments for a particular subject

    :param alias: experiment that is already registered
    """
    def __init__(self, alias: str):
        super().__init__(f"{alias} is already registered. Consider using a different name.")


class DuplicateRegistrationError(ValueError):
    """
    Raised when an experiment is already registered

    :param alias: experiment that is already registered
    """
    def __init__(self, alias: str):
        super().__init__(f"{alias} is already registered. Consider using a different name or "
                         f"registering the class with an alias.")


class ExperimentNotRegisteredError(KeyError):
    """
    Raised when an experiment is not registered

    :param experiment: experiment that is not registered
    """
    def __init__(self, experiment: Any):
        self.experiment = experiment
        super().__init__(f"{self.experiment} is not registered.")


class AnalysisNotRegisteredError(KeyError):
    """
    Raised when an experiment is not registered

    :param experiment: experiment that is not registered
    """

    def __init__(self, experiment: Any):
        self.experiment = experiment
        super().__init__(f"{self.experiment} is not registered.")


"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Version Errors and Warnings
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""


def _config_mismatch_message(version: str) -> str:
    """
    Message for version mismatch

    :param version: Detected version that mismatches the current version

    :return: Config mismatch introduction message
    """
    return (f"Imported organization was not saved with the current version of "
            f"{__package_name__} ({__current_version__}); detected version: {version}.")


class UpdateVersionWarning(UserWarning):
    """
    Raised when the organization's version is a more recent patch than the currently installed version of the package.

    :param version: detected version
    """
    def __init__(self, version: str):
        super().__init__(_config_mismatch_message(version))


class VersionForwardCompatibilityWarning(UserWarning):
    """
    Raised when the configuration major version does not match the expected major version
    (forward compatibility of major versions)

    :param version: detected version
    """
    def __init__(self, version: str):
        message = _config_mismatch_message(version)
        message += "Forward compatibility of major versions is not guaranteed!"
        super().__init__(message)


class VersionBackwardCompatibilityWarning(UserWarning):
    """
    Raised when the configuration minor version does not match the expected minor version
    (backward compatibility of minor versions)

    :param version: detected version
    """

    def __init__(self, version: str):
        super().__init__(f"{_config_mismatch_message(version)} "
                         f"Backward compatibility of minor versions is not guaranteed!")


class VersionBackwardCompatibilityError(ValueError):
    """
    Raised when the configuration major version does not match the major expected version.
    (backward compatibility of major versions)

    :param version: detected version
    """
    def __init__(self, version: str):
        message = _config_mismatch_message(version)
        message += "Exporgo does not support backwards compatibility of major versions!"
        super().__init__(message)


"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Access Errors and Warnings
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""


class FileLockError(PermissionError):
    """
    Raised when a file is locked by another process

    :param file: file that is locked
    """
    def __init__(self, file: Path):
        self.file = file
        super().__init__(f"File {self.file} is locked by another process.")


class SingletonError(RuntimeError):
    """
    Raised when attempting to create a second instance of a singleton
    """

    def __init__(self, singleton: object):
        self.singleton = singleton
        name = self.singleton.__name__ if hasattr(self.singleton, "__name__") \
            else type(self.singleton).__name__
        super().__init__(f"{name} is a singleton and cannot be instantiated more than once")


class ImmutableInstanceWarning(RuntimeWarning):
    """
    Raised when attempting to set an attribute on an immutable instance
    """
    def __init__(self, instance: object):
        self.instance = instance
        super().__init__(f"{self.instance.__class__.__name__} is immutable and cannot be modified")


"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Runtime Errors and Warnings
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""


class DispatchError(RuntimeError):  # pragma: no cover
    """
    Raised when a dispatch error occurs
    """
    def __init__(self, dispatcher: Any, args: Optional[Any] = None):
        self.dispatcher = dispatcher
        super().__init__(f"Dispatch error with {self.dispatcher} given {args}")
