from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    APP_NAME = "MyApp"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "videos")
    UPLOAD_DIR_HLS = os.getenv("UPLOAD_DIR_HLS", "uploads")
    HLS_DIR = os.getenv("HLS_DIR", "videos")
    IMAGE_PATH = os.getenv("IMAGE_PATH", "images")
    THUMBNAIL_PATH = os.getenv("THUMBNAIL_PATH", "thumbnails")
    MAIN_PATH = os.getenv("MAIN_PATH")
    SUB_PATH = os.getenv("SUB_PATH")
    DATABASE_URL = os.getenv("DATABASE_URL")

class DevelopmentConfig(Config):
    DEBUG = True
    APP_NAME = "MyApp"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT"))
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "videos")
    UPLOAD_DIR_HLS = os.getenv("UPLOAD_DIR_HLS", "uploads")
    HLS_DIR = os.getenv("HLS_DIR", "videos")
    IMAGE_PATH = os.getenv("IMAGE_PATH", "images")
    THUMBNAIL_PATH = os.getenv("THUMBNAIL_PATH", "thumbnails")
    MAIN_PATH = os.getenv("MAIN_PATH")
    SUB_PATH = os.getenv("SUB_PATH")
    DATABASE_URL = os.getenv("DATABASE_URL")

class ProductionConfig(Config):
    DEBUG = False