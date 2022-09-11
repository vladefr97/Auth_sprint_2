from db.relational.models.user import User
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class AllUsersAPI(Resource):
    @jwt_required()
    def get(self) -> dict[str, list[dict[str, str]]]:
        return User.return_all()

    def delete(self) -> dict[str, str]:
        return User.delete_all()
