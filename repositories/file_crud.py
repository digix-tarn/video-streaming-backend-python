
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.file_model import File
from schemas.file_schema import FileInfo

async def save_file_to_db(file_info: FileInfo, db_session: AsyncSession):
    db_file = File(
        filename=file_info.filename,
        org_name=file_info.org_name,
        path_upload=file_info.path_upload,
        path_steam=file_info.path_steam,
        path_thumbnail=file_info.path_thumbnail,
        time_play=file_info.time_play,
        location=file_info.location,
        uploaded_at=file_info.uploaded_at
    )
    db_session.add(db_file)
    await db_session.commit()
    await db_session.refresh(db_file)
    return db_file

async def get_video_list_to_db(db: AsyncSession):
    result = await db.execute(select(File))
    return result.scalars().all()