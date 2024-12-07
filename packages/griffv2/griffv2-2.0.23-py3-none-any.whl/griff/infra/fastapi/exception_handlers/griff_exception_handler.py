from fastapi import Request
from loguru import logger
from starlette import status
from starlette.responses import JSONResponse

from griff.infra.fastapi.exception_handlers.validation_exception_simplifier import (
    simplify_errors,
)
from griff.utils.errors import (
    get_error_by_status_code,
)
from griff.utils.exceptions import GriffException


async def griff_exception_handler(
    request: Request, exception: GriffException
) -> JSONResponse:  # pragma: no cover
    status_code = (
        exception.status_code
        if hasattr(exception, "status_code")
        else status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    error_class = get_error_by_status_code(status_code)
    details = exception.details
    if status_code == 422:
        details = simplify_errors(details or [])  # type: ignore
    error = error_class(
        name=exception.short_classname().replace("Exception", "Error"),
        message=exception.message,
        details=details,
    )
    logger.info(f"GriffException: {error}")
    return JSONResponse(status_code=error.code, content=error.model_dump())
