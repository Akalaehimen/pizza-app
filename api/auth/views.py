from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

 # auth_namespace
# Namespace for Authentication
# This namespace is used to define the routes for authentication purposes.
auth_namespace = Namespace('auth', description='Namespace for Authentication')

# Models
#  This model defines the Signup model for authentication purposes.
#  It contains three fields: username, email, and password.
#  All of these fields are required in order to create a valid Signup instance.
signup_model = auth_namespace.model(
    'Signup', {
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password")
    }
)

# This model defines the Login model for authentication purposes.
# It contains two fields: email and password.
# Both of these fields are required in order to create a valid Login instance.
# The Login model is used to generate a JWT token.
login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password")
    }
)

# This model defines the User model for authentication purposes.
# It contains six fields: id, username, email, password_hash, is_active, and is_staff.
# The id field is an integer and is automatically generated by the database.
# The username, email, and password_hash fields are strings.
# The is_active and is_staff fields are booleans.
# The User model is used to marshal the User instance into a JSON object.
user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password_hash': fields.String(required=True, description="A password"),
        'is_active': fields.Boolean(description="This shows if a User is active or not"),
        'is_staff': fields.Boolean(description="This shows that if a User is a member of staff")
    }
)


# Routes
# This route is used to register a new user.
# It takes a Signup model as input and returns a User model as output.
# If the user is successfully registered, a 201 status code is returned.
# If the user is not successfully registered, a 400 status code is returned.
# The route is accessed by sending a POST request to the /signup endpoint.
# The route is decorated with the auth_namespace.expect() decorator.
# This decorator is used to validate the input data.
# The route is decorated with the auth_namespace.marshal_with() decorator.
# This decorator is used to marshal the User instance into a JSON object.
@auth_namespace.route('/signup')
class SignUp(Resource):

    # post
    # this decorator is used to validate the input data.
    @auth_namespace.expect(signup_model)
    # this decorator is used to marshal the User instance into a JSON object.
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
            Register a User 
        """

        # get the data from the request
        data = request.get_json()

        # create a new user
        # the data is passed to the User constructor
        # the password is hashed using the generate_password_hash() function
        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )

        # save the new user to the database
        # then the new user is added to the database session
        # then the database session is committed
        """
        the save function is defined in the model/users.py 
        and imported from the models.users module
        """
        new_user.save()

        # return the new user and a 201 status code
        return new_user, HTTPStatus.CREATED


# This route is used to generate a JWT token.
# It takes a Login model as input and returns a JSON object as output.
# If the user is successfully logged in, a 201 status code is returned.
# If the user is not successfully logged in, a 400 status code is returned.
# The route is accessed by sending a POST request to the /login endpoint.
# The route is decorated with the auth_namespace.expect() decorator.
# This decorator is used to validate the input data.
@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token
        """

        # get the data from the request
        data = request.get_json()

        # get the email and password from the data
        email = data.get('email')
        password = data.get('password')

        # get the user from the database
        user = User.query.filter_by(email=email).first()

        # check if the user exists
        # if the user exists, check if the password is correct
        # if the password is correct, generate an access token and a refresh token
        # if the password is not correct, return a 401 status code
        # if the user does not exist, return a 401 status code
        # the identity is set to the user's username
        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            # return the access token and the refresh token
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            # return the response and a 201 status code
            return response, HTTPStatus.CREATED


# This route is used to generate a new access token.
# It takes no input and returns a JSON object as output.
# If the access token is successfully generated, a 200 status code is returned.
# If the access token is not successfully generated, a 401 status code is returned.
@auth_namespace.route('/refresh')
class Refresh(Resource):
    # jwt_required
    # refresh tokens are used to generate new access tokens
    # refresh is set to True
    @jwt_required(refresh=True)
    def post(self):
        """
            Generate Refresh Token
        """
        # get the username from the JWT token
        # from the login route, the identity is set to the user's username
        # we get the user's username using the get_jwt_identity() function
        # the get_jwt_identity() returns the current user's username
        username = get_jwt_identity()

        # generate a new access token
        access_token = create_access_token(identity=username)

        # return the access token and a 200 status code
        return {'access_token': access_token}, HTTPStatus.OK