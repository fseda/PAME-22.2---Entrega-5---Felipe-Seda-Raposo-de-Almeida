from flask import request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

from .models import User
from .schemas import UserSchema, LoginSchema

# from .utils import validate_data

class UserController(MethodView):

    def get(self):
        schema = UserSchema(only=['full_name', 'email'])
        users = User.query.all()

        return schema.dump(users, many=True), 200

    def post(self):
        schema = UserSchema()
        data = request.json

        print(data)

        data['birthday'] = str(datetime.datetime.strptime(data['birthday'], '%d-%m-%Y'))
        print(data)

        try:
            user = schema.load(data)
        except:
            return {}, 400

        email_already_in_use = UserDetails.get_by_email(data['email'])

        if email_already_in_use:
            return { 'error': 'Email address already in use.'}, 400

        cpf_already_in_use = UserDetails.get_by_cpf(data['cpf'])
        if cpf_already_in_use:
            return { 'error': 'CPF already in use.'}, 400

        if not data['is_admin']:
            data['is_admin'] = False
        
        # Save in database
        user.save()

        return schema.dump(user), 201

class UserDetails(MethodView):

    decorators = [jwt_required()]

    def get(self, id):
        schema = UserSchema()
        user = User.query.get(id)
        if id != get_jwt_identity():
            return { 'error': 'Unauthorized access' }, 401

        if not user:
            return { 'error': 'User not found' }, 404

        return schema.dump(user)

    @staticmethod
    def get_by_email(email):
        schema = UserSchema()
        user = User.query.filter_by(email=email).first()
        return schema.dump(user)

    @staticmethod
    def get_by_cpf(cpf):
        schema = UserSchema()
        user = User.query.filter_by(cpf=cpf).first()
        return schema.dump(user)
        
    def put(self, id):
        schema = UserSchema()
        user = User.query.get(id)
        if id != get_jwt_identity():
            return { 'error': 'Unauthorized access' }, 401

        if not user:
            return { 'error': 'User not found' }, 404
        
        old_data = schema.dump(user)
        data = request.json

        email_already_in_use = UserDetails.get_by_email(data['email'])
        if email_already_in_use and (data['email'] != old_data['email']):
            return { 'error': 'Email address already in use.' }, 400

        cpf_already_in_use = UserDetails.get_by_cpf(data['cpf'])
        if cpf_already_in_use and (data['cpf'] != old_data['cpf']):
            return { 'error': 'CPF already in use.' }, 400

        if not data['is_admin']:
            data['is_admin'] = False

        try:
            user = schema.load(data, instance=user)
        except:
            return {}, 400

        user.save()

        return schema.dump(user), 201
    
    def patch(self, id):
        schema = UserSchema()
        user = User.query.get(id)
        if id != get_jwt_identity():
            return { 'error': 'Unauthorized access' }, 401

        if not user:
            return { 'error': 'User not found' }, 404
        
        old_data = schema.dump(user)
        data = request.json

        email_already_in_use = UserDetails.get_by_email(data['email'])
        print(email_already_in_use, data['email'], old_data['email'])
        if email_already_in_use and (data['email'] != old_data['email']):
            return { 'error': 'Email address already in use.'}, 400

        cpf_already_in_use = UserDetails.get_by_cpf(data['cpf'])
        if cpf_already_in_use and (data['cpf'] != old_data['cpf']):
            return { 'error': 'CPF already in use.'}, 400

        try:
            user = schema.load(data, instance=user, partial=True)
        except:
            return {'asdf':'asdf'}, 400

        # email and cpf fields have to be sent when patching otherwise accessing 
        # data['email'] and data['cpf'] will result in internal server error (500)

        user.save()

        return schema.dump(user), 201

    def delete(self, id):
        schema = UserSchema()
        user = User.query.get(id)
        if id != get_jwt_identity():
            return { 'error': 'Unauthorized access' }, 401

        if not user:
            return { 'error': 'User not found' }, 404

        user.delete(user)

        return {}, 204

class UserLogin(MethodView):
    def post(self): 
        schema = LoginSchema()
        data = schema.load(request.json)

        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return { 'error': 'User not found' }, 404
        
        if not user.check_password(data['password']):
            return { 'error': 'Invalid password' }, 401

        # Access token expires in 30 minutes
        token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(minutes=30))
        
        return { 'user': UserSchema().dump(user), 'token': token }, 200