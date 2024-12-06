from abc import ABC

from griff.appli.message.message import Message


class Command(Message, ABC):
    ...
