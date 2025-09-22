from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from passlib.hash import pbkdf2_sha256

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select

from app.schemas import UserSchema
from app.db import db
from app.blocklist import BLOCKLIST
from app.models import UserModel


bp = Blueprint("users", __name__, description="Operations on Users")


@bp.route("/register")
class UserRegister(MethodView):
    
    
    @bp.arguments(UserSchema)
    @bp.response(201)
    def post(self, user_data):
        user = UserModel(username=user_data["username"],
                         password=pbkdf2_sha256.hash(user_data["password"]))
        try:
            db.session.add(user)
            db.session.commit()
            return "User Created Successfully", 201
        except IntegrityError:
            db.session.rollback()
            abort(400, "The User has already exist")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, "Database Error")


@bp.route("/refresh")
class TokenRefresh(MethodView):
    
    
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_access_token}


@bp.route("/login")
class UserLogin(MethodView):
    
    
    @bp.arguments(UserSchema)
    def post(self, user_data):
        user = db.session.scalar(select(UserModel).where(UserModel.username == user_data["username"]))
        if user is None:
            return "User Not Found! Please create an account", 404

        if pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(401, "Invalid credentials")


@bp.route("/logout")
class UserLogout(MethodView):
    
    
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully Logged Out"}


@bp.route("/user/<int:user_id>")
class User(MethodView):
    
    
    @bp.response(200, UserSchema)
    def get(self, user_id):
        user = db.session.get(UserModel, user_id)
        if user is None:
            abort(404, "User Not Found")
        return user, 200
    
    
    @bp.response(200)
    def delete(self, user_id):
        user = db.session.get(UserModel, user_id)
        if user is None:
            abort(404, "User Not Found")
        
        try:
            db.session.delete(user)
            db.session.commit()
            return "User Deleted Successfully"
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, "Database Error")



@bp.route("/user")
class UserList(MethodView):
    
    
    @bp.response(200, UserSchema(many=True))
    def get(self):
        users = db.session.scalars(select(UserModel)).all()
        
        return users
