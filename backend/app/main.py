# main.py

import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import splunk_routes, clob_routes

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="Splunk Search + CLOB Viewer",
    description="Backend service to search Splunk logs and fetch CLOBs from Oracle",
    version="1.0.0",
)

# CORS setup - allow frontend (adjust origin as per your frontend port)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(splunk_routes.router, prefix="/api/splunk", tags=["Splunk Search"])
app.include_router(clob_routes.router, prefix="/api/clob", tags=["CLOB Data"])


# Optionally: startup/shutdown events
@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI backend is starting...")


@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 FastAPI backend is shutting down.")
