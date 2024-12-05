from dataclasses import field
from typing import List, Optional, Any, Union

from marshmallow import EXCLUDE
from marshmallow_dataclass import dataclass

from .namespaced_schema import NamespacedSchema


@dataclass(base_schema=NamespacedSchema, frozen=True)
class ConfigSection:
    key: str = field(compare=True)
    name: str = field(compare=False)
    order: int = field(compare=False)

    class Meta:
        name = "section"
        plural_name = "sections"
        unknown = EXCLUDE


@dataclass(frozen=True)
class ConfigKey:
    key: str = field(compare=True)
    label: str = field(compare=False)
    data_type: str = field(compare=False)
    schema: Union[None, str] = field(compare=False)
    order: int = field(compare=False)
    is_array: bool = field(compare=False)
    business_cell_id: Union[str, int] = field(compare=False)
    value: Any = field(compare=False)
    possible_values: Optional[Any] = field(compare=False)

    class Meta:
        unknown = EXCLUDE


@dataclass(base_schema=NamespacedSchema, frozen=True)
class ConfigSectionWithKeys:
    id: int = field(compare=True)
    key: str = field(compare=False)
    name: str = field(compare=False)
    order: int = field(compare=False)
    keys: List[ConfigKey]

    class Meta:
        name = "section"
        plural_name = "sections"
        unknown = EXCLUDE
