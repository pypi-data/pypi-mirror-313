import os
from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class AzureBlobSettings:
    account_url: Optional[str] = None

    def __post_init__(self):
        self.account_url = self.account_url or os.environ.get('AZURE_BLOB_ACCOUNT_URL', None)

    def __getitem__(self, key):
        return super().__getattribute__(key)
