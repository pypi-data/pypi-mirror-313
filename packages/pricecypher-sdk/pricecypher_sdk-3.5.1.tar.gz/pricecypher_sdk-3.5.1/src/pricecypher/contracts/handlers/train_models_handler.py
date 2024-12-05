from abc import abstractmethod
from typing import Any

import mlflow.pyfunc
import pandas as pd

from .base_handler import BaseHandler
from pricecypher.enums import AccessTokenGrantType
from ..pricecypher_model import PricecypherModel


class TrainModelHandler(BaseHandler):
    """The abstract TrainModelHandler class provides a base for storing one or more models trained on a pandas
    DataFrame.
    Extend this class and override the `process()` method when you want to receive a DataFrame and train one or more
    models on it.
    The input DataFrame should be available as a pickle at the `path_in` location.
    The output dict will be stored as a pickle at the `path_models_out` location.
    For consistency the (unaltered) input DataFrame is stored at the `path_out` location as well.
    """

    def get_allowed_access_token_grant_types(self) -> set[AccessTokenGrantType]:
        return set()

    def get_config_dependencies(self) -> dict[str, list[str]]:
        return dict()

    def handle(self, user_input: dict[str, Any]) -> any:
        """Handle the given `user_input`.
        Needs a pandas DataFrame stored as a pickle at the `path_in` location. The trained model will be stored at the
        `path_model_out` location by mlflow. For consistency the (unaltered) input DataFrame is stored at `path_out`
        as well.

        :param user_input: requires `path_in`, `path_out` and `path_model_out`.
        :return: the remote storage path of the DataFrame.
        """
        input_df = self._file_storage.read_df(user_input.get('path_in'))
        model = self.train(input_df)

        mlflow.pyfunc.save_model(user_input.get('path_model_out'), python_model=model)
        return self._file_storage.write_df(user_input.get('path_out'), input_df)

    @abstractmethod
    def train(self, df: pd.DataFrame) -> PricecypherModel:
        """Override to implement and train a model (wrapper) on the given input DataFrame.

        :param df: the input DataFrame.
        :return: the trained model instance.
        """
        raise NotImplementedError
