from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from database import get_db
from services.file_service import upload_hls_steam,convert_to_hls
from sqlalchemy.ext.asyncio import AsyncSession
from config import DevelopmentConfig
config = DevelopmentConfig()

file_router = APIRouter()

UPLOAD_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR}"
UPLOAD_DIR_HLS = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS}"
HLS_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR}"
URL_HOST = config.HOST

@file_router.post("/upload-hls")
async def upload_hls(background_tasks: BackgroundTasks,file: UploadFile = File(...),db: AsyncSession = Depends(get_db)):
    if not file:
        raise HTTPException(status_code=422, detail="No file uploaded")
    upload_file = await upload_hls_steam(file,db)
    # print("upload_file",upload_file)
    if upload_file['status'] == 200 :
        response = {"message": "File uploaded successfully", "path": f"{UPLOAD_DIR_HLS}/{upload_file['base_name']}/master.m3u8"}
        background_tasks.add_task(convert_to_hls, upload_file['input_path'], upload_file['base_name'])
        return response
    else :
        return upload_file