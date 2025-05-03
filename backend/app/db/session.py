from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ORACLE_URL = "oracle+cx_oracle://username:password@host:port/service_name"

engine = create_engine(ORACLE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
