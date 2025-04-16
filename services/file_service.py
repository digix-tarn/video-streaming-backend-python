from datetime import datetime
from config import DevelopmentConfig
from fastapi.responses import FileResponse, JSONResponse
import os
from fastapi import File, UploadFile
import subprocess
import uuid
import shutil
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.file_schema import FileInfo  # Schema
from repositories.file_crud import save_file_to_db

from utils.file_utils import get_video_duration_seconds, extract_random_frame,date_thumbnail

config = DevelopmentConfig()


UPLOAD_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR}"
UPLOAD_DIR_HLS = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS}"
HLS_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR}"
THUMBNAIL_PATH = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.IMAGE_PATH}/{config.THUMBNAIL_PATH}"
URL_HOST = config.HOST

def convert_to_hls(input_path: str, base_name: str):
    output_dir = os.path.join(HLS_DIR, base_name)
    os.makedirs(output_dir, exist_ok=True)

    resolutions = {
        "240p": {"scale": "426:240", "bitrate": "400k"},
        "480p": {"scale": "854:480", "bitrate": "800k"},
        "720p": {"scale": "1280:720", "bitrate": "1500k"},
        "1080p": {"scale": "1920:1080", "bitrate": "3000k"},
    }

    full_cmd = ["ffmpeg", "-i", input_path]
    for i, (res, cfg) in enumerate(resolutions.items()):
        full_cmd += [
            "-vf", f"scale={cfg['scale']}", "-c:v", "libx264", "-b:v", cfg["bitrate"],
            "-hls_time", "4", "-hls_playlist_type", "vod",
            "-hls_segment_filename", os.path.join(output_dir, f"{res}_%03d.ts"),
            os.path.join(output_dir, f"{res}.m3u8")
        ]

    try:
        subprocess.run(full_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting video to HLS: {e}")

    # สร้าง master.m3u8
    master_path = os.path.join(output_dir, "master.m3u8")
    with open(master_path, "w") as f:
        f.write("#EXTM3U\n")
        for res in resolutions:
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION={resolutions[res]['scale'].replace(':', 'x')}\n")
            f.write(f"{res}.m3u8\n")
    
    print(f"Video HLS conversion completed: {master_path}")


async def upload_hls_steam(file: UploadFile = File(...),db: AsyncSession = None):
    try:
        # print("file",file)
        # สุ่มชื่อใหม่สำหรับไฟล์
        name_file_org, _ = os.path.splitext(file.filename)

        new_filename = f"{uuid.uuid4().hex}.mp4"

        input_path = os.path.join(UPLOAD_DIR_HLS, new_filename)

        base_name = os.path.splitext(new_filename)[0]

        steam_path = f"{UPLOAD_DIR_HLS}/{base_name}/master.m3u8"
        content = await file.read()

        duration_seconds = await get_video_duration_seconds(content)
        # print(duration_seconds)
        frame_bytes = await extract_random_frame(content, duration_seconds)
        # print(frame_bytes)

        thumbnail_time = date_thumbnail()
        thumbnail_path = f"{THUMBNAIL_PATH}/{base_name}_thumbnail_{thumbnail_time}.jpg"
        thumbnail_path_stamp = f"{base_name}_thumbnail_{thumbnail_time}.jpg"
        steam_path_stamp = f"{config.HLS_DIR}/{base_name}/master.m3u8"
        input_path_stamp = f"{config.UPLOAD_DIR_HLS}/{base_name}/master.m3u8"
        # print(thumbnail_path)

        with open(thumbnail_path, "wb") as f:
            f.write(frame_bytes)

        file_info = FileInfo(
            filename=new_filename,
            org_name=name_file_org,
            path_upload=input_path_stamp,
            path_steam=steam_path_stamp,
            path_thumbnail=thumbnail_path_stamp,
            time_play=f"{duration_seconds}",
            location=input_path,
            uploaded_at=datetime.now()
        )

        # บันทึกไฟล์
        with open(input_path, "wb") as f:
            f.write(content)


        # ส่งคืน response ทันที
        
        # print(base_name)
        await save_file_to_db(file_info, db)
        
        response = {"status": 200,"input_path": input_path,"base_name": base_name,"steam_path": steam_path}
        # print(response)

        return response
    
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": str(e)})
