from pathlib import Path
from typing import Any, Union

#
# Project Manager Errors


class ProjectManagerValueError(ValueError):
    pass


class ProjectDirectoryError(ProjectManagerValueError):
    def __init__(self, path: Path, msg: str) -> None:
        self.path = path
        super().__init__(f'Invalid project directory: {msg}')


class ProjectFileError(ProjectManagerValueError):
    def __init__(self, path: Path, msg: str) -> None:
        self.path = path
        super().__init__(f'Invalid project file: {msg}')


class ProjectYamlParsingError(ProjectFileError):
    def __init__(self, path: Path, yaml_error: Exception) -> None:
        self.path = path
        self.yaml_error = yaml_error
        super().__init__(path, f'the yaml file can not be parsed; {yaml_error}')


class ParameterUnexpectedKeysError(ProjectManagerValueError):
    def __init__(self, params: Union[set[str], list[str]]) -> None:
        self.params = sorted(list(params))
        super().__init__(f'Unexpected parameters: {", ".join(self.params)}')


class ParameterMissingRequiredValuesError(ProjectManagerValueError):
    def __init__(self, params: Union[set[str], list[str]]) -> None:
        self.params = sorted(list(params))
        super().__init__(f'Missing required parameter values: {", ".join(self.params)}')


class ParameterValueTypeError(ProjectManagerValueError):
    def __init__(self, name: str, value: Any, expected_type: str) -> None:
        self.name = name
        self.value = value
        self.expected_type = expected_type
        super().__init__(f'Parameter {name} must be a {expected_type}, got {type(value).__name__}')


class SecretParameterEncryptionError(ProjectManagerValueError):
    def __init__(self, name: str, info: str) -> None:
        super().__init__(f'Parameter {name} encryption error: {info}')


class VaultParameterValueError(ProjectManagerValueError):
    def __init__(self, info: str) -> None:
        super().__init__(f'Invalid vault parameter value: {info}')


#
# Encryption Errors


class EncryptionNotSupportedError(ValueError):
    def __init__(self) -> None:
        super().__init__(
            'Your organization does not have encryption set up. Please contact your administrator'
        )
