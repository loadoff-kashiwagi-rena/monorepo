from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import SessionLocal

from database import get_db
from models import LearningLog
from schemas import LogResponse

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

@app.post("/logs")
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = LearningLog(title=log.title, content=log.content, user_id=log.user_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.put("/logs/{log_id}", response_model=LogResponse)
def update_log(log_id: int)

@app.delete("/logs/{log_id}", status_code=204)
def delete_log(log_id: int, )