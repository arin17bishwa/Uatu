from fastapi import APIRouter, HTTPException
from services.clob_service import get_clob_content
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/{exec_id}/{sequence_no}", response_class=PlainTextResponse)
async def download_clob(exec_id: str, sequence_no: int):
    try:
        clob_data = get_clob_content(exec_id, sequence_no)
        if clob_data is None:
            raise HTTPException(status_code=404, detail="CLOB not found.")
        return clob_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
