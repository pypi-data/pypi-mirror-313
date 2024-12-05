import json
import logging
from typing import Optional, Any

from .collections import Collection
from .encoders import PriceCypherJsonEncoder
from .endpoints import ScriptsEndpoint
from .enums import ScriptType
from .models import Script, ScriptExecution
from .rest import RestClient
from .storage import FileStorage


class ScriptService(object):
    """
    Script execution (output storage) API.
    Exposes the available operations to interact with scripts and the (outputs of) their execution using the PriceCypher
    Script Service.

    :param str bearer_token: Bearer token for PriceCypher (logical) API. The following scopes are relevant.
        - 'read:scripts': Required for all interactions with the PriceCypher Script Service.
        - 'read:scripts:output': Required for reading the output body of a script that is done executing.
        - 'execute:scripts': Required for registering (part of storing) script execution outputs.
    :param int dataset_id: Dataset that is queried by these scripts operations.
    :param str scripts_base: (optional) Base URL of PriceCypher Script Service API.
        (defaults to the static `default_scripts_base`, which in turn defaults to https://scripts.pricecypher.com)
    :param RestClientOptions rest_options: (optional) Set any additional options for the REST client, e.g. rate-limit.
        (defaults to None)
    """

    """ Default script service base URL """
    default_scripts_base = 'https://scripts.pricecypher.com'

    _file_storage: FileStorage

    def __init__(self, bearer_token, dataset_id, file_storage, scripts_base=None, rest_options=None):
        self._bearer = bearer_token
        self._dataset_id = dataset_id
        self._file_storage = file_storage
        self._scripts_base = scripts_base if scripts_base is not None else self.default_scripts_base
        self._rest_options = rest_options
        self._client = RestClient(jwt=bearer_token, options=rest_options)
        self._cache = dict()

    def get_available_scripts(self, **kwargs) -> Collection[Script]:
        """
        List all available scripts for the dataset.

        :return: collection of Script objects.
        """
        scripts = ScriptsEndpoint(self._client, self._dataset_id, self._scripts_base).index(**kwargs)

        return Collection[Script](scripts)

    def store_output(self, output: Any, **kwargs) -> int:
        """
        Store the given output remotely and register it as a new execution output of the given script.
        :param output: The (raw) output to store. It is serialized into a json string using `PriceCypherJsonEncoder`.
        :param kwargs: Must contain either a `script_id` or a `script_type`, specifying for which script the output
            should be stored.
        :key int script_id: ID of the script. Required iff no `script_type` provided.
        :key ScriptType script_type: Type of script to fetch the execution for. Required iff no `script_id` provided.
        :key str filename: Name of the (remote) file containing the output. Defaults to 'result.json'.
        :return: The ID of the newly registered script execution.
        """
        filename = kwargs.get('filename', 'result.json')

        with self._file_storage.save(filename, 'w') as file:
            json.dump(output, file, allow_nan=False, cls=PriceCypherJsonEncoder)

        output_path = self._file_storage.get_path_remote(filename, full=False)
        script_id = kwargs.get('script_id', self._find_script_id(kwargs.get('script_type')))

        response = ScriptsEndpoint(self._client, self._dataset_id, self._scripts_base) \
            .get(script_id) \
            .executions() \
            .store(output_path)

        return response.execution_id

    def get_latest_execution(self, **kwargs) -> Optional[ScriptExecution]:
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
        script_id = kwargs.get('script_id', self._find_script_id(kwargs.get('script_type')))

        execution = ScriptsEndpoint(self._client, self._dataset_id, self._scripts_base) \
            .get(script_id) \
            .executions() \
            .latest_output(**kwargs)

        return execution

    def _find_script_id(self, script_type: ScriptType) -> Optional[int]:
        """ Finds the ID of a script with the given type, or `None` if it cannot be found. """

        if script_type is None:
            raise ValueError("A script type must be provided.")

        if 'scripts_index' not in self._cache:
            self._cache['scripts_index'] = self.get_available_scripts()

        filtered_scripts = self._cache['scripts_index'].where('type', script_type)

        if len(filtered_scripts) == 0:
            logging.warning(f"No script with type '{script_type.value}' available for dataset {self._dataset_id}.")
            return None
        elif len(filtered_scripts) > 1:
            logging.warning(
                f"More than 1 script with type '{script_type.value}' available for dataset {self._dataset_id}."
                "This is probably caused by a fault in the PriceCypher SDK / event handler runtime."
            )

        script = filtered_scripts[0]
        return script.id
