
from fastapi import  FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config import DevelopmentConfig
from routes.api_router import api_router
from storage_manager import ensure_storage_directory_exists
from database import SessionLocal


config = DevelopmentConfig()

app = FastAPI(debug=config.DEBUG)
print("HOST => ",config.HOST)
print("PORT => ",config.PORT)

ensure_storage_directory_exists(config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200","http://192.168.1.83:4200"],  # แทนที่ * ด้วยโดเมนของ frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

UPLOAD_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR}"
UPLOAD_DIR_HLS = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS}"
HLS_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR}"
THUMBNAIL_PATH = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.IMAGE_PATH}/{config.THUMBNAIL_PATH}"
URL_HOST = config.HOST

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(UPLOAD_DIR_HLS, exist_ok=True)
# os.makedirs(HLS_DIR, exist_ok=True)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


app.mount("/videos", StaticFiles(directory=UPLOAD_DIR), name="videos")
app.mount("/images/thumbnails", StaticFiles(directory=THUMBNAIL_PATH), name="thumbnails")

app.include_router(api_router)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=True)