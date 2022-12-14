from api.extensions.block_list import get_blocklist
from db.relational.models.user import User
from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()
jwt_redis_block_list = get_blocklist()


def init_jwt(app: Flask) -> None:
    jwt.init_app(app)


# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(_: any, jwt_payload: dict[str, str]) -> bool:
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_block_list.get(jti)
    return token_in_redis is not None


@jwt.user_lookup_loader
def _user_lookup_callback(_: any, jwt_data: dict[str, any]) -> type(User):
    identity = jwt_data["sub"]
    return User.find_by_login(identity)
