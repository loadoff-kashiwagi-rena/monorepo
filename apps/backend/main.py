from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import LearningLog
from schemas import LogCreate, LogResponse

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
