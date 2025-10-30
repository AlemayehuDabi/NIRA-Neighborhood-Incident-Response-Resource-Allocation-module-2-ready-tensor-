from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum
import datetime
import enum

Base = declarative_base()

class SourceEnum(str, enum.Enum):
    SMS = "SMS"
    WEB = "WEB"
    WHATSAPP = "WHATSAPP"

class Incident(Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    severity = Column(String)
    description = Column(String)
    location = Column(String)
    phone_number = Column(String, default="")
    status = Column(String, default="PENDING")
    image_url = Column(String, default=None)
    source = Column(Enum(SourceEnum), default=SourceEnum.WEB)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
