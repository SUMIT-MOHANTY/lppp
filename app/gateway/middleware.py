from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time
import redis
import os
from typing import Optional

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
        except:
            self.redis_client = None
    
    async def dispatch(self, request: Request, call_next):
        client_id = request.headers.get('X-API-Key', request.client.host)
        
        if self.redis_client:
            key = f'rate_limit:{client_id}'
            current = self.redis_client.get(key)
            
            if current and int(current) >= self.requests_per_minute:
                raise HTTPException(status_code=429, detail='Rate limit exceeded')
            
            pipe = self.redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, 60)
            pipe.execute()
        
        response = await call_next(request)
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
