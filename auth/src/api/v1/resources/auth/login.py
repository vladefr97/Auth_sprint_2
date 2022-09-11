from http import HTTPStatus

from api.v1.parsers import auth_parser
from api.v1.utils import create_jwt_tokens, save_user_to_history
from db.relational.models.user import User
from db.relational.models.userrole import UserRole
from flask_restful import Resource


class UserLoginAPI(Resource):
    def post(self) -> tuple[dict, type(HTTPStatus)]:
        """
        Login method for users
        ---
        tags:
          - auth
        parameters:
          - in: body
            name: body
            schema:
              id: UserLogin
              required:
                - login
                - password
              properties:
                login:
                  type: string
                  description: The user's username.
                  default: "JohnDoe"
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
        responses:
          200:
            description: Success user's login
            schema:
              properties:
                message:
                  type: string
                  description: Response message
                access_token:
                  type: string
                refresh_token:
                  type: string
                  description: Response message

          400:
            description: Bad request response
          404:
            description: Not found
          429:
            description: Too many requests. Limit in interval seconds
        """
        data = auth_parser.parse_args()
        current_user = User.find_by_login(data["login"])

        if not current_user:
            return {"message": "User {} doesn't exist".format(data["login"])}, HTTPStatus.NOT_FOUND

        if User.verify_hash(data["password"], current_user.password):
            user_role_model = UserRole.find_by_id(role_id=current_user.user_role)
            tokens = create_jwt_tokens(user_login=current_user.login, user_role=user_role_model.role_type)
            save_user_to_history(user=current_user)

            return {
                "message": "Logged in as {}".format(current_user.login),
                "access_token": tokens.access_token,
                "refresh_token": tokens.refresh_token,
            }, HTTPStatus.OK

        return {"message": "Wrong credentials"}, HTTPStatus.UNAUTHORIZED
