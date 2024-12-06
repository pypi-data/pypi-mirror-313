import copy
import datetime
from typing import Any, Union, Annotated
from gettext import gettext as _
import arrow
from arrow import Arrow
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

DateTimeIn = Union[str, datetime.datetime, datetime.date, int, float, Arrow]


class DateTime:
    _parse_error = _("datetime invalid (YYYY-MM-DD HH:mm:ss.SSSSSS)")

    def __init__(self, datetime: DateTimeIn):
        self._value = (
            datetime if isinstance(datetime, Arrow) else self._check_is_valid(datetime)
        )
        self._timezone = "UTC"

    def to_mysql_date(self) -> str:
        return self._format("YYYY-MM-DD")

    def to_mysql_datetime(self) -> str:
        return self._format("YYYY-MM-DD HH:mm:ss.SSSSSS")

    def to_date(self) -> datetime.date:
        return self._value.date()

    def to_datetime(self) -> datetime.datetime:
        return self._value.to(self._timezone).datetime

    def to_timestamp(self) -> float:
        return self._value.timestamp()

    def copy(self):
        return copy.copy(self)

    def format(self, format: str):
        return self._format(format)

    @classmethod
    def _check_is_valid(cls, value: Any) -> Arrow:
        try:
            return arrow.get(value)
        except (TypeError, arrow.parser.ParserError):
            raise ValueError(_(cls._parse_error))

    def __copy__(self):
        return DateTime(self._value)

    def __repr__(self):
        return self._value.format("YYYY-MM-DDTHH:mm:ss.SSSSSSZZ")

    def __eq__(self, other):
        return self._value == other._value

    def __ne__(self, other):
        return self._value != other._value

    def __ge__(self, other):
        return self._value >= other._value

    def __le__(self, other):
        return self._value <= other._value

    def __gt__(self, other):
        return self._value > other._value

    def __lt__(self, other):
        return self._value < other._value

    def _format(self, date_format) -> str:
        return self._value.to(self._timezone).format(date_format)

    def shift(self, shifting_amount: dict) -> "DateTime":
        """
        Shift a date with the amount

        Args:
            d (str|Arrow|datetime.datetime|datetime.date): arrow date to shift from
            shifting_amount (dict):  shifting amount (use {years: 1, months:-1})
        Returns:
            DateTime : shifted date
        """
        return DateTime(self._value.shift(**shifting_amount))


class _DateTimeTypePydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        def validate_from_in(value: DateTimeIn | DateTime) -> DateTime:
            if isinstance(value, DateTime):
                return value
            result = DateTime(value)
            return result

        from_in_schema = core_schema.no_info_plain_validator_function(validate_from_in)

        return core_schema.json_or_python_schema(
            json_schema=from_in_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    from_in_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.to_mysql_datetime()
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(
            core_schema.union_schema(
                [
                    core_schema.str_schema(),
                    core_schema.date_schema(),
                    core_schema.datetime_schema(),
                    core_schema.int_schema(),
                ]
            )
        )


DateTimeType = Annotated[DateTime, _DateTimeTypePydanticAnnotation]


class Date(DateTime):
    _parse_error = _("date invalid (YYYY-MM-DD)")

    def __init__(self, datetime: DateTimeIn):
        super().__init__(datetime)
        self._value = arrow.get(self._value.date())

    def __copy__(self):
        return Date(self._value)

    def __repr__(self):
        return self._value.format("YYYY-MM-DD")  # pragma: no cover

    def shift(self, shifting_amount: dict) -> "Date":
        return Date(self._value.shift(**shifting_amount))


class _DateTypePydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        def validate_from_in(value: DateTimeIn | Date) -> Date:
            if isinstance(value, Date):
                return value
            result = Date(value)
            return result

        from_in_schema = core_schema.no_info_plain_validator_function(validate_from_in)

        return core_schema.json_or_python_schema(
            json_schema=from_in_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    from_in_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.to_mysql_date()
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(
            core_schema.union_schema(
                [
                    core_schema.str_schema(),
                    core_schema.date_schema(),
                    core_schema.datetime_schema(),
                    core_schema.int_schema(),
                ]
            )
        )


DateType = Annotated[Date, _DateTypePydanticAnnotation]
