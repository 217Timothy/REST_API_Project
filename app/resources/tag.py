from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import TagSchema, ItemAndTagSchema
from app.models import TagModel, StoreModel, ItemModel
from app.db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select


bp = Blueprint("tags", __name__, description="Operations on Tags")


@bp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    
    
    @bp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = db.session.get(StoreModel, store_id)
        if store is None:
            return abort(404, "Store Not Found")
        tags = store.tags
        return tags


    @bp.arguments(TagSchema)
    @bp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
            return tag, 201
        except IntegrityError:
            db.session.rollback()
            abort(400, "Integrity Error")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, "Database Error")


@bp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    
    
    @bp.response(200, TagSchema)
    def get(self, tag_id):
        tag = db.session.get(TagModel, tag_id)
        if tag is None:
            return abort(404, "Tag Not Found")
        return tag
    
    
    @bp.response(204, TagSchema)
    @bp.alt_response(404, description="Tag Not Found")
    @bp.alt_response(400, description="the Tag is assign to one or more items")
    def delete(self, tag_id):
        tag = db.session.get(TagModel, tag_id)
        if tag is None:
            abort(404, "Tag Not Found")
        if tag.items:
            abort(400, "The Tag has assigned to one or more Items")
        
        try:
            db.session.delete(tag)
            db.session.commit()
            return 204
        except IntegrityError:
            db.session.rollback()
            abort(400, "This Tag is assign to a Item. You cannot delete it")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, "Database Error")


@bp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    
    
    @bp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = db.session.get(ItemModel, item_id)
        tag = db.session.get(TagModel, tag_id)
        if item is None:
            abort(404, "Item Not Found")
        if tag is None:
            abort(404, "Tag Not Found")
        
        item.tags.append(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
            return tag
        except IntegrityError:
            db.session.rollback()
            abort(400, "")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, "Database Error")


    @bp.response(204, TagSchema)
    def delete(self, item_id, tag_id):
        item = db.session.get(ItemModel, item_id)
        tag = db.session.get(TagModel, tag_id)
        if item is None:
            abort(404, "Item Not Found")
        if tag is None:
            abort(404, "Tag Not Found")
        
        item.tags.remove(tag)
        
        try:
            db.session.commit()
            return 204
        except IntegrityError:
            db.session.rollback()
            abort(400, "")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, "Database Error")


@bp.route("/tag")
class TagList(MethodView):
    
    
    @bp.response(200, TagSchema(many=True))
    def get(self):
        tags = db.session.scalars(select(TagModel)).all()
        return tags