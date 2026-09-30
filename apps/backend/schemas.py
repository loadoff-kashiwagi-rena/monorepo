from datetime import datetime
from pydantic import BaseModel

class LogCreate(BaseModel):
  title: str
  content: str

class LogResponse(BaseModel):
  id: int
  title: str
  content: str
  created_at: datetime
  user_id: int

  class Config:
    from_attributes = True

class UserCreate(BaseModel):
  email: str
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"
