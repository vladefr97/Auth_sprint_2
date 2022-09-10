from typing import Any

from http import HTTPStatus

from api.v1.parsers import registration_parser
from api.v1.utils import create_jwt_tokens, save_user_to_history
from core.models import DefaultUserRole
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

        if User.find_by_login(data["login"]):
            return {"message": "User {} already exists".format(data["login"])}, HTTPStatus.CONFLICT

        role_name = DefaultUserRole.USER.value
        role_model = UserRole.get_role(user_role_type=role_name)
        new_user = User(
            login=data["login"],
            password=User.generate_hash(data["password"]),
            user_role=role_model.id,
            email=data["email"],
        )
        new_user.save_to_db()

        save_user_to_history(new_user)
        tokens = create_jwt_tokens(user_login=data["login"], user_role=role_name)

        return tokens.dict(), HTTPStatus.CREATED
