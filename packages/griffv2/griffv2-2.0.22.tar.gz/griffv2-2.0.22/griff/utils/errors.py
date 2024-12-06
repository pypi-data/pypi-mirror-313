import typing
from abc import ABC
from typing import Any, Type

from pydantic import BaseModel, model_validator


class BaseError(BaseModel, ABC):  # pragma: no cover
    code: int
    name: str | None = None
    message: str
    details: dict | None = None

    @model_validator(mode="before")
    @classmethod
    def set_name_from_classname(cls, data: Any) -> str:
        if isinstance(data, dict) and "name" not in data:
            data["name"] = cls.__name__
        return data

    @classmethod
    def short_classname(cls) -> str:
        return cls.__name__


class UnauthorizedError(BaseError, ABC):  # pragma: no cover
    code: int = 401
    message: str = "unauthorized access"


class AccessForbiddenError(BaseError, ABC):  # pragma: no cover
    code: int = 403
    message: str = "access forbidden"


class NotFoundError(BaseError, ABC):  # pragma: no cover
    code: int = 404
    message: str = "not found"


class ConflictError(BaseError, ABC):  # pragma: no cover
    code: int = 409
    message: str = "conflict error"


class ValidationError(BaseError, ABC):  # pragma: no cover
    code: int = 422
    message: str = "validation error"


class InternalError(BaseError, ABC):  # pragma: no cover
    code: int = 500
    message: str = "internal error"


class DefaultExceptionHandlerError(BaseError):
    pass


Error = (
    UnauthorizedError
    | AccessForbiddenError
    | NotFoundError
    | ConflictError
    | ValidationError
    | InternalError
)


@typing.no_type_check
def get_error_by_status_code(status_code: int) -> Type[Error]:
    return {
        401: UnauthorizedError,
        403: AccessForbiddenError,
        404: NotFoundError,
        409: ConflictError,
        422: ValidationError,
        500: InternalError,
    }[status_code]
