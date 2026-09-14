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