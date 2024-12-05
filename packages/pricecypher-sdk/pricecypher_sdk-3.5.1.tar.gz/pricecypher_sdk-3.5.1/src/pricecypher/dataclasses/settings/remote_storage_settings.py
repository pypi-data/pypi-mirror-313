from dataclasses import dataclass
from typing import Optional

from .azure_blob_settings import AzureBlobSettings


@dataclass(kw_only=True)
class RemoteStorageSettings:
    azure: Optional[AzureBlobSettings] = None

    def __post_init__(self):
        self.azure = self.azure or AzureBlobSettings()

    def __getitem__(self, key):
        if not hasattr(self, key):
            return None

        return super().__getattribute__(key)
