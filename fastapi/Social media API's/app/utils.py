from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_txt,hashed_pass):
    return pwd_context.verify(plain_txt,hashed_pass)
    