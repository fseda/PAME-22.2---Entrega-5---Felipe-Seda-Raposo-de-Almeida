from app.models import BaseModel
from app.extensions import db

class User(BaseModel):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(20))
    # birthday = db.Column(db.DateTime)
    cpf = db.Column(db.String(11))
    phone_number = db.Column(db.String(12))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean) # O Usuário é um funcionário?

    appointments = db.relationship('Appointment', backref='User')
       
