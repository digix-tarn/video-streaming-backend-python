from fastapi import APIRouter
from routes.stream_routes import steam_router
from routes.file_routes import file_router

# สร้าง router หลักที่รวมทุก route
api_router = APIRouter(prefix="/api")

# รวม video router และ file router
api_router.include_router(steam_router, prefix="/stream", tags=["videos"])
api_router.include_router(file_router, prefix="/files", tags=["files"])