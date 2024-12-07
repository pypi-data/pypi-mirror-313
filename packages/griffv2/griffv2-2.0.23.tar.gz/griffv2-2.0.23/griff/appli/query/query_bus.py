from injector import inject

from griff.appli.message.message_bus import MessageBus
from griff.appli.query.query import Query
from griff.appli.query.query_dispatcher import QueryDispatcher
from griff.appli.query.query_handler import QueryResponse, QueryHandler


class QueryBus(MessageBus[Query, QueryResponse, QueryHandler]):
    @inject
    def __init__(self, dispatcher: QueryDispatcher) -> None:
        super().__init__(dispatcher)
