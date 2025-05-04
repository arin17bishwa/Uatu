from sqlalchemy import Column, String, Integer, CLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ClobEntry(Base):
    __tablename__ = "UATU_CLOBS"
    __table_args__ = {"schema": "RW_API"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    exec_id = Column(String(128))
    sequence_no = Column(Integer)
    process_name = Column(String(128))
    dttm = Column(String(128))
    payload = Column(CLOB)
