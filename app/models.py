from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text
from datetime import datetime
from app.database import Base

class AdapterConfig(Base):
    __tablename__ = 'adapter_configs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    base_url = Column(String)
    auth_type = Column(String)
    api_key = Column(String, nullable=True)
    bearer_token = Column(String, nullable=True)
    enabled = Column(Boolean, default=False)
    timeout = Column(Integer, default=30)
    retry_count = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RequestLog(Base):
    __tablename__ = 'request_logs'
    id = Column(Integer, primary_key=True, index=True)
    adapter_name = Column(String, index=True)
    endpoint = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    request_data = Column(JSON, nullable=True)
    response_data = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    duration_ms = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class ApiKey(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    name = Column(String)
    rate_limit = Column(Integer, default=100)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
