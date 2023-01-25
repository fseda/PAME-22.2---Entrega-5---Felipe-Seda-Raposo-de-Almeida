from flask import Blueprint
from .controller import AppointmentController, UserAppointmentController, UserAppointmentDetails

appointment_api = Blueprint('appointment_api', __name__)

appointment_api.add_url_rule(
    '/appointments/',
    view_func=AppointmentController.as_view('appointment_controller'),
    methods=['GET']
)

appointment_api.add_url_rule(
    '/users/<int:user_id>/appointments/',
    view_func=UserAppointmentController.as_view('user_appointment_controller'),
    methods=['GET', 'POST']
)

appointment_api.add_url_rule(
    '/users/<int:user_id>/appointments/<int:id>/',
    view_func=UserAppointmentDetails.as_view('user_appointment_details'),
    methods=['GET', 'DELETE']
)