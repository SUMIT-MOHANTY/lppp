from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .config import get_db_config
from .models import Base

_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        cfg = get_db_config()
        url = f"postgresql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
        _engine = create_engine(url, pool_size=cfg['pool_size'], max_overflow=cfg['max_overflow'], pool_timeout=cfg['pool_timeout'], pool_recycle=3600)
    return _engine

def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine())
    return _SessionLocal()

def init_db():
    Base.metadata.create_all(bind=get_engine())
