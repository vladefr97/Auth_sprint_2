from typing import Any

from http import HTTPStatus

from api.v1.parsers import registration_parser
from api.v1.utils import create_jwt_tokens, save_user_to_history
from db.relational.models.user import User
from db.relational.models.userrole import UserRole
from flask_restful import Resource


class UserRegistrationAPI(Resource):
    def post(self) -> tuple[dict[str, Any], int]:
        """
        Registration method for users
        ---
        tags:
          - auth
        parameters:
          - in: body
            name: body
            schema:
              id: UserRegistration
              required:
                - login
                - password
              properties:
                login:
                  type: string
                  description: The user's username.
                  default: "JohnDoe"
                email:
                  type: string
                  description: The user's email.
                  default: "email@gmail.com"
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
        responses:
          201:
            description: That user was created
          400:
            description: Bad request response
          409:
            description: User already exists
          429:
            description: Too many requests. Limit in interval seconds
        """
        data = registration_parser.parse_args()

        if not data["login"] or not data["password"] or not data["email"]:
            return {}, HTTPStatus.BAD_REQUEST

        registered_user = User.find_by_login_or_email(login=data["login"], email=data["email"])
        if registered_user:
            return {
                "message": f"User with login: {registered_user.login} or"
                f" email: {registered_user.email} already exists"
            }, HTTPStatus.CONFLICT

        registered_user = User.save_user_with_default_role(
            login=data["login"], email=data["email"], password=data["password"]
        )

        role_model = UserRole.find_by_id(role_id=registered_user.user_role)

        save_user_to_history(registered_user)
        tokens = create_jwt_tokens(user_login=registered_user.login, user_role=role_model.role_type)

        return tokens.dict(), HTTPStatus.CREATED
