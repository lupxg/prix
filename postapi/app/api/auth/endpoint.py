from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token
from http import HTTPStatus
from .model import User
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
    
        return {'msg' : 'User created'}, HTTPStatus.CREATED
    


@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_model)
    def post(self):
        data = request.get_json()
        user:User = User.query.filter_by(username=data.get('username')).first()

        if not user or not user.check_password(data.get('password')):
            return {"msg": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED
        
        access_token = create_access_token(identity=str(user.id))

        return {"access_token": access_token}, HTTPStatus.OK


