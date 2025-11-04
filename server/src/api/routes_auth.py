from fastapi import APIRouter, Depends, HTTPException
from src.core.auth_schema import Register, Login, UserResponse
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.core.model import User
from src.utils.hash_verify import hashPassword, verifyPassword

router  = APIRouter()      
           
# no auth for citizen
@router.post("/register")    
def register(data:Register, db:Session = Depends(get_db)):
   is_user_exist = db.query(User).filter(data.email == User.email).first()
   if is_user_exist:
      raise HTTPException(400, "user exist")
   
   hashed_password = hashPassword(data.password)
      
   new_user = User(name=data.name, email=data.email, password=hashed_password)
   print("new user from register", new_user)
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   
   return {
      "id": new_user.id,
      "name": new_user.name,
      "email": new_user.email
   }
                    
            
@router.post("/login")    
async def login (data:Login, db:Session = Depends(get_db)):
   is_user_exist = db.query(User).filter(User.email == data.email).first()
   if not is_user_exist:
       raise HTTPException(400, "Invalid credentials.")
   
   password_hashed = verifyPassword(data.password, is_user_exist.password)
   
   if not password_hashed:
       raise HTTPException(400, "Invalid credentials.")
      
   return {
      "id": is_user_exist.id,
      "name": is_user_exist.name,
      "email": is_user_exist.email,
      "role": is_user_exist.role 
   }
