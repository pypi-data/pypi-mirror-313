from griff.appli.message.message_dispatcher import MessageDispatcher
from griff.appli.query.query import Query
from griff.appli.query.query_handler import QueryResponse


class QueryDispatcher(MessageDispatcher[Query, QueryResponse]):
    ...
