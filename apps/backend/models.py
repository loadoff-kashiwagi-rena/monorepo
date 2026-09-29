from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, DeclarativeBase

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
  metadata = MetaData(naming_convention=naming_convention)

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
  hashed_password: Mapped[str] = mapped_column(String(255))

class LearningLog(Base):
  __tablename__ = "learning_logs"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(
    Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
  title: Mapped[str] = mapped_column(String(255))
  content: Mapped[str] = mapped_column(Text)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
