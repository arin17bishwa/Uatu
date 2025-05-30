from typing import Optional

from sqlalchemy.orm import Session

from models.db import ClobEntry


def get_clob_content(db: Session, exec_id: str, sequence_no: int) -> Optional[str]:
    entry = db.query(ClobEntry).filter_by(exec_id=exec_id, sequence_no=sequence_no).first()
    if entry and entry.payload:
        return entry.payload.read() if hasattr(entry.payload, "read") else str(entry.payload)
    return None
