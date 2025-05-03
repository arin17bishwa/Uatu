from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class KVFilter(BaseModel):
    key: str
    value: str

class TimeRange(BaseModel):
    earliest: str  # e.g., "-15m" or ISO datetime string
    latest: str    # e.g., "now" or ISO datetime string

class SearchRequest(BaseModel):
    raw_query: Optional[str] = None
    time_range: TimeRange
    process_name: Optional[str] = None
    environment: Optional[str] = None
    execution_id: Optional[str] = None
    kv_filters: Optional[List[KVFilter]] = []

class SplunkEvent(BaseModel):
    exec_id: str
    sequence_no: int
    timestamp: str
    data: Dict[str, Any]  # Arbitrary key-value pairs
    has_clob: bool = False  # Indicates if CLOB is available (lazy, inferred)

class SearchResponseGroup(BaseModel):
    exec_id: str
    events: List[SplunkEvent]
