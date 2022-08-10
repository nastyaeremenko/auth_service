from flask_jwt_extended import JWTManager

from app.models import Profile

jwt = JWTManager()


# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Profile.query.filter_by(id=identity).one_or_none()


def init_jwt(app):
    jwt.init_app(app)
