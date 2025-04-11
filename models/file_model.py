# app/models/file_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    org_name = Column(String)
    path_upload = Column(Text)
    path_steam = Column(Text)
    path_thumbnail = Column(Text)
    time_play = Column(Text)
    location = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # def __repr__(self):
    #     return f"<File(id={self.id}, filename={self.filename}, uploaded_at={self.uploaded_at})>"
