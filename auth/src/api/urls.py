from api.v1.resources.auth import (
    TokenRefreshAPI,
    UserLoginAPI,
    UserLoginChangeAPI,
    UserLogoutAccessAPI,
    UserPasswordChangeAPI,
    UserRegistrationAPI,
)
from api.v1.resources.roles.roles import RolesAPI
from api.v1.resources.users import AllUsersAPI, UserAllHistoryAPI
from api.v1.resources.users.user_role import UserRoleAPI
from flask_restful import Resource

V1_PREFIX = "/api/v1"
urls: list[tuple[type(Resource), str]] = [
    (UserRegistrationAPI, V1_PREFIX + "/registration"),
    (UserLoginAPI, V1_PREFIX + "/login"),
    (UserLogoutAccessAPI, V1_PREFIX + "/logout"),
    (TokenRefreshAPI, V1_PREFIX + "/token/refresh"),
    (AllUsersAPI, V1_PREFIX + "/users"),
    (UserAllHistoryAPI, V1_PREFIX + "/user/history"),
    (UserPasswordChangeAPI, V1_PREFIX + "/password/change"),
    (UserLoginChangeAPI, V1_PREFIX + "/login/change"),
    (RolesAPI, V1_PREFIX + "/roles"),
    (UserRoleAPI, V1_PREFIX + "/user/<string:user_id>/role"),
]
