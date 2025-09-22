from app.db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey

# 中介表
class ItemTagsModel(db.Model):
    __tablename__ = "item_tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey("items.id"))
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id"))