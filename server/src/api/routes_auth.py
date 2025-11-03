from fastapi import APIRouter
from src.core.auth_schema import Register, Login

router  = APIRouter()
        
   
@router.post("/register")    
def register(data:Register):
   pass
                    
            
@router.post("/login")    
async def login (data:Login):
    pass
