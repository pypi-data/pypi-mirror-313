from typing import Any

import pandas as pd
import pyarrow as pa

from .base_handler import BaseHandler
from pricecypher.enums import AccessTokenGrantType


class ReadParquetHandler(BaseHandler):
    """The abstract ReadParquetHandler class provides a base to read a parquet file into a pandas DataFrame.
    Extend this class and override the `process()` method when you want to receive a pyarrow Table to convert to a
    DataFrame.
    The input parquet file should be available at the `path_in` location. The output DataFrame will be
    stored as a pickle at the `path_out` location.
    """

    def get_allowed_access_token_grant_types(self) -> set[AccessTokenGrantType]:
        return set()

    def get_config_dependencies(self) -> dict[str, list[str]]:
        return dict()

    def handle(self, user_input: dict[str, Any]) -> any:
        """Handle the given `user_input`.
        Needs a parquet file stored at the `path_in` location. The output pandas DataFrame will be stored as a pickle at
        the `path_out` location.

        :param user_input: requires `path_in` and `path_out`.
        :return: the remote storage path.
        """
        input_table = self._file_storage.read_parquet(user_input.get('path_in'))
        output_df = self.process(input_table)
        return self._file_storage.write_df(user_input.get('path_out'), output_df)

    def process(self, table: pa.Table) -> pd.DataFrame:
        """Transform the pyarrow table into a pandas DataFrame.
        The Table is read from the input parquet file stored at the `path_in` location passed in the `handle()` method.

        :param table: the input pyarrow Table.
        :return: the resulting DataFrame.
        """
        return table.to_pandas()
