from abc import ABC
from typing import Any

from griff.appli.message.message import Message


class Query(Message, ABC):
    payload: Any
