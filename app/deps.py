from fastapi import Depends, HTTPException, status
from app.auth import get_current_user
from app.models import User

async def reqire_admin(user: User = Depends(get_current_user)) -> User:
  if user.role != "admin":
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Доступ только для админа"
    )
  return user