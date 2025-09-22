from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import StoreSchema
from app.models import StoreModel
from app.db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select



bp = Blueprint("stores", __name__, description="Operations on Stores")

@bp.route("/store/<int:store_id>")
class Store(MethodView):
    
    
    @bp.response(200, StoreSchema)
    def get(self, store_id):
        store = db.session.get(StoreModel, store_id)
        if store is None:
            return jsonify({"error": "Store Not Found"}), 404
        return store
    
    
    def delete(self, store_id):
        store = db.session.get(StoreModel, store_id)
        if store is None:
            return jsonify({"error": "Store Not Found"}), 404
        
        try:
            db.session.delete(store)
            db.session.commit()
            return jsonify({"Message": f"Store{store_id} Deleted Successfully"}), 204
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Database Error"}), 500


@bp.route("/store")
class StoreList(MethodView):
    
    
    @bp.response(200, StoreSchema(many=True))
    def get(self):
        stores = db.session.scalars(select(StoreModel)).all()
        return stores
    
    
    @bp.arguments(StoreSchema)
    @bp.response(201, StoreSchema)
    def post(self, store_data):
        new_store = StoreModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()
            return new_store, 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "The Store is already Exist"}), 400
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Database Error"}), 500