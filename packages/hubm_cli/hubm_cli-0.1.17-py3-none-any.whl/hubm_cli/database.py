from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.utils import get_config_value
from hubm_cli import hubm_path

db_url = get_config_value(hubm_path + "/config.ini", "db_url")

engine = create_engine(db_url, pool_size=10, max_overflow=20, pool_recycle=10, pool_timeout=10)
Session = sessionmaker(bind=engine)