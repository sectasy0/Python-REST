from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import jsonify, request, make_response
from datetime import datetime

from api import User as UserModel, api, bcrypt
from api.error_codes import Response


class AllUsers(Resource):
    @jwt_required
    def get(self):
        return make_response(jsonify({
            "status": "success",
            "content": [dict(username=u.username, email=u.email, admin=u.admin,
                             register_date=u.register_date) for u in UserModel.objects.all()],
        }))


class User(Resource):
    @jwt_required
    def get(self, username):
        user = UserModel.objects(username=username).first()
        return make_response((jsonify({
            "status": "success",
            "content": {'username': user.username, 'email': user.email,
                        'register_date': user.register_date}
        }) if user else ""), 200 if user else 404)

    @jwt_required
    def put(self, username):
        user = get_jwt_identity()

        password = request.json['password']
        allowed_fields = ('username', 'email', 'admin', 'password')

        if UserModel.objects(username=user).first().admin:
            user = UserModel.objects(username=username).first_or_404()

            for field in allowed_fields:
                fieldValue = request.json.get(field)
                if fieldValue is not None:
                    if field == 'password':
                        if password is not None:
                            setattr(user, field, str(
                                bcrypt.generate_password_hash(password).decode('utf-8')))
                            user.save()
                    else:
                        setattr(user, field, fieldValue)
                    user.save()

            return make_response(jsonify({
                "status": "success",
                "message": "resource updated successfully"
            }), 200)

        return Response.insufficient_permissions()

    @jwt_required
    def delete(self, username):
        user = get_jwt_identity()

        if UserModel.objects(username=user).first().admin:
            if UserModel.objects(username=username).first().username == user:
                return Response.operation_not_allowed()

            user = UserModel.objects(username=username).first_or_404().delete()

            return make_response(jsonify({
                "status": "success",
                "message": "resource deleted successfully" 
            }), 200)

        return Response.insufficient_permissions()
