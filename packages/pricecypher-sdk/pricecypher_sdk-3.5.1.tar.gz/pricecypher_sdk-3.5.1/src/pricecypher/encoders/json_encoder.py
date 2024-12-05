import dataclasses
from json import JSONEncoder

import numpy as np

from pricecypher.dataclasses import DataclassProtocol

type _Primitives = None | dict | list | str | int | float | bool | set
type JsonSerializable = _Primitives | DataclassProtocol | np.integer | np.floating | np.ndarray


class PriceCypherJsonEncoder(JSONEncoder):
    """JSON encoder that can properly serialize dataclasses and numpy numbers."""

    def default(self, obj: JsonSerializable):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, DataclassProtocol):
            return dataclasses.asdict(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()

        return super().default(obj)
