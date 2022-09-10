from flask_restful import reqparse

# Auth API
auth_parser = reqparse.RequestParser()
auth_parser.add_argument("login", help="This field cannot be blank", required=True)
auth_parser.add_argument("password", help="This field cannot be blank", required=True)

# Registration API
registration_parser = reqparse.RequestParser()
registration_parser.add_argument("login", help="This field cannot be blank", required=True)
registration_parser.add_argument("password", help="This field cannot be blank", required=True)
registration_parser.add_argument("email", help="This field cannot be blank", required=True)

# Roles API
create_role_parser = reqparse.RequestParser()
create_role_parser.add_argument("role", help="This field cannot be blank", required=True)

delete_role_parser = reqparse.RequestParser()
delete_role_parser.add_argument("role_id", help="This field cannot be blank", required=True)

change_role_parser = reqparse.RequestParser()
change_role_parser.add_argument("role_id", help="This field cannot be blank", required=True)
change_role_parser.add_argument("role", help="This field cannot be blank", required=True)

# User Roles API
set_user_role_parser = reqparse.RequestParser()
set_user_role_parser.add_argument("role_id", help="This field cannot be blank", required=True)
