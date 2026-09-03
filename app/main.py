from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks, users
from app.db import engine
from app.models import Base

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(users.router)
app.include_router(tasks.router)

@app.on_event("startup")
async def on_startup():
  # Base.metadata.create_all(bind = engine)
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  

@app.get('/')
async def root():
  return {"message": "Task Manager работает"}