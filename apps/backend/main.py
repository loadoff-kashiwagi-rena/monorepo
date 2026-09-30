from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm

from auth import hash_password, verify_password, create_access_token
from database import get_db
from models import LearningLog, User
from schemas import LogCreate, LogResponse, UserCreate, Token

app = FastAPI()

@app.get("/logs", response_model=List[LogResponse])
def read_logs(db: Session = Depends(get_db)):
    return db.query(LearningLog).all()

@app.get("/logs/{log_id}", response_model=LogResponse)
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = db.get(LearningLog, log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

@app.post("/logs", response_model=LogResponse, status_code=201)
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = LearningLog(
        title=log.title,
        content=log.content,
        user_id=1,
        created_at=datetime.now(),
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.put("/logs/{log_id}", response_model=LogResponse)
def update_log(log_id: int, log: LogCreate, db: Session = Depends(get_db)):
    db_log = db.get(LearningLog, log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    db_log.title = log.title
    db_log.content = log.content
    db.commit()
    db.refresh(db_log)
    return db_log

@app.delete("/logs/{log_id}", status_code=204)
def delete_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.get(LearningLog, log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(db_log)
    db.commit()
    return None

@app.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
