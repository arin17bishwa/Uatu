from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from config import export_db_config

db_config = export_db_config()

ORACLE_URL = URL(
    drivername="oracle+oracledb",
    username=db_config["DB_USER"],
    host=db_config["DB_HOST"],
    port=db_config["DB_PORT"],
    password=db_config["DB_PASSWORD"],
    database=None,
    query={"service_name": db_config["DB_NAME"]},
)

engine = create_engine(ORACLE_URL, thick_mode=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
