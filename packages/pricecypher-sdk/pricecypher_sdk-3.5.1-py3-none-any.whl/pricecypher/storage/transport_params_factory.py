from typing import Optional

from pricecypher.dataclasses import AzureBlobSettings
from pricecypher.dataclasses.settings.remote_storage_settings import RemoteStorageSettings


def create_transport_params(settings: RemoteStorageSettings, scheme: Optional[str]) -> dict:
    if scheme is None:
        return {}

    scheme_settings = settings[scheme]

    if scheme_settings is None:
        return {}

    if scheme == 'azure':
        return _transport_params_azure(scheme_settings)

    return {}


def _transport_params_azure(settings: AzureBlobSettings) -> dict:
    if settings.account_url is None:
        raise Exception('Azure Blob account URL must be set when using azure remote base.')

    from azure.identity import DefaultAzureCredential
    from azure.storage.blob import BlobServiceClient

    client = BlobServiceClient(account_url=settings.account_url, credential=DefaultAzureCredential())

    return {'client': client}
