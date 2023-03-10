from flask import Flask

from .extensions import ma, db, mi, jwt
from .config import Config

from app.user.routes import user_api
from app.appointment.routes import appointment_api

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    ma.init_app(app)
    db.init_app(app)
    mi.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)

    app.register_blueprint(user_api)
    app.register_blueprint(appointment_api)

    return app