from pydantic import BaseModel
from src.core.model import RoleEnum

class Register(BaseModel):
    name: str
    email: str
    password: str
    role: RoleEnum
    
class Login(BaseModel):
    email:str
    password:str
    role: RoleEnum
    
class UserResponse(BaseModel):
    id: str
    email: str
    
    class Config:
        orm_mode = True