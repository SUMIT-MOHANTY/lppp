import httpx
from typing import Dict, Any, Optional
import json

class ApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _headers(self) -> Dict[str, str]:
        return {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    async def request(self, method: str, adapter: str, endpoint: str, 
                     params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict:
        url = f'{self.base_url}/api/v1/{adapter}/{endpoint}'
        
        response = await self.client.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=self._headers()
        )
        
        return {
            'status': response.status_code,
            'data': response.json() if response.text else {}
        }
    
    async def get(self, adapter: str, endpoint: str, params: Optional[Dict] = None):
        return await self.request('GET', adapter, endpoint, params)
    
    async def post(self, adapter: str, endpoint: str, data: Dict):
        return await self.request('POST', adapter, endpoint, data=data)
    
    async def put(self, adapter: str, endpoint: str, data: Dict):
        return await self.request('PUT', adapter, endpoint, data=data)
    
    async def delete(self, adapter: str, endpoint: str):
        return await self.request('DELETE', adapter, endpoint)
    
    async def health_check(self) -> Dict[str, Any]:
        response = await self.client.get(f'{self.base_url}/api/v1/health')
        return response.json()
    
    async def list_adapters(self) -> Dict[str, Any]:
        response = await self.client.get(f'{self.base_url}/api/v1/adapters')
        return response.json()
    
    async def close(self):
        await self.client.aclose()
