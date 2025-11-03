from jose import jwt
from datetime import datetime, timedelta

import dotenv
import os

dotenv.load_dotenv()

def create_jwt(data:dict):
    data_copy = data.copy()
    
    # expire data
    expire = datetime.utcnow() + timedelta(minutes=os.environ.get("TOKEN_EXP_MIN"))
    data_copy = data_copy.update({"exp": expire})
    
    return jwt.encode(data_copy, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM"))

