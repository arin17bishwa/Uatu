from sqlalchemy import Column, String, Integer, CLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClobEntry(Base):
    __tablename__ = "your_clob_table"

    exec_id = Column(String(255), primary_key=True)
    sequence_no = Column(Integer, primary_key=True)
    content = Column(CLOB)
