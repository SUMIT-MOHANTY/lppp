import redis
import os
from typing import Dict, Any

async def check_health() -> Dict[str, Any]:
    health = {
        'status': 'healthy',
        'timestamp': None,
        'components': {}
    }
    
    # Check Redis
    try:
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        r = redis.from_url(redis_url, socket_timeout=2)
        r.ping()
        health['components']['redis'] = 'healthy'
    except Exception as e:
        health['components']['redis'] = f'unhealthy: {str(e)}'
        health['status'] = 'degraded'
    
    # Check adapters
    from app.adapters import get_adapter
    adapter_names = ['placeholder_api_a', 'placeholder_api_b']
    health['components']['adapters'] = {}
    
    for name in adapter_names:
        adapter = get_adapter(name)
        if adapter:
            health['components']['adapters'][name] = 'available' if adapter.enabled else 'disabled'
    
    return health
