from flask import request, jsonify, Blueprint, abort, make_response
from flask_restful import Resource
from flask_login import login_user
from flask_jwt_extended import (create_access_token, jwt_required,
        jwt_refresh_token_required, create_refresh_token, get_jwt_identity)
from datetime import timedelta

from api import bcrypt, User, api
from api.error_codes import Response


class Refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        return make_response({
            "status": "success",
            "access_token": create_refresh_token(identity=current_user,
                                            expires_delta=timedelta(minutes=60)),
            "message": "new token generated succesfully"
        })

class Register(Resource):
    def post(self):
        keys = ('username', 'password', 'email')
        
        rjson = request.json
        if rjson is None: return Response.missing_parameters()
        if all(elem in rjson for elem in keys):
            if '' in rjson.values():
                return Response.invalid_arguments()

            if User.objects(username=rjson['username']):
                return Response.user_exists()
            if User.objects(email=rjson['email']):
                return Response.email_taken()

            User(password=bcrypt.generate_password_hash(rjson['password']),
             username=rjson['username'], email=rjson['email']).save()

            return make_response(jsonify({
                "status": "success",
                "message": "user successful created"
            }), 201)
            
        else: return Response.missing_parameters()
        return Response.unexpected_error()


class Login(Resource):
    def post(self):
        keys = ('username', 'password')

        rjson = request.json
        if rjson is None: return Response.missing_parameters()
        if all(elem in rjson for elem in keys):
            if '' in rjson.values():
                return Response.invalid_arguments()

            user = User.objects(username=rjson['username']).first()

            if user and bcrypt.check_password_hash(user.password, rjson['password']):
                login_user(user)

                return make_response(jsonify({
                    "status": "success",
                    "message": "successful log in!",
                    "access_token": create_access_token(identity=user.username,
                                                    expires_delta=timedelta(minutes=60)),
                    "refresh_token": create_refresh_token(identity=user.username,
                                                    expires_delta=timedelta(minutes=60))
                }))

            else:
                return Response.wrong_credentials()

        else: return Response.missing_parameters()
        return Response.unexpected_error()