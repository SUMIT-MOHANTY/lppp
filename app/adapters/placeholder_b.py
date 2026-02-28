from app.adapters.base import BaseAdapter
from typing import Dict, Any

class PlaceholderApiBAdapter(BaseAdapter):
    def __init__(self):
        super().__init__('placeholder_api_b', 'https://api.placeholder-b.com', 'bearer_token')
    
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
