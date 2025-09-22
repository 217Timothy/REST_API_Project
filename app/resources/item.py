from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from app.schemas import ItemSchema, ItemUpdateSchema
from app.models import ItemModel 
from app.db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select

bp = Blueprint("items", __name__, description="Operations on Items")


@bp.route("/item/<int:item_id>")
class Item(MethodView):
    
    
    @jwt_required()
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        item = db.session.get(ItemModel, item_id)
        if item is None:
            return jsonify({"error": "Item Not Found"}), 404
        return item
    
    
    @jwt_required(fresh=True)
    def delete(self, item_id):
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, "admin privilege required")
        
        item = db.session.get(ItemModel, item_id)
        if item is None:
            return jsonify({"error": "Item Not Found"}), 404
        
        try :
            db.session.delete(item)
            db.session.commit()
            return jsonify({"Message": f"Item{item_id} Deleted Successfully"}), 204
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Database Error"}), 500
    
    
    @jwt_required()
    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def put(self, updated_data, item_id):
        item = db.session.get(ItemModel, item_id)
        if item is None:
            return jsonify({"error": "Item Not Found"}), 404

        allowed = {"name", "price", "store_id"}
        for key, value in updated_data.items():
            if key in allowed:    
                setattr(item, key, value)
        
        try:
            db.session.commit()
            return item
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"error": "Integrity Error"}), 400
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Database Error"}), 500


@bp.route("/item")
class ItemList(MethodView):
    
    
    @jwt_required()
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        items = db.session.scalars(select(ItemModel)).all()
        return items
    
    
    @jwt_required(fresh=True)
    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, item_data):
        new_item = ItemModel(**item_data)
        try:
            db.session.add(new_item)
            db.session.commit()
            return new_item, 201
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"error": "Integrity Error", "detail": str(e.orig)}), 400
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Database Error"}), 500