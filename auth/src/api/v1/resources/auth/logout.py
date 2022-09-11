from http import HTTPStatus

from api.extensions.block_list import get_blocklist
from core.config import JWT_ACCESS_TOKEN_EXPIRES
from flask_jwt_extended import get_jwt, jwt_required
from flask_restful import Resource

block_list = get_blocklist()

# TODO: передать эту на стройку в создание JWT токенов


class UserLogoutAccessAPI(Resource):
    @jwt_required()
    def post(self) -> tuple[dict, type(HTTPStatus)]:
        """
        Logout access token method for users
        ---
        tags:
          - auth
        responses:
          200:
            description: Success user's logout access token
          401:
            description: Authorization error response
          429:
            description: Too many requests. Limit in interval seconds
        """

        jti = get_jwt()["jti"]
        block_list.set_token(key=jti, expire=JWT_ACCESS_TOKEN_EXPIRES, value="")
        return {"message": "User logout"}, HTTPStatus.OK
