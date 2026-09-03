from fastapi import APIRouter, Depends, BackgroundTasks
from app.schemas.task import TaskCreate, TaskOut
from app.services import task_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AsyncSessionLocal
from app.auth import get_current_user
from app.models import User
from app.task_notifications import send_notification
from app.redis_client import redis_client
import json

router = APIRouter()

CACHE_KEY_PREFIX = 'tasks_cashe'

def task_to_dict(task) -> dict: 
  return {
    "id": task.id,
    "title": task.title,
    "description": task.description,
    "completed": task.completed,
    "created_at" : task.created_at.isoformat() if task.created_at else None,
    "owner_id": task.owner_id
  }

async def get_db():
  async with AsyncSessionLocal() as session:
    yield session


@router.get('/tasks', response_model=list[TaskOut])
async def get_tasks(
  db: AsyncSession = Depends(get_db), 
  current_user: User = Depends(get_current_user)):

  cache_key = f"{CACHE_KEY_PREFIX}:{current_user.id}"
  cached = redis_client.get(cache_key)
  if cached: 
    return json.loads(cached)
  
  tasks = await task_service.get_all(db, current_user.id)
  tasks_json = json.dumps([task_to_dict(t) for t in tasks])
  redis_client.set(cache_key, tasks_json, ex=60)
  # cashe_key - ключ в кэше
  # tasks_json - значение в кэше 
  # ex=60 срок жизни кэша 60 секунд 

  
  return tasks
  # return await task_service.get_all(db, current_user.id)

@router.post('/tasks', response_model=TaskOut, status_code=201)
async def create_task(
  task_data: TaskCreate, 
  background_tasks: BackgroundTasks,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)):

  task = await task_service.create(db ,task_data, current_user.id)
  cache_key = f"{CACHE_KEY_PREFIX}:{current_user.id}"
  redis_client.delete(cache_key)

  background_tasks.add_task(send_notification, task.id, task.title)
  return task

@router.get("/tasks/search", response_model=list[TaskOut])
async def search_tasks(
  keyword: str, 
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)):
    return await task_service.search(db, keyword, current_user.id)


@router.delete('/tasks/{task_id}', status_code=204)
async def delete_task(
  task_id: int, 
  db: AsyncSession = Depends(get_db), 
  current_user: User = Depends(get_current_user)):
  cache_key = f"{CACHE_KEY_PREFIX}:{current_user.id}"
  redis_client.delete(cache_key)
  await task_service.delete(db, task_id, current_user.id)

# @router.get("/tasks/{task_id}", response_model= TaskOut)
# async def get_task(task_id: int, db: AsyncSession = Depends(get_db)): 
#   return await task_service.get_by_id(db, task_id)
