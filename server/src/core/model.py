from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum, Float
import datetime
import enum

Base = declarative_base()

class SourceEnum(str, enum.Enum):
    SMS = "SMS"
    WEB = "WEB"
    WHATSAPP = "WHATSAPP"
    
class RoleEnum(str,enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role=Column(Enum(RoleEnum), default=SourceEnum.USER)

class Incident(Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    severity = Column(String)
    description = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    phone_number = Column(String, default="")
    status = Column(String, default="PENDING")
    image_url = Column(String, default=None)
    source = Column(Enum(SourceEnum), default=SourceEnum.WEB)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
