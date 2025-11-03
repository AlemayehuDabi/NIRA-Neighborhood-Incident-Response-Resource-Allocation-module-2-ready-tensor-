from passlib.context import CryptContext

pwt_context = CryptContext(schemes="bcript", deprecate="auto")

def hassPassword(password:str):
    hashedPassword = pwt_context.hash(password)
    return hashedPassword

def VerifyPassword(password:str, hashedPassword:str):
    matched = pwt_context.verify(password,hashedPassword)
    return matched