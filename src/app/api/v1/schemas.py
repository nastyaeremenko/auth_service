from marshmallow import Schema, fields
from marshmallow.validate import Length
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.core.db import db
from app.models import (Role, Permission, Session,
                        User, Profile, SocialAuth)


class RegisterUser(Schema):
    login = fields.String(required=True, validate=Length(min=3))
    password = fields.String(required=True, validate=Length(min=6))
    g_recaptcha_response = fields.String(required=True)


class LoginUser(Schema):
    login = fields.String(required=True, validate=Length(min=3))
    password = fields.String(required=True, validate=Length(min=6))


class ChangeUser(Schema):
    login = fields.String(validate=Length(min=3))
    password = fields.String(validate=Length(min=6))
    old_password = fields.String()


class ChangeProfile(Schema):
    name = fields.String(validate=Length(min=3))
    email = fields.Email()


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Role
        sqla_session = db.session
        load_instance = True


class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Permission
        sqla_session = db.session
        load_instance = True


class SessionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Session
        sqla_session = db.session
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ('password',)


class SocialAuthSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = SocialAuth
        sqla_session = db.session
        load_instance = True


class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Profile
        sqla_session = db.session
        load_instance = True
    user = fields.Nested(UserSchema)
    social_auth = fields.Nested(SocialAuthSchema, many=True)
