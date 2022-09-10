from typing import Any, Dict, List

from http import HTTPStatus

from api.v1.decorators import superuser_required
from api.v1.parsers import change_role_parser, create_role_parser, delete_role_parser
from db.relational.models.userrole import UserRole
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class RolesAPI(Resource):
    @jwt_required()
    @superuser_required()
    def post(self) -> tuple[dict[str, Any], int]:
        data = create_role_parser.parse_args()
        UserRole(role_type=data["role"]).save_to_db()

        return {}, HTTPStatus.CREATED

    @jwt_required()
    @superuser_required()
    def get(self) -> List[Dict[str, str]]:
        roles = UserRole.return_all()
        return roles

    @jwt_required()
    @superuser_required()
    def delete(self) -> tuple[dict[str, Any], int]:
        data = delete_role_parser.parse_args()
        UserRole.delete_by_id(data["role_id"])

        return {}, HTTPStatus.OK

    @jwt_required()
    @superuser_required()
    def put(self) -> tuple[dict[str, Any], int]:
        data = change_role_parser.parse_args()
        role = UserRole.find_by_id(role_id=data["role_id"])
        role.role_type = data["role"]
        role.save_to_db()

        return {}, HTTPStatus.OK
