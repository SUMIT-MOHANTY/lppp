from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.gateway.router import router as gateway_router
from app.gateway.middleware import RateLimitMiddleware, SecurityHeadersMiddleware
from app.adapters import init_adapters
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title='External API Gateway',
    description='Unified API Gateway for External Service Integrations',
    version='1.0.0'
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Custom middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)

# Initialize adapters
init_adapters()

# Routes
app.include_router(gateway_router, prefix='/api/v1', tags=['Gateway'])

@app.on_event('startup')
async def startup():
    logger.info('API Gateway starting up...')
    
@app.on_event('shutdown')
async def shutdown():
    logger.info('API Gateway shutting down...')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
