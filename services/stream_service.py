from fastapi import HTTPException
from config import DevelopmentConfig
from fastapi.responses import FileResponse, JSONResponse
import os
from sqlalchemy.ext.asyncio import AsyncSession
from models.file_model import File
from repositories.file_crud import get_video_list_to_db
from utils.date_utils import seconds_to_hms

config = DevelopmentConfig()

UPLOAD_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR}"
UPLOAD_DIR_HLS = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS}"
HLS_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR}"
THUMBNAIL_PATH = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.IMAGE_PATH}/{config.THUMBNAIL_PATH}"
URL_HOST = "localhost"

async def get_video_hls(video_id: str):
    try:
        # สร้าง path สำหรับ HLS ที่เกี่ยวข้อง
        video_quality_urls = []
        for quality in ["240p", "480p", "720p", "1080p"]:
            file_path = os.path.join(HLS_DIR, video_id, f"{quality}.m3u8")
            
            # ตรวจสอบว่าไฟล์มีอยู่หรือไม่
            if os.path.exists(file_path):
                # ถ้าไฟล์มีอยู่ ให้เพิ่ม URL ที่เหมาะสมใน list
                video_quality_urls.append(f"http://{URL_HOST}:8000/videos/{video_id}/{quality}.m3u8")
        
        # ถ้าไม่มีไฟล์ใด ๆ กลับค่าผิดพลาด
        if not video_quality_urls:
            return JSONResponse(
                status_code=404,
                content={"error": "No available streams for this video_id"}
            )
        
        # คืนค่า URL ของไฟล์ m3u8
        return JSONResponse(
            status_code=200,
            content={"urls": video_quality_urls}
        )
    
    except Exception as e:
        # ถ้ามีข้อผิดพลาดที่เกิดขึ้น ให้ส่งข้อความข้อผิดพลาด
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )

def stream_video():
    path = os.path.join(UPLOAD_DIR, "converted_720p.mp4")
    return FileResponse(path, media_type="video/mp4")

async def get_video_list(db: AsyncSession = None):
    try:
        list = await get_video_list_to_db(db)
        print(list)

        if not list:
            return JSONResponse(status_code=404, content={"message": "No videos found"})
        
        for v in list: 
            duration_raw = float(v.time_play)
            print(duration_raw)
            v.duration = seconds_to_hms(duration_raw)
            print(v.duration)
            del v.time_play
            v.title = v.org_name
            del v.org_name
            v.code_file = os.path.splitext(v.filename)[0]
            del v.filename
            v.path_thumbnail = os.path.basename(v.path_thumbnail)

        video_list = [{"id": v.id, "title": v.title, "duration": v.duration,"code":v.code_file,"thumbnail":v.path_thumbnail} for v in list]  # ดัดแปลงตาม schema

        return {"videos": video_list}

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": str(e)})

def get_thumbnail(image_name: str):
    try:
        image_path = os.path.join(THUMBNAIL_PATH, image_name)
        print(image_path)

        # ตรวจสอบว่าไฟล์มีอยู่หรือไม่
        if os.path.exists(image_path):
            return FileResponse(image_path, media_type="image/jpeg")
        else:
            return JSONResponse(
                status_code=404,
                content={"error": "Image not found"}
            )
    except Exception as e:
        # ถ้ามีข้อผิดพลาดภายในให้ส่งข้อความข้อผิดพลาด
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )
