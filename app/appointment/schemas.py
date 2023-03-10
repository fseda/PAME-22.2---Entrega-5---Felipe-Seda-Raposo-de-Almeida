from app.extensions import ma

from .models import Appointment

class AppointmentSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Appointment
        load_instance = True
        ordered = True

    id = ma.Integer(dump_only=True)
    start = ma.DateTime(required=True)
    end = ma.DateTime(required=True)
    
    user_id = ma.Integer()
