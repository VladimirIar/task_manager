from app import models
from app.schemas import task as schemas
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all(db: AsyncSession, user_id: int) -> list[models.Task]:
  # return db.query(models.Task).all()
  # select(models.Task)
  # db.execute()
  result = await db.execute(
    select(models.Task).filter(models.Task.owner_id == user_id)
    )
  return result.scalars().all()

async def get_by_id(db: AsyncSession, task_id: int, user_id: int) -> models.Task:
  result = await db.execute(
    select(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id)
  )
  task = result.scalars().first()
  if not task: 
    raise HTTPException(
      status_code=404, 
      detail="Задача не найденна")

  return task
  # return db.query(models.Task).filter(models.Task.id == task_id).first()


async def create(
    db: AsyncSession, 
    task_data: schemas.TaskCreate,
    user_id: int ) -> models.Task:
  task = models.Task(
    title = task_data.title,
    description = task_data.description,
    owner_id=user_id
  ) 
  db.add(task)
  await db.commit()
  await db.refresh(task)
  return task

async def delete(db: AsyncSession, task_id: int, user_id: int) -> None: 
  task = await get_by_id(db, task_id, user_id)
  await db.delete(task)
  await db.commit()

async def search(db: AsyncSession, keyword: str, user_id) -> list[models.Task]:
    result = await db.execute(
        select(models.Task).filter(models.Task.owner_id == user_id, models.Task.title.contains(keyword))
    )
    return result.scalars().all()