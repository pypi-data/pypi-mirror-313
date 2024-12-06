from abc import ABC

from pydantic import BaseModel


class ApiIn(BaseModel, ABC):  # pragma: no cover
    ...


class ApiOut(BaseModel, ABC):  # pragma: no cover
    ...
