from pricecypher.models import Scope, ScopeValue, TransactionSummary, TransactionsPage
from pricecypher.rest import RestClient
from .base_endpoint import BaseEndpoint


class DatasetsEndpoint(BaseEndpoint):
    """PriceCypher dataset endpoints in dataset service.

    :param str bearer_token: Bearer token for PriceCypher (logical) API. Needs 'read:datasets' scope.
    :param int dataset_id: Dataset ID.
    :param str dss_base: (optional) Base URL for PriceCypher dataset service API.
        (defaults to https://datasets.pricecypher.com)
    :param RestClientOptions rest_options: (optional) Set any additional options for the REST client, e.g. rate-limit.
        (defaults to None)
    """

    def __init__(self, bearer_token, dataset_id, dss_base='https://datasets.pricecypher.com', rest_options=None):
        self.bearer_token = bearer_token
        self.dataset_id = dataset_id
        self.base_url = dss_base
        self.client = RestClient(jwt=bearer_token, options=rest_options)
        self.param_keys = {'intake_status', 'environment'}

    def business_cell(self, bc_id='all'):
        """
        Business cell-specific endpoints within dataset service.
        :param str bc_id: (optional) Business cell ID.
            (defaults to 'all')
        :return: Business cell endpoint
        :rtype: _BusinessCellEndpoint
        """
        url = self._url(['api/datasets', self.dataset_id, 'business_cells', bc_id])
        return _BusinessCellEndpoint(self.client, url)


class _BusinessCellEndpoint(BaseEndpoint):
    """
    Business cell specific endpoints in dataset service.
    """
    def __init__(self, client, base):
        self.client = client
        self.base_url = base

    def scopes(self):
        """
        Scope endpoints in dataset service.
        :rtype: _ScopesEndpoint
        """
        return _ScopesEndpoint(self.client, self._url('scopes'))

    def transactions(self):
        """
        Transaction endpoints in dataset service.
        :rtype: _TransactionsEndpoint
        """
        return _TransactionsEndpoint(self.client, self._url('transactions'))


class _ScopesEndpoint(BaseEndpoint):
    """
    Scope endpoints in dataset service.
    """
    def __init__(self, client, base):
        self.client = client
        self.base_url = base

    def index(self, **kwargs):
        """
        Show a list of all scopes of the dataset.
        :key intake_status: (Optional) intake status to fetch the scopes for.
        :key environment: (Optional) environment of the underlying data intake to query. Defaults to latest intake.
        :rtype: list[Scope]
        """
        return self.client.get(self._url(), params=self._find_request_params(**kwargs), schema=Scope.Schema(many=True))

    def scope_values(self, scope_id, **kwargs):
        """
        Get all scope values for the given scope of the dataset.
        :param scope_id: Scope to get scope values for.
        :key intake_status: (Optional) intake status to fetch the scope values for.
        :key environment: (Optional) environment of the underlying data intake to query. Defaults to latest intake.
        :rtype: list[ScopeValue]
        """
        url = self._url([scope_id, 'scope_values'])
        return self.client.get(url, params=self._find_request_params(**kwargs), schema=ScopeValue.Schema(many=True))


class _TransactionsEndpoint(BaseEndpoint):
    """
    Transaction endpoints in dataset service.
    """
    def __init__(self, client, base):
        self.client = client
        self.base_url = base

    def index(self, data):
        """
        Display a listing of transactions. The given data will be passed directly to the dataset service.
        :param data: See documentation of dataset service on what data can be passed.
        :rtype: list[Transaction]
        """
        # Perform initial request to retrieve first page of transactions and page metadata.
        init_response = self.client.post(self._url(), data=data, schema=TransactionsPage.Schema())
        # Collect first page of transactions, which will be appended later when multiple pages are available.
        transactions = init_response.transactions
        curr_page = init_response.meta.current_page
        last_page = init_response.meta.last_page
        request_path = init_response.meta.path

        # Loop over all available pages.
        for page_nr in range(curr_page + 1, last_page + 1):
            page_path = f'{request_path}?page={page_nr}'
            page_response = self.client.post(page_path, data=data, schema=TransactionsPage.Schema())
            # Append transactions of the current page.
            transactions += page_response.transactions

        return transactions

    def summary(self, **kwargs):
        """
        Get a summary of the transactions. Contains the first and last date of any transaction in the dataset.
        :key intake_status: (Optional) intake status to fetch the summary for.
        :key environment: (Optional) environment of the underlying data intake to query. Defaults to latest intake.
        :rtype: TransactionSummary
        """
        url = self._url('summary')
        return self.client.get(url, params=self._find_request_params(**kwargs), schema=TransactionSummary.Schema())
