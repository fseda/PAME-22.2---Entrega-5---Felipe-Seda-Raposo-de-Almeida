from app.models import BaseModel
from app.extensions import db

class Appointment(BaseModel):
    __tablename__ = 'Appointment'

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))


    
