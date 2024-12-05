from abc import ABCMeta

from mlflow.pyfunc import PythonModel


class PricecypherModel(PythonModel, metaclass=ABCMeta):
    """The top-level, abstract PricecypherModel class serves as an interaction contract that specifies the most
    generic form of any PriceCypher model.

    We define our own (abstract) class for this to avoid any hard dependencies to specific libraries, as well as to
    define a common interface for all models that are built on the PriceCypher platform.

    NB: This class does not necessarily have to extend mlflow PythonModel. Mainly, it needs a `predict` function.
    Please replace the base class with something else if needed. This was the best base class I could find up to now.
    """
    # Intentionally empty for now. Change as needed if the PythonModel base class does not suffice.
