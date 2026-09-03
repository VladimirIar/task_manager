from dotenv import load_dotenv 
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- Хэширование паролей ----

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool: 
  return pwd_context.verify(password, hashed)

# ---- Создание JWT токена ----

def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
  to_encode = data.copy()
  expire_minutes = expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
  expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User: 
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Неверный токен: отсутствует поле sub")
  except JWTError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Токен недействителен или истёк")

  async with AsyncSessionLocal() as db:
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()

  if user is None: 
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
    )
  return user