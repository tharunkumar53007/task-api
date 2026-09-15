from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "tharunsecure53007"
ALGORITHM = "HS256"

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