from http import HTTPStatus

from api.v1.decorators import superuser_required
from api.v1.parsers import set_user_role_parser
from core.models import DefaultUserRole
from db.relational.models import User
from db.relational.models.userrole import UserRole
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class UserRoleAPI(Resource):
    @jwt_required()
    @superuser_required()
    def get(self, user_id: str) -> tuple[dict, type(HTTPStatus)]:
        """
        Get Role method for users
        ---
        tags:
          - auth
        parameters:
          - in: path
            name: user_id
            type: string
            required: true
        responses:
          200:
            description: Success get user's Role
          401:
            description: Authorization error response
          429:
            description: Too many requests. Limit in interval seconds.
        """
        user = User.find_by_id(user_id)
        user_role = UserRole.find_by_id(role_id=user.user_role)
        return {"role": user_role.role_type, "id": str(user_role.id)}, HTTPStatus.OK

    @jwt_required()
    @superuser_required()
    def delete(self, user_id: str) -> tuple[dict[str, str], int]:
        """
        delete Default Role  from user
        ---
        tags:
          - auth
        parameters:
          - in: path
            name: user_id
            type: string
            required: true
        responses:
          200:
            description: Success delete user's Role
          401:
            description: Authorization error response
          429:
            description: Too many requests. Limit in interval seconds.
        """
        user = User.find_by_id(user_id)
        user_role = UserRole.get_role(user_role_type=DefaultUserRole.USER.value)
        user.user_role = user_role.id
        user_role.save_to_db()

        return {"ok": f"{user_role} deleted"}, HTTPStatus.OK

    @jwt_required()
    @superuser_required()
    def put(self, user_id: str) -> tuple[dict[str, str], int]:
        """
        put Role method for users
        ---
        tags:
          - auth
        parameters:
          - in: path
            name: user_id
            type: string
            required: true
        responses:
          200:
            description: Success put user's Role
          401:
            description: Authorization error response
          429:
            description: Too many requests. Limit in interval seconds.
        """
        data = set_user_role_parser.parse_args()
        user = User.find_by_id(user_id)
        user_role = UserRole.find_by_id(role_id=data["role_id"])
        user.user_role = user_role.id
        user_role.save_to_db()

        return {"ok": f"set {user_role} - user role for {user}"}, HTTPStatus.OK
