from app.db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class UserModel(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=False, nullable=False)