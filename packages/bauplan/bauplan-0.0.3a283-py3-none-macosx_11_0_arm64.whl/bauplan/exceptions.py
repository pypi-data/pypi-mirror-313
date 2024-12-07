from .state import TableCreatePlanApplyState, TableCreatePlanState


class BauplanError(Exception):
    pass


class InvalidDataError(BauplanError):
    """400 status from API"""

    pass


class UnauthorizedError(BauplanError):
    """401 status from API"""

    pass


class AccessDeniedError(BauplanError):
    """403 status from API"""

    pass


class ResourceNotFoundError(BauplanError):
    """404 status from API"""

    pass


class ApiMethodError(BauplanError):
    """404 status from API"""

    pass


class ApiRouteError(BauplanError):
    """405 status from API"""

    pass


class UpdateConflictError(BauplanError):
    """409 status from API"""

    pass


class TooManyRequestsError(BauplanError):
    """429 status from API"""

    pass


class BauplanInternalError(BauplanError):
    """500 status from API"""

    pass


# Exceptions raised during loading of object
class UserObjectKeyNotExistsError(BauplanError):
    pass


class MismatchedPythonVersionsError(BauplanError):
    pass


# Exceptions raised during saving object
class UserObjectWithKeyExistsError(BauplanError):
    pass


class ObjectTooBigError(BauplanError):
    pass


class ObjectCannotBeSerializedError(BauplanError):
    pass


class UnhandledRuntimeError(BauplanError):
    pass


# Exceptions during a run


class NoResultsFoundError(BauplanError):
    pass


class JobError(BauplanError):
    pass


# Exceptions during an import


class InvalidPlanError(BauplanError):
    pass


class MissingPandasError(BauplanError):
    def __init__(self) -> None:
        super().__init__('Pandas is not installed. Please do `pip3 install pandas` to resolve this error.')


class MissingMagicCellError(BauplanError):
    def __init__(self) -> None:
        super().__init__(
            '`from IPython.core.magic import register_cell_magic` failed: are you in a Python notebook context? You can do `pip3 install jupyterlab` to resolve this error.'
        )


# Exceptions during table creation


class TableCreatePlanError(BauplanError):
    pass


class TableCreatePlanStatusError(TableCreatePlanError):
    def __init__(self, message: str, state: TableCreatePlanState, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.state = state


class TableCreatePlanApplyStatusError(BauplanError):
    def __init__(self, message: str, state: TableCreatePlanApplyState, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.state = state
