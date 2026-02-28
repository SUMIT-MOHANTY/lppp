from typing import List, Dict, Any
import yaml
import os

_config = None

def load_config() -> Dict:
    global _config
    if _config is None:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
        with open(config_path, 'r') as f:
            _config = yaml.safe_load(f)
    return _config

def get_all_adapters() -> List[Dict[str, Any]]:
    config = load_config()
    adapters = config.get('adapters', {})
    return [
        {
            'name': name,
            'enabled': data.get('enabled', False),
            'base_url': data.get('base_url'),
            'auth_type': data.get('auth_type')
        }
        for name, data in adapters.items()
    ]

def get_adapter_config(name: str) -> Dict[str, Any]:
    config = load_config()
    return config.get('adapters', {}).get(name, {})
