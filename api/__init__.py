from flask import Flask, jsonify, request
from flask_login import LoginManager, UserMixin
from flask_restful import Api, Resource
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'YOUR DATABASE ADRESS'
}

app.config['SECRET_KEY'] = '<---YOUR_SECRET_FORM_KEY--->'

cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = MongoEngine(app)
lm = LoginManager(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
api = Api(app)


class User(UserMixin, db.Document):
    username = db.StringField(max_length=60, unique=True)
    password = db.StringField()
    email = db.EmailField(default='email@gmail.com', unique=True)
    admin = db.BooleanField(default=False)
    register_date = db.DateTimeField(default=datetime.now())


@lm.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': "error",
        'message': f'The {token_type} token has expired, please log in again.'
    }), 401


from api.auth import Login, Register, Refresh
api.add_resource(Register, '/api/v1.0/auth/register')
api.add_resource(Refresh, '/api/v1.0/auth/refresh')
api.add_resource(Login, '/api/v1.0/auth/login')

from api.users import User, AllUsers
api.add_resource(User, '/api/v1.0/users/<username>')
api.add_resource(AllUsers, '/api/v1.0/users')
