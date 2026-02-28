from app.adapters.base import BaseAdapter
from typing import Dict, Any

class PlaceholderApiAAdapter(BaseAdapter):
    def __init__(self):
        super().__init__('placeholder_api_a', 'https://api.placeholder-a.com', 'api_key')
    
    async def execute(self, method: str, endpoint: str, params: Dict, body: Any) -> Dict:
        url = f'{self.base_url}/{endpoint}'
        
        # Mock response for development
        return {
            'status': 200,
            'data': {
                'adapter': self.name,
                'endpoint': endpoint,
                'method': method,
                'message': 'Mock response - API credentials not configured',
                'mock_data': True
            }
        }
