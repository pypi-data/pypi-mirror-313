from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from pydantic_i18n import PydanticI18n
from starlette.responses import JSONResponse

from griff.infra.fastapi.exception_handlers.validation_exception_simplifier import (
    simplify_errors,
)
from griff.utils.errors import (
    get_error_by_status_code,
)


class PydanticValidationExceptionHandler:
    def __init__(self, pydantic_i18n: PydanticI18n) -> None:
        self._i18n = pydantic_i18n

    async def dispatch(
        self, request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        current_locale = request.query_params.get("locale", self._i18n.default_locale)
        errors = self._i18n.translate(list(exc.errors()), current_locale)
        error_class = get_error_by_status_code(status.HTTP_422_UNPROCESSABLE_ENTITY)
        error = error_class(details=simplify_errors(errors))
        return JSONResponse(status_code=error.code, content=error.model_dump())
