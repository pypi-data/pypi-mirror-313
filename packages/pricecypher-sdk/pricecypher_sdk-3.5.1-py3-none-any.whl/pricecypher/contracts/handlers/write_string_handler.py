from abc import abstractmethod
from typing import Any

import pandas as pd

from .base_handler import BaseHandler
from pricecypher.enums import AccessTokenGrantType


class WriteStringHandler(BaseHandler):
    """The abstract WriteStringHandler class provides a base to write a pandas DataFrame to a string file.
    Extend this class and override the `process()` method when you want to do exactly that.
    The input DataFrame file should be available as a pickle at the `path_in` location. The output string file will be
    stored at the `path_out` location.
    """

    def get_allowed_access_token_grant_types(self) -> set[AccessTokenGrantType]:
        return set()

    def get_config_dependencies(self) -> dict[str, list[str]]:
        return dict()

    def handle(self, user_input: dict[str, Any]) -> any:
        """Handle the given `user_input`.
        Needs a DataFrame stored as a pickle at the `path_in` location. The output string will be stored at the
        `path_out` location.

        :param user_input: requires `path_in` and `path_out`.
        :return: the remote storage path.
        """
        input_df = self._file_storage.read_df(user_input.get('path_in'))
        output_string = self.process(input_df)
        return self._file_storage.write_string(user_input.get('path_out'), output_string)

    @abstractmethod
    def process(self, df: pd.DataFrame) -> str:
        """Override to implement and transform a pandas DataFrame into a string, which will be stored as a file at the
        `path_out` location passed in the `handle()` method.

        :param df: the input DataFrame.
        :return: the resulting string.
        """
        raise NotImplementedError
