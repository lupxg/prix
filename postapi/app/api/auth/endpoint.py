import sqlalchemy
from flask_restx import Namespace, Resource, fields
from flask import request
from http import HTTPStatus
from .model import User
from .utils import generate_token, verify_token
from ...extensions import db

api = Namespace('auth', description='auth namespace')

user_model = api.model('User', {
    "id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
})

@api.route('/resgiter')
class UserRegistration(Resource):
    @api.doc("User registration", security='Bearer')
    @api.response(HTTPStatus.CREATED, "User created")
    @api.expect(user_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'error' : 'Missing credentials'}, HTTPStatus.BAD_REQUEST
        
        if User.query.filter_by(username=username).first():
            return {'error':'Username exists'}, HTTPStatus.CONFLICT

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
    
        return {'message' : 'User created'}, HTTPStatus.CREATED
    


@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_model)
    def post(self):
        data = request.get_json()
        user:User = User.query.filter_by(username=data.get('username')).first()

        if not user or not user.check_password(data.get('password')):
            return {'error':'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
        
        access_token = generate_token(user.id, 'access')
        refresh_token = generate_token(user.id, 'refresh')

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': user.id
        }, HTTPStatus.OK


