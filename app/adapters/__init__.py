from app.adapters.base import BaseAdapter
from app.adapters.placeholder_a import PlaceholderApiAAdapter
from app.adapters.placeholder_b import PlaceholderApiBAdapter

ADAPTERS = {}

def register_adapter(name: str, adapter: BaseAdapter):
    ADAPTERS[name] = adapter

def get_adapter(name: str):
    return ADAPTERS.get(name)

def init_adapters():
    adapter_a = PlaceholderApiAAdapter()
    adapter_b = PlaceholderApiBAdapter()
    
    register_adapter('placeholder_api_a', adapter_a)
    register_adapter('placeholder_api_b', adapter_b)
    
    return ADAPTERS

__all__ = ['BaseAdapter', 'get_adapter', 'init_adapters']
