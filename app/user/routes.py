from flask import Blueprint
from .controller import UserController, UserDetails, UserLogin

user_api = Blueprint('user_api', __name__)

user_api.add_url_rule(
    '/users/',
    view_func=UserController.as_view('user_controller'),
    methods=['GET', 'POST']
)

user_api.add_url_rule(
    '/users/<int:id>',
    view_func=UserDetails.as_view('user_user_details'),
    methods=['GET', 'PUT', 'PATCH', 'DELETE']
)

user_api.add_url_rule(
    '/login/',
    view_func=UserLogin.as_view('user_login'),
    methods=['POST']
)