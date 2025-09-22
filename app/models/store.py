from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String


class StoreModel(db.Model):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    
    items = relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = relationship("TagModel", back_populates="store", lazy="dynamic", cascade="all, delete")