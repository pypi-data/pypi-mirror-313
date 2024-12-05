from typing import Protocol, ClassVar, Dict, Any, runtime_checkable


@runtime_checkable
class DataclassProtocol(Protocol):
    """Checking for this attribute currently seems to be the most reliable way to ascertain that something is a
    dataclass. See: https://stackoverflow.com/a/55240861"""
    __dataclass_fields__: ClassVar[Dict[str, Any]]
