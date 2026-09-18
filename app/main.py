from fastapi import FastAPI, HTTPException, Query, Depends
from .models import Task, Priority, TaskResponse, TaskListResponse, TaskCreate, TaskUpdate, TaskComplete, TaskActionResponse, UserCreate, User, UserActionResponse
from app.auth import create_access_token, get_current_user
from app.database import tasks, users, get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.database import Base, engine
from app.models import TaskDB
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

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

@app.get("/tasks",status_code=200)
def get_tasks(completed : bool | None = None, priority : Priority | None = None, search : str | None = None, skip : int = Query(0,ge=0), limit : int = Query(10,lt=100), current_user: dict = Depends(get_current_user), db:Session = Depends(get_db)):
  
  usertasks = db.query(TaskDB).filter(TaskDB.user_id == current_user.id).all()
  return usertasks
  # get_list = []
  # for task in tasks:
  #   if task.user_id == current_user.id:
  #     if (
  #       (completed is None or task["completed"] == completed) and
  #       (priority is None or task["priority"] == priority) and
  #       (search is None or search.lower() in task["title"].lower() or search.lower() in task["description"].lower())):
  #           get_list.append(task)
        
  # return {
  #   "tasks" : get_list[skip : skip + limit]
  # }

@app.get("/tasks/{task_id}",response_model=TaskResponse, status_code=200)
def get_taskById(task_id : int,current_user :dict = Depends(get_current_user), db : Session = Depends(get_db)):
  # for task in tasks:
  #     if task_id == task.id and task.user_id == current_user.id:
  task = db.query(TaskDB).filter(task_id == TaskDB.id, TaskDB.user_id == current_user.id).first()
  if task is None:
    raise HTTPException(status_code=404, detail="Task not found")
  
  return {
        "message" : "Task found successfully",
        "task" : task
        }

@app.post("/tasks",response_model=TaskActionResponse, status_code=201)
def add_task(task : TaskCreate, current_user: dict = Depends(get_current_user), db : Session = Depends(get_db)):

  new_task = TaskDB(
    
    user_id=current_user.id,
    title=task.title,
    description=task.description,
    priority=task.priority.value,
    due_date=task.due_date,
    )
  # tasks.append(new_task)
  db.add(new_task)
  db.commit()
  db.refresh(new_task)
  
  return {
    "message" : "Task created successfully",
    "task" : new_task
  }

@app.put("/tasks/{task_id}", response_model=TaskActionResponse,status_code=200)
def update_task(task_id : int, updated_task : TaskUpdate, current_user : dict = Depends(get_current_user), db: Session = Depends(get_db)):
  # for old_task in tasks:
  #     if task_id == old_task.id and old_task.user_id == current_user.id:
  task = db.query(TaskDB).filter(task_id == TaskDB.id, current_user.id == TaskDB.user_id).first()
  
  if task is None:
    raise HTTPException(status_code=404, detail="Task not found")
  
  task.title = updated_task.title
  task.description = updated_task.description
  task.priority = updated_task.priority
  task.completed = updated_task.completed
  task.due_date = updated_task.due_date
  
  db.commit()
  db.refresh(task)

  return {
      "message" : "Task Updated Successfull",
      "task" : task
      }
  
  

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