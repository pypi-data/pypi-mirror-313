from gettext import gettext as _

ExceptionMsg = str | None
ExceptionDetails = dict | list | None


class GriffException(Exception):
    """
    Base class for exceptions

    Attributes:
        code (int): code like HTTP status code
        default_message (str): default error message
        details (dict): additional details
    """

    status_code = 500
    default_message: str = _("error message")

    def __init__(
        self, message: ExceptionMsg = None, details: ExceptionDetails = None
    ) -> None:
        self.message = message or self.default_message
        self.code = self.status_code
        self.details = details or None

    def __str__(self) -> str:
        return f"{self.message}"

    def get_message(self):  # pragma: no cover
        return self.message

    def get_code(self):  # pragma: no cover
        return self.code

    def get_details(self):  # pragma: no cover
        return self.details

    def to_dict(self) -> dict:  # pragma: no cover
        a_dict = {"code": self.code, "message": self.get_message()}
        if self.details is not None:
            a_dict["details"] = self.details
        return a_dict

    @classmethod
    def classname(cls) -> str:  # pragma: no cover
        return str(cls)

    @classmethod
    def short_classname(cls) -> str:  # pragma: no cover
        return cls.__name__


class NotFoundException(GriffException):
    """Raised when something is not found"""

    status_code = 404


class AlreadyExistsException(GriffException):
    """Raised when something already exists"""

    status_code = 409
    default_message = _("Entity or Aggregate already exists")


class ValidationException(GriffException):
    """Raised when data validation failed"""

    status_code = 422
    default_message = _("Unprocessable Entity")


class UnauthorizedException(GriffException):
    """Raised when Authorization failed"""

    status_code = 401
    default_message = _("Unauthorized")


class AuthenticationTimeoutException(GriffException):
    """Raise when Authentification Timeout"""

    status_code = 403
    default_message = _("Authentication Timeout")


class AccessForbiddenException(GriffException):
    """Raise when access is forbidden"""

    status_code = 403
    default_message = _("Access Forbidden")


class BadRequestException(GriffException):
    """
    Raise on an apparent client (e.g., malformed request syntax, size too large, ...)
    """

    status_code = 400
    default_message = _("Bad Request")


class ServiceUnavailableException(GriffException):
    """
    Raise when cannot handle the request (because it is overloaded or down for
    maintenance). Generally, this is a temporary state
    """

    status_code = 503
    default_message = _("Service temporarily unavailable, try again later.")


class EntityNotFoundException(NotFoundException):
    default_message = _("Entity not found")
