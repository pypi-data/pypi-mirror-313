from typing import Any

import mlflow
from mlflow.pyfunc import PyFuncModel
import pandas as pd

from .base_handler import BaseHandler
from pricecypher.enums import AccessTokenGrantType


class BatchInferenceHandler(BaseHandler):
    """The abstract BatchInferenceHandler class provides a base for processing the inference (i.e. scoring) of a
    machine learning model on a DataFrame containing a whole batch of inputs (as opposed to real-time model inference).

    The input PricecypherModel should be available as a pickle at the 'path_models_in' location.
    The input DataFrame should be available as a pickle at the `path_in` location.
    The output DataFrame will be stored as a pickle at the `path_out` location.
    """
    _model: PyFuncModel

    def get_allowed_access_token_grant_types(self) -> set[AccessTokenGrantType]:
        return set()

    def get_config_dependencies(self) -> dict[str, list[str]]:
        return dict()

    def handle(self, user_input: dict[str, Any]) -> any:
        """Handle the given `user_input`.
        Needs a model tracked by mlflow, referenced by `model_uri_in`, and a pandas DataFrame pickle at `path_in`.
        The output pandas DataFrame will be stored as a pickle at the `path_out` location.

        :param user_input: requires `path_in`, `model_uri_in`, and `path_out`.
        :return: the remote storage path.
        :raise RuntimeError: when the number of rows of the output is not equal to the input.
        """
        input_df = self._file_storage.read_df(user_input.get('path_in'))
        self._model = mlflow.pyfunc.load_model(user_input.get('model_uri_in'))
        num_rows_input = input_df.shape[0]
        output_df = self.process(input_df)
        self._guard_num_rows(output_df, num_rows_input)
        return self._file_storage.write_df(user_input.get('path_out'), output_df)

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._model.predict(df)
