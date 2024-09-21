import toml
from typing import Dict, Any
_CONF = None

def load_config(path: str = 'config.toml') -> Dict[str, Any]:
    "Load the configuration dictionary from a TOML file"
    global _CONF
    _CONF = toml.load(path)
    return _CONF

def get_config():
    "Get the configuration dictionary"
    if not _CONF:
        return load_config()
    else:
        return _CONF
