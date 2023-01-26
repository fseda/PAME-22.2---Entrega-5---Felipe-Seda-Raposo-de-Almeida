from app.extensions import ma

from .models import Appointment

class AppointmentSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Appointment
        load_instance = True
        ordered = True

    id = ma.Integer(dump_only=True)
    start = ma.String(required=True)
    # end = ma.DateTime()
    
    user_id = ma.Integer()
