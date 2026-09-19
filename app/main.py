from fastapi import FastAPI, HTTPException, Query, Depends
from .models import Priority, TaskResponse, TaskListResponse, TaskCreate, TaskUpdate, TaskComplete, TaskActionResponse, UserCreate, User, UserActionResponse
from app.auth import create_access_token, get_current_user
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.database import Base, engine
from app.models import TaskDB, UserDB
from sqlalchemy.orm import Session
from sqlalchemy import or_

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
  
  query = db.query(TaskDB).filter(TaskDB.user_id == current_user.id)
  if completed is not None:
    query = query.filter(TaskDB.completed == completed)
  
  if priority is not None:
    query = query.filter(TaskDB.priority == priority)
    
  if search:
    query = query.filter(
      or_(
        TaskDB.title.ilike(f"%{search}%"),
        TaskDB.description.ilike(f"%{search}%")
      )
    )
  
  query = query.offset(skip).limit(limit=limit)
  tasks = query.all()
  return tasks
  

@app.get("/tasks/{task_id}",response_model=TaskResponse, status_code=200)
def get_taskById(task_id : int,current_user :dict = Depends(get_current_user), db : Session = Depends(get_db)):
  
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
  
  db.add(new_task)
  db.commit()
  db.refresh(new_task)
  
  return {
    "message" : "Task created successfully",
    "task" : new_task
  }

@app.put("/tasks/{task_id}", response_model=TaskActionResponse,status_code=200)
def update_task(task_id : int, updated_task : TaskUpdate, current_user : dict = Depends(get_current_user), db: Session = Depends(get_db)):
 
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
def delete_task(task_id : int, current_user : dict = Depends(get_current_user), db:Session = Depends(get_db)):
 
  task = db.query(TaskDB).filter(task_id == TaskDB.id, current_user.id == TaskDB.user_id).first()
  
  if task is None:
    raise HTTPException(status_code=404, detail="Task not found")

  db.delete(task)
  db.commit()
  return

@app.patch("/tasks/{task_id}/complete", response_model=TaskActionResponse, status_code=200)
def patch_task(task_id : int, task_status : TaskComplete, current_user : dict = Depends(get_current_user), db: Session = Depends(get_db)):
  task = db.query(TaskDB).filter(task_id == TaskDB.id, current_user.id == TaskDB.user_id).first()
  
  if task is None:
    raise HTTPException(status_code=404, detail="Task not found")
  
  task.completed = task_status.completed
  
  db.commit()
  db.refresh(task)
  return {
        "message" : "Task status updated",
        "task" : task
        }
  

@app.post("/register", status_code=200, response_model=UserActionResponse)
def register_user(user : UserCreate, db: Session = Depends(get_db)):
  
  new_user = UserDB(username = user.username, password = user.password)
  
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  return {
    "message" : "User created successfully",
    "user" : new_user
  }
  
@app.post("/login",status_code=200)
def login_user(user : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):

   current_user = db.query(UserDB).filter(UserDB.username == user.username).first()
   if not current_user:
     raise HTTPException(status_code=401, detail="user not found")
   if current_user.password != user.password:
     raise HTTPException(status_code=401, detail="Incorrect username or password")
   access_token = create_access_token(
      {
      "sub" : str(current_user.id)
      }
        )
        
   return {
          "message" : "User login successfull",
          "access_token" : access_token,
          "user" : current_user
        }
      
  