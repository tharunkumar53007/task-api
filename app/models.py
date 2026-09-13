from pydantic import BaseModel
class Task(BaseModel):
  id : int
  title : str
  description : str
  priority : str
  completed : bool = False
  due_date : str