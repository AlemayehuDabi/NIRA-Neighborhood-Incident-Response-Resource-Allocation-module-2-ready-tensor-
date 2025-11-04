from pydantic import BaseModel

class Register(BaseModel):
    name: str
    email: str
    password: str
    
class Login(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id: str
    email: str
    
    class Config:
        from_attributes = True
