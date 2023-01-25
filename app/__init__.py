from flask import Flask

from .extensions import ma, db, mi
from .config import Config

from app.user.routes import user_api

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    ma.init_app(app)
    db.init_app(app)
    mi.init_app(app, db)

    app.register_blueprint(user_api)

    return app