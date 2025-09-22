from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, ForeignKey

class ItemModel(db.Model):
    __tablename__ = "items"
    
    id: Mapped[int] =  mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float(precision=2), unique=False, nullable=False)
    store_id: Mapped[int] = mapped_column(Integer, ForeignKey("stores.id"), unique=False, nullable=False)
    
    store = relationship("StoreModel", back_populates="items")
    tags = relationship("TagModel", back_populates="items", secondary="item_tags")