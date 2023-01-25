from flask import request
from flask.views import MethodView

from .models import Appointment
from .schemas import AppointmentSchema

from app.user.models import User

class AppointmentController(MethodView):

    # Return all appointments by all users
    def get(self):
        schema = AppointmentSchema()
        appointments = Appointment.query.all()

        return schema.dump(appointments, many=True), 200

class UserAppointmentController(MethodView):
    def get(self, user_id):
        schema = AppointmentSchema()

        user = User.query.get(user_id)
        if not user:
            return { 'error' : 'User not found' }, 404
        
        posts = Appointment.query.filter_by(user_id=user_id)

        return schema.dump(posts, many=True), 200
                
    def post(self, user_id):
        schema = AppointmentSchema()

        user = User.query.get(user_id)
        if not user:
            return {}, 404

        data = request.json
        data['user_id'] = user_id

        try:
            post = schema.load(data)
        except:
            return {}, 400

        post.save()

        return schema.dump(post), 201

class UserAppointmentDetails(MethodView):
    def get(self, user_id, id):
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

        return schema.dump(appointment), 200

    def delete(self, user_id, id):
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
        