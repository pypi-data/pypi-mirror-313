from dataclasses import field
from datetime import datetime
from typing import Optional, List, Union

from marshmallow import EXCLUDE
from marshmallow_dataclass import dataclass

from .namespaced_schema import NamespacedSchema


@dataclass(base_schema=NamespacedSchema, frozen=True)
class Scope:
    id: int = field(compare=True)
    data_version_id: int = field(compare=False)
    order: Optional[int] = field(compare=False)
    type: str = field(compare=False)
    representation: Optional[str] = field(compare=False)
    name_dataset: str = field(compare=False)
    name_human: Optional[str] = field(compare=False)
    name_human_times_volume: Optional[str] = field(compare=False)
    multiply_by_volume_enabled: bool = field(compare=False)
    default_aggregation_method: Optional[str] = field(compare=False)

    class Meta:
        name = "scope"
        plural_name = "scopes"
        unknown = EXCLUDE


@dataclass(base_schema=NamespacedSchema, frozen=True)
class ScopeValue:
    id: str = field(compare=True)
    scope_id: int = field(compare=False)
    value: str = field(compare=False)

    class Meta:
        name = "scope_value"
        plural_name = "scope_values"
        unknown = EXCLUDE


@dataclass(base_schema=NamespacedSchema, frozen=True)
class TransactionSummary:
    first_date_time: datetime = field(metadata=dict(data_key='first_date'))
    last_date_time: datetime = field(metadata=dict(data_key='last_date'))

    class Meta:
        name = "summary"
        plural_name = "summaries"
        unknown = EXCLUDE


@dataclass(frozen=True)
class ScopeValueTransaction:
    scope_id: int
    value: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass(frozen=True)
class ScopeConstantTransaction:
    scope_id: int
    constant: Union[str, float, None]
    volume_multiplied_constant: Optional[Union[str, float, None]]

    class Meta:
        unknown = EXCLUDE


@dataclass(frozen=True)
class Transaction:
    id: Optional[int]
    external_id: Optional[str]
    count: Optional[int]
    volume: float
    price: float
    date_time: datetime
    currency: Optional[str]
    currencies: Optional[List[str]]
    unit: Optional[str]
    units: Optional[List[str]]
    scope_values: List[ScopeValueTransaction]
    scope_constants: List[ScopeConstantTransaction]

    class Meta:
        unknown = EXCLUDE

    def to_dict(self, scope_keys):
        dic = {
            'id': self.id,
            'external_id': self.external_id,
            'count': self.count,
            'volume': self.volume,
            'price': self.price,
            'date_time': self.date_time,
            'currency': self.currency,
            'currencies': self.currencies,
            'unit': self.unit,
            'units': self.units,
        }

        for scope_value in self.scope_values:
            if scope_value.scope_id in scope_keys:
                scope_key = scope_keys[scope_value.scope_id]
                dic[scope_key] = scope_value.value

        for scope_constant in self.scope_constants:
            if scope_constant.scope_id in scope_keys:
                scope_key = scope_keys[scope_constant.scope_id]
                dic[scope_key] = scope_constant.constant

        return dic


@dataclass(frozen=True)
class PageMeta:
    current_page: int
    last_page: int
    path: str

    class Meta:
        # Exclude other fields since we don't need them.
        unknown = EXCLUDE


@dataclass(frozen=True)
class TransactionsPage:
    meta: PageMeta
    transactions: List[Transaction]

    class Meta:
        # Exclude other fields since we don't need them.
        unknown = EXCLUDE
