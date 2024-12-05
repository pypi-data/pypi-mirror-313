from abc import ABC, abstractmethod
from typing import Optional, Any, Callable

from pricecypher.dataclasses import TestSuite
from pricecypher.enums import AccessTokenGrantType
from .script import Script


class QualityTestScript(Script, ABC):
    """
    The abstract QualityTestScript class serves as an interaction contract such that by extending it with its
        methods implemented, a script can be created that performs data quality tests on a dataset, which can then be
        used in a generalized yet controlled setting.
    """

    def get_allowed_access_token_grant_types(self) -> set[AccessTokenGrantType]:
        return {AccessTokenGrantType.CLIENT_CREDENTIALS}

    def execute(self, business_cell_id: Optional[int], get_bearer_token: Callable[[], str],
                user_input: dict[Any: Any]) -> Any:
        return self.execute_tests(business_cell_id, get_bearer_token)

    @abstractmethod
    def execute_tests(self, business_cell_id: Optional[int], get_bearer_token: Callable[[], str]) -> TestSuite:
        """
        Execute the script to calculate the values of some scope for the given transactions.

        :param business_cell_id: Business cell to execute the script for, or None if running the script for all.
        :param get_bearer_token: Function that can be invoked to retrieve an access token.
        :return: List of all test results that were performed by the test script.
        """
        raise NotImplementedError
