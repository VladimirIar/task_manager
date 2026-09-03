import pytest 
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models import Task, User
from sqlalchemy import delete


@pytest.fixture
async def client():
  async with AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
  ) as ac: 
    yield ac
    
@pytest.fixture
async def clean_db():
    """
    подробности ошибки описаны в комментарии в test_tasks
    """
    from app.db import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        # Удаляем ВСЕ задачи
        await db.execute(delete(Task))
        # Удаляем ВСЕХ пользователей
        await db.execute(delete(User))
        # Сохраняем изменения
        await db.commit()
# В следующем занятии переделаем правильно,
# чтобы удалялись исключительно тестовые данные 
# созданные в ходе автотеста 
    yield

@pytest.fixture 
async def auth_headers(client):
  await client.post("/register", json={
    "email": "test@mail.com",
    "password": "secret123"
  })

  login_response = await client.post("/login", json={
    "email": "test@mail.com",
    "password": "secret123"
  })
  token = login_response.json()["access_token"]
  return {"Authorization": f'Bearer {token}'}

