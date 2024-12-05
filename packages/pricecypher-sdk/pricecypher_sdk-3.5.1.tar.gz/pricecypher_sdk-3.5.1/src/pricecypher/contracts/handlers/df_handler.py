from abc import abstractmethod
from typing import Any

import pandas as pd

from .base_handler import BaseHandler
from pricecypher.enums import AccessTokenGrantType


class DataFrameHandler(BaseHandler):
    """The abstract DataFrameHandler class provides a base for mutating a pandas DataFrame.
    Extend this class and override the `process()` method when you want to run a data science script on the DataFrame
    and add the results to it (as extra columns).
    The input DataFrame should be available as a pickle at the `path_in` location. The output DataFrame will be stored
    as a pickle at the `path_out` location.
    """

    def get_allowed_access_token_grant_types(self) -> set[AccessTokenGrantType]:
        return set()

    def get_config_dependencies(self) -> dict[str, list[str]]:
        return dict()

    def handle(self, user_input: dict[str, Any]) -> any:
        """Handle the given `user_input`.
        Needs a pandas DataFrame stored as a pickle at the `path_in` location. The output pandas DataFrame will be
        stored as a pickle at the `path_out` location.

        :param user_input: requires `path_in` and `path_out`.
        :return: the remote storage path.
        :raise RuntimeError: when the number of rows of the output is not equal to the input.
        """
        input_df = self._file_storage.read_df(user_input.get('path_in'))
        num_rows_input = input_df.shape[0]
        output_df = self.process(input_df)
        self._guard_num_rows(output_df, num_rows_input)
        return self._file_storage.write_df(user_input.get('path_out'), output_df)

    @abstractmethod
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Override to implement and run a data science (or other) script on the input DataFrame.
        Add the results of the script as one or more extra columns.
        The output DataFrame should have the same number of rows as the input DataFrame, unless explicitly overruled by
        overriding the `_guard_num_rows()` function.

        :param df: the input DataFrame.
        :return: the resulting DataFrame.
        """
        raise NotImplementedError
