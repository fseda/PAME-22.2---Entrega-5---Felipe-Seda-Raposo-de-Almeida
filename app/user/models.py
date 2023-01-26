from app.models import BaseModel
from app.extensions import db

import bcrypt

class User(BaseModel):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(20))
    # birthday = db.Column(db.DateTime)
    cpf = db.Column(db.String(11))
    phone_number = db.Column(db.String(12))
    email = db.Column(db.String(100))
    password_hash = db.Column(db.LargeBinary(256))
    is_admin = db.Column(db.Boolean) # O Usuário é um funcionário?

    appointments = db.relationship('Appointment', backref='User', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('Password: write-only field.')
       

    @password.setter
    def password(self, password) -> None:
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash)