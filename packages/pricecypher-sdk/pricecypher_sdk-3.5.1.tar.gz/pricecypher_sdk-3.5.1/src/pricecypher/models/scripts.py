from dataclasses import field
from typing import Optional, Any

from marshmallow import EXCLUDE
from marshmallow.fields import Enum
from marshmallow_dataclass import dataclass

from .namespaced_schema import NamespacedSchema
from ..enums import ScriptLang, ScriptType, ScriptEnvStatus


@dataclass(base_schema=NamespacedSchema, frozen=True)
class Script:
    id: int = field(compare=True)
    label: str = field(compare=False)
    scope_representation: Optional[str] = field(compare=False)
    lang: ScriptLang = field(metadata={'marshmallow_field': Enum(ScriptLang, by_value=True)})
    type: ScriptType = field(metadata={'marshmallow_field': Enum(ScriptType, by_value=True)})
    env_status: ScriptEnvStatus = field(metadata={'marshmallow_field': Enum(ScriptEnvStatus, by_value=True)})

    class Meta:
        name = "script"
        plural_name = "scripts"
        unknown = EXCLUDE


@dataclass(base_schema=NamespacedSchema, frozen=True)
class ScriptExecution:
    script_service_base: str
    script_id: int
    dataset_id: int
    execution_id: int
    script_output: Optional[Any]

    class Meta:
        name = "output"
        plural_name = "outputs"
        unknown = EXCLUDE


@dataclass(frozen=True)
class CreateScriptExecResponse:
    execution_id: int = field(compare=False)
