from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import engine
from models import LearningLog
from datetime import datetime

with Session(engine) as session:
    session.add(LearningLog(user_id=777, title="t", content="c", created_at=datetime.now()))
    try:
        session.commit()
    except IntegrityError:
        print("制約が効いて弾かれました")