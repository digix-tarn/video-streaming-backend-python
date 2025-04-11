import subprocess
import json
from fastapi import UploadFile
import tempfile
import os
import random
from datetime import datetime

async def get_video_duration_seconds(video_bytes: bytes) -> float:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_bytes)
        tmp.flush()
        video_path = tmp.name

    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            print("ffprobe error:", result.stderr.decode())
            return 0.0

        duration = float(result.stdout.decode().strip())
        return duration
    finally:
        os.remove(video_path)
    
async def extract_random_frame(video_bytes: bytes, duration_seconds: float) -> bytes:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            input_path = temp_file.name
            temp_file.write(video_bytes)

        timestamp = round(random.uniform(1, max(duration_seconds - 1, 1)), 2)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as out_file:
            output_path = out_file.name

        result = subprocess.run([
            "ffmpeg",
            "-ss", str(timestamp),
            "-i", input_path,
            "-frames:v", "1",
            "-q:v", "2",
            output_path,
            "-y"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("ffmpeg stdout:", result.stdout.decode())
        print("ffmpeg stderr:", result.stderr.decode())

        if result.returncode != 0:
            print(f"Error running ffmpeg: {result.stderr.decode()}")
            return b''

        with open(output_path, "rb") as f:
            frame_bytes = f.read()

        os.remove(input_path)
        os.remove(output_path)

        return frame_bytes

    except Exception as e:
        print(f"Error extracting frame: {e}")
        return b''
    
def date_thumbnail():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m%d")
    return formatted_date