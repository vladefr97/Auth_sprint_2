from typing import Any

from http import HTTPStatus

from api.extensions.block_list import get_blocklist
from api.v1.utils import create_jwt_tokens
from core.config import JWT_ACCESS_TOKEN_EXPIRES
from db.relational.models.userrole import UserRole
from flask_jwt_extended import current_user, get_jwt, jwt_required
from flask_restful import Resource

jwt_blocklist = get_blocklist()


class TokenRefreshAPI(Resource):
    @jwt_required(refresh=True)
    def post(self) -> tuple[dict[str, Any], int]:
        """
        Refresh token method for users
        ---
        tags:
          - auth
        responses:
          200:
            description: Success user's token refresh
          401:
            description: Authorization error response
          429:
            description: Too many requests. Limit in interval seconds.
        """
        jti = get_jwt()["jti"]
        jwt_blocklist.set_token(key=jti, value="", expire=JWT_ACCESS_TOKEN_EXPIRES)
        user_role_model = UserRole.find_by_id(role_id=current_user.user_role)
        tokens = create_jwt_tokens(user_login=current_user.login, user_role=user_role_model.role_type)

        return tokens.dict(), HTTPStatus.OK
