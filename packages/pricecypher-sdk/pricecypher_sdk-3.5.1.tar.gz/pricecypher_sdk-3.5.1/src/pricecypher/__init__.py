import pbr.version

from .collections import ScopeCollection, ScopeValueCollection
from .config_sections import ConfigSections
from .datasets import Datasets
from .script_service import ScriptService
from .rest import RestClient

__all__ = ['ScopeCollection', 'ScopeValueCollection', 'ConfigSections', 'Datasets', 'RestClient', 'ScriptService']

__version__ = pbr.version.VersionInfo('pricecypher_sdk').version_string()
