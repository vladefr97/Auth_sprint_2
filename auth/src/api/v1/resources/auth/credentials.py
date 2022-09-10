from typing import Any

from http import HTTPStatus

from db.models import User
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse

change_password_parser = reqparse.RequestParser()
change_password_parser.add_argument("new_password", help="This field cannot be blank", required=True)

change_login_parser = reqparse.RequestParser()
change_login_parser.add_argument("new_login", help="This field cannot be blank", required=True)


class UserPasswordChangeAPI(Resource):
    @jwt_required()
    def put(self) -> tuple[dict[str, Any], int]:
        """
        Change password method for users
        ---
        tags:
          - auth
        parameters:
          - in: body
            name: body
            schema:
              id: UserPasswordChangeAPI
              required:
                - new_password
              properties:
                new_password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
        responses:
          200:
            description: Success change user's  password
          401:
            description: Error response
          429:
            description: Too many requests. Limit in interval seconds.
        """
        data = change_password_parser.parse_args()

        hashed_new_password = User.generate_hash(data["new_password"])
        current_user.change_password(hashed_new_password)

        return {}, HTTPStatus.OK


class UserLoginChangeAPI(Resource):
    @jwt_required()
    def put(self) -> tuple[dict[str, Any], int]:
        """
        Change login method for users
        ---
        tags:
          - auth
        parameters:
          - in: body
            name: body
            schema:
              id: UserLoginChangeAPI
              required:
                - new_login
              properties:
                new_login:
                  type: string
                  description: The user's username.
                  default: "JohnDoe"
        responses:
          200:
            description: Success change user's  login
          401:
            description: Error response
          429:
            description: Too many requests. Limit in interval seconds.
        """
        # TODO: сделать проверку существующего логина

        data = change_login_parser.parse_args()

        if current_user.login != data["new_login"]:
            current_user.change_login(data["new_login"])
            out = {"message": "User change login"}, HTTPStatus.OK
        else:
            out = {"message": "Logins should not match"}, HTTPStatus.CONFLICT
        return out
