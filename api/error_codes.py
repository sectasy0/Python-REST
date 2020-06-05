from flask import make_response

class Response(object):
    @classmethod
    def invalid_arguments(cls):
        return make_response({"status": "error", "message": "invalid arguments"}, 422)

    @classmethod
    def missing_parameters(cls):
        return make_response({"status": "error", "message": "missing parameters"}, 400)

    @classmethod
    def user_exists(cls):
        return make_response({"status": "error", "message": "user already exists"}, 400)

    @classmethod
    def email_taken(cls):
        return make_response({"status": "error", "message": "email taken"}, 400)

    @classmethod
    def unexpected_error(cls):
        return make_response({"status": "error", "message": "unexpected error"}, 400)

    @classmethod
    def wrong_credentials(cls):
        return make_response({"status": "error", "message": "wrong credentials"}, 401)

    @classmethod
    def insufficient_permissions(cls):
        return make_response({"status": "error", "message": "insufficient permissions"}, 403)

    @classmethod
    def operation_not_allowed(cls):
        return make_response({"status": "error", "message": "operation not allowed"}, 405)