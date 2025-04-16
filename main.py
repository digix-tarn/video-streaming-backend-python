
from fastapi import  FastAPI, Response
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

class CORSEnabledStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: dict) -> Response:
        response: Response = await super().get_response(path, scope)
        # ดึงค่า origin จาก request headers
        headers = dict(scope.get("headers") or [])
        origin = headers.get(b"origin", b"").decode()
        allowed_origins = ["http://localhost:4200", "http://192.168.1.83:4200"]
        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
        # หรือถ้าต้องการให้เปิดทั้งโดเมนใน dev mode สามารถกำหนดเป็น "*"
        # response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

UPLOAD_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR}"
UPLOAD_DIR_HLS = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS}"
HLS_DIR = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR}"
THUMBNAIL_PATH = f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.IMAGE_PATH}/{config.THUMBNAIL_PATH}"
URL_HOST = config.HOST

app.mount("/videos", CORSEnabledStaticFiles(directory=HLS_DIR), name="videos")
app.mount("/images/thumbnails", StaticFiles(directory=THUMBNAIL_PATH), name="thumbnails")

# @app.get("/")
# def read_root():
#     return {"message": "Hello, world!"}


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=True)