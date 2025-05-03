from fastapi import APIRouter, HTTPException
from models.splunk import SearchRequest, SearchResponseGroup
from services.splunk_service import run_splunk_query, group_and_sort_events

router = APIRouter()

@router.post("/", response_model=list[SearchResponseGroup])
async def search_splunk(req: SearchRequest):
    try:
        raw_results = run_splunk_query(req)
        grouped_results = group_and_sort_events(raw_results)
        return grouped_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
