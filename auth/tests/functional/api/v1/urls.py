# TODO: вынести host в конфиг
HOST = "http://127.0.0.1:5000"
V1_PREFIX = "/api/v1"

V1_API = HOST + V1_PREFIX

REGISTRATION_URL = V1_API + "/registration"
LOGIN_URL = V1_API + "/login"
LOGOUT_URL = V1_API + "/logout"
TOKEN_REFRESH_URL = V1_API + "/token/refresh"
USERS_LIST_URL = V1_API + "/users"
USERS_HISTORY_URL = V1_API + "/users/history"
PASSWORD_CHANGE_URL = V1_API + "/password/change"
LOGIN_CHANGE_URL = V1_API + "/login/change"
ROLES_URL = V1_API + "/roles"
USER_ROLES_URL = V1_API + "/user/<string:user_id>/role"
