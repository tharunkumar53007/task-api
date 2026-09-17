from pydantic import BaseModel, Field
from enum import Enum
from datetime import date
from sqlalchemy import Boolean, Integer,String, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class TaskDB(Base):
  __tablename__ = "tasks"
  
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  user_id: Mapped[int] = mapped_column(Integer)
  title: Mapped[int] = mapped_column(String(100))
  description: Mapped[str] = mapped_column(String(500))
  priority: Mapped[str] = mapped_column(String(10))
  completed: Mapped[bool] = mapped_column(Boolean, default=False)
  due_date: Mapped[date] = mapped_column(Date)

class Priority(str, Enum):
  LOW = "low"
  MEDIUM = "medium"
  HIGH = "high"

class Task(BaseModel):
  id : int = Field(gt=0)
  user_id: int = Field(gt=0)
  title : str = Field(min_length=3, max_length=100)
  description : str = Field(min_length=5, max_length=500)
  priority : Priority
  completed : bool = False
  due_date : date
  
class TaskBody(BaseModel):
  id : int
  title : str
  description : str
  priority : Priority
  completed : bool
  due_date : date

class TaskResponse(BaseModel):
  message : str
  task : TaskBody
  
class TaskListResponse(BaseModel):
  tasks : list[TaskBody]
  
class TaskCreate(BaseModel):
  title : str = Field(min_length=3, max_length=100)
  description : str = Field(min_length=5, max_length=500)
  priority : Priority
  due_date : date
  
class TaskUpdate(BaseModel):
  title : str = Field(min_length=3, max_length=100)
  description : str = Field(min_length=5, max_length=500)
  priority : Priority
  completed : bool
  due_date : date
  
class TaskComplete(BaseModel):
  completed : bool
  
class TaskActionResponse(BaseModel):
  message : str
  task : TaskBody
  
class User(BaseModel):
  id : int
  username : str
  password : str
  
class UserCreate(BaseModel):
  username : str
  password : str
  
class UserLogin(BaseModel):
  username : str
  password : str
  
class UserActionResponse(BaseModel):
  message : str
  user : User