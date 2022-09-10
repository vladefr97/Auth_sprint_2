from api.v1.entities.tokens import JWTTokens
from db.relational.models import User, UserHistory
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token


def create_jwt_tokens(user_login: str, user_role: str) -> JWTTokens:
    access_token = create_access_token(identity=user_login, additional_claims={"role": user_role})
    refresh_token = create_refresh_token(identity=user_login, additional_claims={"role": user_role})
    return JWTTokens(access_token=access_token, refresh_token=refresh_token)


def save_user_to_history(user: User) -> None:
    UserHistory(
        user_id=user.id,
        user_agent=request.user_agent.string,
        ip_address=request.remote_addr,
        url=request.host + request.path,
    ).save_to_db()
