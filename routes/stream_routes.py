from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from services.stream_service import get_thumbnail, get_video_hls,stream_video, get_video_list
from config import DevelopmentConfig
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
config = DevelopmentConfig()

steam_router = APIRouter()

UPLOAD_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR}"


@steam_router.get("/")
def read_root():
    return {"message": "Hello, world!"}



@steam_router.get("/video-hls/{video_id}")
def video_hls(video_id: str):
    caller = get_video_hls(video_id)

    return caller

@steam_router.get("/stream")
def stream():
    caller = stream_video()
    return caller

@steam_router.get("/videos-list")
async def video_list(db: AsyncSession = Depends(get_db)):
    caller = await get_video_list(db)
    return caller

@steam_router.get("/thumbnails/{image_name}")
async def thumbnail(image_name: str):
    caller = get_thumbnail(image_name)
    return caller