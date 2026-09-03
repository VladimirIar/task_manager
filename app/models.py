from sqlalchemy import Integer, String, Text, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass 

class User(Base): 
  __tablename__ = "users"
  id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
  email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
  hashed_password: Mapped[str] = mapped_column(String, nullable=False)
  is_active: Mapped[bool] = mapped_column(Boolean, default=True)
  role: Mapped[str] = mapped_column(String, default="user")

class Task(Base):
  __tablename__ = "tasks"
  id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
  title: Mapped[str] = mapped_column(String(300))
  description: Mapped[str | None] = mapped_column(Text, nullable = True)
  completed: Mapped[bool] = mapped_column(Boolean, default = False) 
  created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
  owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable= False)

# CREATE TABLE tasks (
#   id Integer PRIMARY KEY AUTOINCREMENT 
#   ...
# )

#tasks
#  ________________________________
# | id | title | descr. | completed |
#   1  | задача| null   |  false    |
#

# users 
# | user_tasks  | 
# | 20, 150, 311|