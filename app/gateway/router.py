from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import time
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.api_route('/{adapter_name}/{endpoint:path}', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
async def route_request(adapter_name: str, endpoint: str, request: Request):
    start_time = time.time()
    
    try:
        body = await request.body()
        query_params = dict(request.query_params)
        headers = dict(request.headers)
        
        # Authenticate request
        api_key = headers.get('X-API-Key')
        if not api_key:
            raise HTTPException(status_code=401, detail='Missing API key')
        
        # Import adapter dynamically
        from app.adapters import get_adapter
        adapter = get_adapter(adapter_name)
        
        if not adapter:
            raise HTTPException(status_code=404, detail=f'Adapter {adapter_name} not found')
        
        if not adapter.enabled:
            raise HTTPException(status_code=503, detail=f'Adapter {adapter_name} is disabled')
        
        # Execute request through adapter
        method = request.method.lower()
        response = await adapter.execute(method, endpoint, query_params, body)
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log request
        from app.services.logging_service import log_request
        await log_request(adapter_name, endpoint, method, response.get('status', 200), 
                         query_params, response, None, duration_ms)
        
        return JSONResponse(content=response.get('data', {}), status_code=response.get('status', 200))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'Gateway error: {str(e)}')
        duration_ms = int((time.time() - start_time) * 1000)
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/health')
async def health_check():
    from app.services.health_service import check_health
    return await check_health()

@router.get('/adapters')
async def list_adapters():
    from app.services.config_service import get_all_adapters
    return {'adapters': get_all_adapters()}
