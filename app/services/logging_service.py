import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

async def log_request(adapter_name: str, endpoint: str, method: str, 
                     status_code: int, request_data: Optional[Dict],
                     response_data: Optional[Dict], error: Optional[str],
                     duration_ms: int):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'adapter': adapter_name,
        'endpoint': endpoint,
        'method': method,
        'status': status_code,
        'duration_ms': duration_ms,
        'error': error
    }
    
    logger.info(f'Request: {log_entry}')
    
    # In production, store in database
    # from app.database import SessionLocal
    # from app.models import RequestLog
    # db = SessionLocal()
    # db.add(RequestLog(...))
    # db.commit()
