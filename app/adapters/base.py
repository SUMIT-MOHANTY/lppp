from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)

class BaseAdapter(ABC):
    def __init__(self, name: str, base_url: str, auth_type: str = 'none', 
                 timeout: int = 30, retry_count: int = 3):
        self.name = name
        self.base_url = base_url
        self.auth_type = auth_type
        self.timeout = timeout
        self.retry_count = retry_count
        self.enabled = False
        self.api_key: Optional[str] = None
        self.bearer_token: Optional[str] = None
    
    @abstractmethod
    async def execute(self, method: str, endpoint: str, params: Dict, body: Any) -> Dict:
        pass
    
    async def _make_request(self, method: str, url: str, **kwargs) -> Dict:
        headers = kwargs.pop('headers', {})
        
        if self.auth_type == 'api_key' and self.api_key:
            headers['X-API-Key'] = self.api_key
        elif self.auth_type == 'bearer_token' and self.bearer_token:
            headers['Authorization'] = f'Bearer {self.bearer_token}'
        
        for attempt in range(self.retry_count):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(method, url, headers=headers, **kwargs)
                    return {
                        'status': response.status_code,
                        'data': response.json() if response.text else {},
                        'headers': dict(response.headers)
                    }
            except httpx.TimeoutException:
                logger.warning(f'Timeout on attempt {attempt + 1} for {url}')
                if attempt == self.retry_count - 1:
                    raise
            except httpx.HTTPError as e:
                logger.error(f'HTTP error: {str(e)}')
                raise
            
            await asyncio.sleep(2 ** attempt)
        
        return {'status': 500, 'data': {'error': 'Max retries exceeded'}}
    
    def transform_request(self, data: Dict) -> Dict:
        return data
    
    def transform_response(self, data: Dict) -> Dict:
        return data
