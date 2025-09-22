from app.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey


class TagModel(db.Model):
    __tablename__ ="tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    store_id: Mapped[int] = mapped_column(Integer, ForeignKey("stores.id"), nullable=False)
    
    store = relationship("StoreModel", back_populates="tags")
    items = relationship("ItemModel", back_populates="tags", secondary="item_tags")