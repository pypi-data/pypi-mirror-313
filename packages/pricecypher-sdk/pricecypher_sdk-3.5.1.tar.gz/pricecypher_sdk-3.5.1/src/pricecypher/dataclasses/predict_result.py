from dataclasses import dataclass
from typing import Optional

from pricecypher.enums import Accuracy


@dataclass(frozen=True)
class PredictValues:
    predictive_price: float
    max_predictive_range: Optional[float] = None
    min_predictive_range: Optional[float] = None


@dataclass(frozen=True)
class PredictStep:
    key: str
    value: float
    order: Optional[int] = None


@dataclass(frozen=True)
class PredictResult:
    """
    Result after model inference, i.e. the model prediction result. It consists of the following properties.

    - `predictive_values`: The value and associated min-max range that form the of the underlying prediction.
    - `accuracy`: The accuracy of the underlying prediction.
    - `predictive_steps`: The different (pricing) steps building up the total underlying prediction.
    """
    predictive_values: PredictValues
    predictive_steps: list[PredictStep]
    accuracy: Accuracy
    version: Optional[str] = None
