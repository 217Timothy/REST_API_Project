import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from sqlalchemy import select

from app.db import db
from app.blocklist import BLOCKLIST
from app.resources.store import bp as StoreBlueprint
from app.resources.item import bp as ItemBlueprint
from app.resources.tag import bp as TagBlueprint
from app.resources.user import bp as UserBlueprint
from app import models


migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)
    
    app.config["JWT_SECRET_KEY"] = "303676907085738348143009969327299527622"
    jwt = JWTManager(app)
    
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "the token has been revoked",
                     "error": "token_revoked"}),
            401
        )
    
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "the token isn't fresh",
                     "error": "fresh_token_required"}),
            401
        )
    
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # users = db.session.scalars(select(UserModel)).all()
        # user_ids = [user.id for user in users]
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
            {"message": "the token has expired",
             "error": "token_expired"}),
            401
        )
    
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
            {"message": "signature verification failed",
             "error": "invalid_token"}),
             401
        )
    
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
            {"message": "Request does not contain access token",
             "error": "authorization_required"}),
            401
        )
    
    
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)    
    return app