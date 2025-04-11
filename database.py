# app/database.py
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.file_model import Base  # Import model จากไฟล์ที่เก็บใน models
from config import DevelopmentConfig

config = DevelopmentConfig()

DATABASE_URL = config.DATABASE_URL

# ตั้งค่า engine สำหรับเชื่อมต่อ PostgreSQL แบบ async
engine = create_async_engine(DATABASE_URL, echo=True)

# สร้าง session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ฟังก์ชันในการสร้างตาราง
async def init_db():
    async with engine.begin() as conn:
        # สร้างตารางในฐานข้อมูล
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    try:
        async with SessionLocal() as session:
            yield session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")