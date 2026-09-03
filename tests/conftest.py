import pytest 
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import engine
from app.models import Task, User, Base
from sqlalchemy import delete
from app import models

# @pytest.fixture 
# async def clean_db():
#   async with engine.begin() as conn: 
#     await conn.run_sync(Base.metadata.drop_all)
#     await conn.run_sync(Base.metadata.create_all)
#   yield

@pytest.fixture
async def client():
  async with AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
  ) as ac: 
    yield ac
    

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

