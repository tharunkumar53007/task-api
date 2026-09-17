from fastapi import FastAPI, HTTPException, Query, Depends
from .models import Task, Priority, TaskResponse, TaskListResponse, TaskCreate, TaskUpdate, TaskComplete, TaskActionResponse, UserCreate, User, UserActionResponse
from app.auth import create_access_token, get_current_user
from app.database import tasks, users
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(
  title="Task Management API",
  description="A Mimimal Task management API",
  version="1.0.0"
)


@app.get("/")
def greeting():
  return {
    "message" : "Task API is running"
  }

@app.get("/tasks", response_model=TaskListResponse,status_code=200)
def get_tasks(completed : bool | None = None, priority : Priority | None = None, search : str | None = None, skip : int = Query(0,ge=0), limit : int = Query(10,lt=100), current_user: dict = Depends(get_current_user)):
  
  get_list = []
  for task in tasks:
    if task.user_id == current_user.id:
      if (
        (completed is None or task["completed"] == completed) and
        (priority is None or task["priority"] == priority) and
        (search is None or search.lower() in task["title"].lower() or search.lower() in task["description"].lower())):
            get_list.append(task)
        
  return {
    "tasks" : get_list[skip : skip + limit]
  }

@app.get("/tasks/{task_id}",response_model=TaskResponse, status_code=200)
def get_taskById(task_id : int,current_user :dict = Depends(get_current_user)):
  for task in tasks:
      if task_id == task.id and task.user_id == current_user.id:
        return {
          "message" : "Task found successfully",
          "task" : task
        }
  raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks",response_model=TaskActionResponse, status_code=201)
def add_task(task : TaskCreate, current_user: dict = Depends(get_current_user)):
  new_id = len(tasks) + 1
  new_task = Task(
    id=new_id,
    user_id=current_user.id,
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
def update_task(task_id : int, task : TaskUpdate, current_user : dict = Depends(get_current_user)):
  for old_task in tasks:
      if task_id == old_task.id and old_task.user_id == current_user.id:
        old_task.title = task.title
        old_task.description = task.description
        old_task.priority = task.priority
        old_task.completed = task.completed
        old_task.due_date = task.due_date

        return {
          "message" : "Task Updated Successfull",\
          "task" : old_task
        }
  
  raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id : int, current_user : dict = Depends(get_current_user)):
  for task in tasks:
      if task_id == task.id and task.user_id == current_user.id:
        tasks.remove(task)
        return
  
  raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}/complete", response_model=TaskActionResponse, status_code=200)
def patch_task(task_id : int, task_status : TaskComplete, current_user : dict = Depends(get_current_user)):
  for task in tasks:
      if task_id == task.id and task.user_id == current_user.id:
        task.completed = task_status.completed

        return {
          "message" : "Task status updated",
          "task" : task
        }
  
  raise HTTPException(status_code=404, detail="Task not found")

@app.post("/register", status_code=200, response_model=UserActionResponse)
def register_user(user : UserCreate):
  new_id = len(users) + 1
  new_user = User(id=new_id, username=user.username, password=user.password)
  users.append(new_user)
  
  return {
    "message" : "User created successfully",
    "user" : new_user
  }
  
@app.post("/login",status_code=200)
def login_user(user : OAuth2PasswordRequestForm = Depends()):
  for user_item in users:
    if user_item.username == user.username:
      if user_item.password == user.password:
        access_token = create_access_token(
          {
            "sub" : str(user_item.id)
          }
        )
        
        return {
          "message" : "User login successfull",
          "access_token" : access_token,
          "user" : user_item
        }
      else:
        raise HTTPException(status_code=401, detail="Password incorrect")
  
  raise HTTPException(status_code=404, detail="User not found")