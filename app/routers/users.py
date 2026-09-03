from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserOut, Token
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import AsyncSessionLocal
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model = UserOut, status_code=201)
async def register(user_data: UserCreate): 
  async with AsyncSessionLocal() as db:
    result = await db.execute(select(User).filter(User.email == user_data.email))
    exisitin_user = result.scalars().first()

    if exisitin_user: 
      raise HTTPException(
        status_code= status.HTTP_400_BAD_REQUEST,
        detail = "Пользователь с таким email уже существует"
      )
    user = User(
      email = user_data.email,
      hashed_password = hash_password(user_data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login", response_model=Token)
async def login(user_data: UserCreate):
  async with AsyncSessionLocal() as db: 
    result = await db.execute(select(User).filter(User.email == user_data.email))
    user = result.scalars().first()

    if not user or not verify_password(user_data.password, user.hashed_password):
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Неверный email или пароль"
      )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)