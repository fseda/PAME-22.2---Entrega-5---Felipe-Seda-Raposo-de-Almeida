from app.extensions import ma

from .models import User
from app.appointment.schemas import AppointmentSchema

class UserSchema(ma.SQLAlchemySchema):

    class Meta:
        model = User
        load_instance = True
        ordered = True

    id = ma.Integer(dump_only=True)
    full_name = ma.String(required=True)
    # birthday = ma.DateTime(required=True)
    cpf = ma.String(required=True)
    phone_number = ma.String(required=True)
    email = ma.String(required=True)
    password = ma.String(required=True)
    is_admin = ma.Boolean()

    appointments = ma.List(ma.Nested(AppointmentSchema), dump_only=True)

class LoginSchema(ma.Schema):
    email = ma.String(required=True)
    password = ma.String(load_only=True, required=True)