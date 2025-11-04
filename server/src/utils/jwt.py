from jose import jwt
from datetime import datetime, timedelta
import os

def create_jwt(data: dict):
    data_copy = data.copy()
    
    # Convert env value to int
    expire_minutes = int(os.environ.get("TOKEN_EXP_MIN", 30))
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    
    data_copy["exp"] = expire  # set exp correctly
    
    token = jwt.encode(
        data_copy, 
        os.environ.get("JWT_SECRET"),
        algorithm=os.environ.get("JWT_ALGORITHM")
    )
    
    return token
