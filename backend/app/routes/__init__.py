from fastapi import APIRouter
from routes.splunk_routes import router as splunk_router
from routes.clob_routes import router as clob_router

router = APIRouter()
router.include_router(splunk_router, prefix="/search", tags=["Splunk Search"])
router.include_router(clob_router, prefix="/clob", tags=["CLOB Access"])
