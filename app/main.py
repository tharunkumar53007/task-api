from fastapi import FastAPI, HTTPException, Query
from .models import Task
from .models import Priority
from .models import TaskResponse, TaskListResponse

app = FastAPI(
  title="Task Management API",
  description="A Mimimal Task management API",
  version="1.0.0"
)

tasks = [
  {
    "id": 8,
    "title": "Call Parents",
    "description": "Catch up with mom and dad",
    "priority": "medium",
    "completed": True,
    "due_date": "2026-09-12"
  },
  {
    "id": 9,
    "title": "Clean the House",
    "description": "Vacuum, dust, and organize the living room",
    "priority": "low",
    "completed": False,
    "due_date": "2026-09-19"
  },
  {
    "id": 10,
    "title": "Prepare Presentation",
    "description": "Create slides for the client pitch",
    "priority": "high",
    "completed": False,
    "due_date": "2026-09-21"
  }
]

@app.get("/")
def greeting():
  return {
    "message" : "Task API is running"
  }

@app.get("/tasks", response_model=TaskListResponse)
def get_tasks(completed : bool | None = None, priority : Priority | None = None, search : str | None = None, skip : int = Query(0,ge=0), limit : int = Query(10,lt=100)):
  
  get_list = []
  for task in tasks:
   if (
     (completed is None or task["completed"] == completed) and
     (priority is None or task["priority"] == priority) and
     (search is None or search.lower() in task["title"].lower() or search.lower() in task["description"].lower())):
        get_list.append(task)
        
  return {
    "tasks" : get_list[skip : skip + limit]
  }

@app.get("/tasks/{task_id}",response_model=TaskResponse)
def get_taskById(task_id : int):
  for task in tasks:
    if task_id == task["id"]:
      return {
        "message" : "Task found successfully",
        "task" : task
      }
  raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task : Task):
  tasks.append(task)
  return {
    "message" : "Task added successfully",
    "task" : task
  }

@app.put("/tasks/{task_id}")
def update_task(task_id : int, task : Task):
  for old_task in tasks:
    if task_id == old_task["id"]:
      old_task["title"] = task.title
      old_task["description"] = task.description
      old_task["priority"] = task.priority
      old_task["completed"] = task.completed
      old_task["due_date"] = task.due_date

      return {
        "message" : "Task Updated Successfull",\
        "task" : task
      }
  
  raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id : int):
  for task in tasks:
    if task_id == task["id"]:
      tasks.remove(task)

      return {
        "message" : "Task deleted successsfully",
        "task" : task
      }
  
  raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}/complete")
def patch_task(task_id : int):
  for task in tasks:
    if task_id == task["id"]:
      task["completed"] = True

      return {
        "message" : "Task status updated",
        "task" : task
      }
  
  raise HTTPException(status_code=404, detail="Task not found")

