from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import Appointment
from .schemas import AppointmentSchema

from app.user.models import User

import datetime

class AppointmentController(MethodView):

    # Return all appointments by all users
    def get(self):
        schema = AppointmentSchema()
        appointments = Appointment.query.all()

        return schema.dump(appointments, many=True), 200

    @staticmethod
    def get_all():
        schema = AppointmentSchema()
        appointments = Appointment.query.all()

        return schema.dump(appointments, many=True), 200

class UserAppointmentController(MethodView):
    decorators = [jwt_required()]

    def get(self, user_id):
        schema = AppointmentSchema()

        user = User.query.get(user_id)
        if user_id != get_jwt_identity():
            return { 'error': 'Unauthorized' }, 401
        if not user:
            return { 'error' : 'User not found' }, 404
        
        appointments = Appointment.query.filter_by(user_id=user_id)

        return schema.dump(appointments, many=True), 200

    def post(self, user_id):

        schema = AppointmentSchema()

        user = User.query.get(user_id)
        if user_id != get_jwt_identity():
            return { 'error': 'Unauthorized' }, 401

        if not user:
            return {}, 404

        data = request.json
        data['user_id'] = user_id

        data['start'] = datetime.datetime.strptime(data['start'], '%d-%m-%Y %H:%M')
        data['end'] = datetime.datetime.strptime(data['end'], '%d-%m-%Y %H:%M')

        if data['start'] > data['end']:
            return { 'error': 'Appointment should end after start' }, 400
        
        # Check if new appointment has free slot
        appointments = AppointmentController.get_all()
        if len(appointments[0]) > 0:
            for appointment in appointments[0]:
                if isinstance(appointment, int):
                    break

                appointment_end = datetime.datetime.strptime(appointment['end'], '%Y-%m-%dT%H:%M:%S')
                if data['start'] < appointment_end:
                    return { 'error': 'Unable to overlap appointments'}, 400
        
        data['start'] = str(data['start'])
        data['end'] = str(data['end'])

        try:
            post = schema.load(data)
        except:
            return {}, 400

        post.save()

        return schema.dump(post), 201

class UserAppointmentDetails(MethodView):
    decorators = [jwt_required()]

    def get(self, user_id, id):
        schema = AppointmentSchema()

        user = User.query.get(user_id)
        if user_id != get_jwt_identity():
            return { 'error': 'Unauthorized' }, 401
        if not user:
            return { 'error' : 'User not found' }, 404

        appointment = Appointment.query.get(id)
        if not appointment:
            return { 'error' : 'Appointment not found' }, 404
        
        appointment_schema = schema.dump(appointment)

        if appointment_schema['user_id'] != user_id:
            return { 'error' : 'Unathorized access to appointment.'}, 401

        return schema.dump(appointment), 200

    def delete(self, user_id, id):
        if user_id != get_jwt_identity():
            return { 'error': 'Unauthorized' }, 401
        schema = AppointmentSchema()

        user = User.query.get(user_id)
        if not user:
            return { 'error' : 'User not found' }, 404

        appointment = Appointment.query.get(id)
        if not appointment:
            return { 'error' : 'Appointment not found' }, 404
        
        appointment_schema = schema.dump(appointment)

        if appointment_schema['user_id'] != user_id:
            return { 'error' : 'Unathorized access to appointment.'}, 401
        
        appointment.delete(appointment)

        return {}, 204
        