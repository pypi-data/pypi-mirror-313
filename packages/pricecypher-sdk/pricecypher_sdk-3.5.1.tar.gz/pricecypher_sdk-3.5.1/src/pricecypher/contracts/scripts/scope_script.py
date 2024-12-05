from abc import ABC, abstractmethod
from typing import Any, Optional, Callable

from pricecypher.enums import AccessTokenGrantType
from .script import Script


class ScopeScript(Script, ABC):
    """
    The abstract ScopeScript class serves as an interaction contract such that by extending it with its
        methods implemented, a script can be created that calculates values for some scope for transactions,
        which can then be used in a generalized yet controlled setting.
    """

    def get_allowed_access_token_grant_types(self) -> set[AccessTokenGrantType]:
        return {AccessTokenGrantType.CLIENT_CREDENTIALS}

    def execute(
            self,
            business_cell_id: Optional[int],
            get_bearer_token: Callable[[], str],
            user_input: dict[Any: Any],
    ) -> Any:
        # Executing a scope-script like a normal script:
        # Attempt to extract the transaction IDs and continue as normal
        if 'transaction_ids' not in user_input:
            raise Exception('Expected input key "transaction_ids" not present.')
        transaction_ids: list[int] = user_input['transaction_ids']
        return self.execute_scope_script(business_cell_id, get_bearer_token, transaction_ids)

    @abstractmethod
    def execute_scope_script(
            self,
            business_cell_id: Optional[int],
            get_bearer_token: Callable[[], str],
            transaction_ids: list[int],
    ) -> dict[int, str]:
        """
        Execute the script to calculate the values of some scope for the given transactions.

        :param business_cell_id: Business cell to execute the script for, or None if running the script for all.
        :param get_bearer_token: Function that can be invoked to retrieve an access token.
        :param transaction_ids: List of transaction IDs to calculate the scope values/constants for.
        :return: Dictionary mapping every transaction ID to a string value for the scope of this script.
        """
        raise NotImplementedError
