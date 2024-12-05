from typing import Optional

from pricecypher.exceptions import HttpException
from pricecypher.models import Script, ScriptExecution, CreateScriptExecResponse
from .base_endpoint import BaseEndpoint


class ScriptsEndpoint(BaseEndpoint):
    """
    PriceCypher script service endpoints.

    :param RestClient client: HTTP client for making API requests.
    :param int dataset_id: Dataset ID.
    :param str scripts_base: (optional) Base URL of PriceCypher script service API.
        (defaults to https://scripts.pricecypher.com)
    """

    def __init__(self, client, dataset_id, scripts_base='https://scripts.pricecypher.com'):
        self.base_url = scripts_base
        self.client = client
        self.dataset_id = dataset_id
        self.param_keys = ['environment']

        self.base_url = self._url(['api/datasets', self.dataset_id, '/scripts'])

    def index(self, **kwargs) -> Optional[list[Script]]:
        """
        List all available scripts for the dataset.

        :return: list of scripts.
        :key environment: (Optional) environment of the underlying data intake to query. Defaults to latest intake.
        """
        params = self._find_request_params(
            keys={'include_dependencies', 'type', 'env_status'},
            include_dependencies='false',
            **kwargs
        )
        return self.client.get(self._url(), params=params, schema=Script.Schema(many=True))

    def get(self, script_id) -> '_ScriptEndpoint':
        """Script endpoints for single script in script service API."""
        return _ScriptEndpoint(self.client, self._url([script_id]))


class _ScriptEndpoint(BaseEndpoint):
    """PriceCypher script endpoints in script service API."""

    def __init__(self, client, base):
        self.client = client
        self.base_url = base

    def executions(self) -> '_ScriptExecutionsEndpoint':
        return _ScriptExecutionsEndpoint(self.client, self._url(['executions']))


class _ScriptExecutionsEndpoint(BaseEndpoint):
    def __init__(self, client, base):
        self.client = client
        self.base_url = base
        self.param_keys = {'environment'}

    def store(self, output_path: str) -> Optional[CreateScriptExecResponse]:
        """
        Stores a new execution of a script in Script Service API. I.e., "registers" the given output path to be
        "pointing" to the file that stores the output of the script execution.

        :param output_path: The (relative) path to the remote file that stores the output of the script execution.
        """
        body = {
            'execute': False,
            'location': output_path,
        }
        return self.client.post(self._url(), data=body, schema=CreateScriptExecResponse.Schema())

    def latest_output(self, **kwargs) -> Optional[ScriptExecution]:
        """
        Get the latest execution of a given script (type) for the dataset. If a completed execution exists, it contains
        the output of the execution of the script as well.

        :param kwargs: Must contain either a `script_id` or a `script_type`, specifying for which script the latest
            execution should be fetched.
        :key int script_id: ID of the script. Required iff no `script_type` provided.
        :key ScriptType script_type: Type of script to fetch the execution for. Required iff no `script_id` provided.
        :key str environment: (Optional) environment of the underlying data intake to query. Defaults to latest.
        :return: `ScriptExecution` instance or `None` if there are no completed executions of the requested script.
        """
        url = self._url(['latest/output'])
        params = self._find_request_params(**kwargs)
        try:
            return self.client.get(url, params=params, schema=ScriptExecution.Schema(many=False))
        except HttpException as err:
            if err.status_code == 404:
                return None
            raise err
