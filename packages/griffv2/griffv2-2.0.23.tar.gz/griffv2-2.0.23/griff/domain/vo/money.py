from decimal import Decimal
from typing import Any

from pydantic import model_validator

from griff.domain.common_types import ValueObject


class Money(ValueObject):
    amount: Decimal
    currency: str = "EUR"

    @model_validator(mode="before")
    @classmethod
    def check_card_number_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict) is False:
            data = {"amount": str(data)}
        return data

    def __str__(self):  # pragma: no cover
        return f"{self.amount}{self.currency}"

    def __ge__(self, other):
        self._check_currency_match(other)
        return self.amount >= other.amount

    def __le__(self, other):
        self._check_currency_match(other)
        return self.amount <= other.amount

    def __gt__(self, other):
        self._check_currency_match(other)
        return self.amount > other.amount

    def __lt__(self, other):
        self._check_currency_match(other)
        return self.amount < other.amount

    def _check_currency_match(self, other):
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
