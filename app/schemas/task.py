from pydantic import BaseModel, Field
from typing import Optional 
from datetime import datetime

class TaskCreate(BaseModel):
  title: str = Field(..., min_length=1, max_length=100)
  description: Optional[str] = ""

class TaskUpdate(BaseModel): 
  title: Optional[str] = None
  description: Optional[str] = None
  completed: Optional[bool] = None

class TaskOut(BaseModel):
  id: int
  title: str 
  description: Optional[str] = None
  completed: bool
  created_at: Optional[datetime] = None
  owner_id: int  
  class Config:
    form_attributes = True

# class Task(TaskCreate):
#   id: int
#   completed: bool = False
