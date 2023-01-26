from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy#, MetaData
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


ma = Marshmallow()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
# db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
db = SQLAlchemy()
mi = Migrate()
jwt = JWTManager()