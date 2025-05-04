from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from db.session import get_db
from services.clob_service import get_clob_content

router = APIRouter()


@router.get("/{exec_id}/{sequence_no}", response_class=PlainTextResponse)
async def download_clob(exec_id: str, sequence_no: int, db: Session = Depends(get_db)):
    try:
        clob_data = get_clob_content(db, exec_id, sequence_no)
        if clob_data is None:
            raise HTTPException(status_code=404, detail="CLOB not found.")
        return clob_data
    except KeyError as e:
        raise HTTPException(status_code=500, detail=str(e))
