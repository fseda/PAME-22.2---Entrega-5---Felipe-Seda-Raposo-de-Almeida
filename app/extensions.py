from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

ma = Marshmallow()
db = SQLAlchemy()
mi = Migrate()