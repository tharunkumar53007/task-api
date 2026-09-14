from pydantic import BaseModel, Field
from enum import Enum
from datetime import date

class Priority(str, Enum):
  LOW = "low"
  MEDIUM = "medium"
  HIGH = "high"

class Task(BaseModel):
  id : int = Field(gt=0)
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