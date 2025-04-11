from pydantic import BaseModel
from datetime import datetime

class FileInfo(BaseModel):
    filename: str
    org_name: str
    path_upload: str
    path_steam: str
    path_thumbnail: str
    time_play: str
    location: str
    uploaded_at: datetime