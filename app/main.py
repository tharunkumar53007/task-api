from fastapi import FastAPI, HTTPException, Query
from .models import Task, Priority, TaskResponse, TaskListResponse, TaskCreate, TaskUpdate, TaskComplete, TaskActionResponse

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

@app.get("/tasks", response_model=TaskListResponse,status_code=200)
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

@app.get("/tasks/{task_id}",response_model=TaskResponse, status_code=200)
def get_taskById(task_id : int):
  for task in tasks:
    if task_id == task["id"]:
      return {
        "message" : "Task found successfully",
        "task" : task
      }
  raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks",response_model=TaskActionResponse, status_code=201)
def add_task(task : TaskCreate):
  new_id = len(tasks) + 1
  new_task = Task(
    id=new_id,
    title=task.title,
    description=task.description,
    priority=task.priority,
    due_date=task.due_date,
    )
  tasks.append(new_task)
  return {
    "message" : "Task created successfully",
    "task" : new_task
  }

@app.put("/tasks/{task_id}", response_model=TaskActionResponse,status_code=200)
def update_task(task_id : int, task : TaskUpdate):
  for old_task in tasks:
    if task_id == old_task["id"]:
      old_task["title"] = task.title
      old_task["description"] = task.description
      old_task["priority"] = task.priority
      old_task["completed"] = task.completed
      old_task["due_date"] = task.due_date

      return {
        "message" : "Task Updated Successfull",\
        "task" : old_task
      }
  
  raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id : int):
  for task in tasks:
    if task_id == task["id"]:
      tasks.remove(task)
      return
  
  raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}/complete", response_model=TaskActionResponse, status_code=200)
def patch_task(task_id : int, task_status : TaskComplete):
  for task in tasks:
    if task_id == task["id"]:
      task["completed"] = task_status.completed

      return {
        "message" : "Task status updated",
        "task" : task
      }
  
  raise HTTPException(status_code=404, detail="Task not found")

