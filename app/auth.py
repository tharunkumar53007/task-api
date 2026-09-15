from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.database import users

SECRET_KEY = "tharunsecure53007"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
  to_encode = data.copy()
  
  expire = datetime.now(timezone.utc) + timedelta(minutes=30)
  to_encode.update({"exp": expire})
  token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return token

def verify_token(token : str):
  payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
  )
  
  return payload

def get_current_user(token : str = Depends(oauth2_scheme)):
  payload = verify_token(token=token)
  user_id = int(payload["sub"])
  for user in users:
    if user_id == user.id:
      return user
  
  raise HTTPException(status_code=401, detail="User not found")