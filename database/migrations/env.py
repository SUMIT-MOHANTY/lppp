from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models import Base
from config import get_db_config

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

cfg = get_db_config()
config.set_main_option('sqlalchemy.url', f"postgresql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}")
target_metadata = Base.metadata
