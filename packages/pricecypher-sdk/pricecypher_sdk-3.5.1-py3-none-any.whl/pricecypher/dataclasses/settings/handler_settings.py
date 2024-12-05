import os
from dataclasses import dataclass
from typing import Optional

from .remote_storage_settings import RemoteStorageSettings


@dataclass(kw_only=True)
class HandlerSettings:
    """Context / environment-specific event handler settings."""
    base_users: str = None
    base_config: str = None
    base_scripts: str = None
    path_local_out: Optional[str] = None
    path_remote_out_base: Optional[str] = None
    path_remote_out_prefix: Optional[str] = None
    remote_storage_settings: Optional[RemoteStorageSettings] = None

    def __post_init__(self):
        self.base_users = self.base_users or os.environ.get('BASE_USERS', 'https://users.pricecypher.com')
        self.base_config = self.base_config or os.environ.get('BASE_CONFIG', 'https://config.pricecypher.com')
        self.base_scripts = self.base_scripts or os.environ.get('BASE_SCRIPTS', 'https://scripts.pricecypher.com')
        self.remote_storage_settings = self.remote_storage_settings or RemoteStorageSettings()

    def __getitem__(self, key):
        return super().__getattribute__(key)
