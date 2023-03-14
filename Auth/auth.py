from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException

token= OAuth2PasswordBearer(tokenUrl='user/login/1')

algorithm= 'HS256'
secret_key= 'jhf438734jyhfbyuimnyghbgthbthnbnth'
minutes= 30

def Create_token(data:dict):
    expire_time= datetime.utcnow()+ timedelta(minutes=minutes)
    data.update({'exp':expire_time})
    token= jwt.encode(data,secret_key, algorithm=algorithm)
    return token

def verify_token(token= Depends(token)):
    try:
        token_data= jwt.decode(token, secret_key, algorithms=[algorithm])
        return token_data
    except JWTError as Error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")

