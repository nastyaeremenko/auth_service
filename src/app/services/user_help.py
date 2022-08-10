from functools import wraps
from http import HTTPStatus
from uuid import uuid4, UUID

from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_current_user, get_jwt,
                                verify_jwt_in_request)
from flask_restful import abort

from app.core.config import (REFRESH_TOKEN_EXPIRES, ROLES_EXPIRES,
                             SUPERUSER_ROLE, PROFILE_NOT_FOUND)
from app.core.db import redis_db, jwt_redis_blocklist
from app.excepions import TokenInvalid, ObjectExists
from app.models import User, Session, Role, Profile, SocialAuth
from app.services.tracer_help import tracer_help


def check_and_create_user(user_in: dict, profile: Profile = None):
    user = User(login=user_in['login'])
    user.set_password(user_in['password'])
    if not profile:
        profile = Profile().save()
    user.profile_id = profile.id
    try:
        user.save()
    except ObjectExists as e:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors=str(e))


def change_user(user_in: dict):
    profile = get_current_user()
    if not profile:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors='Login for make changes.')
    user = profile.user
    if not user:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors='Create local user before change.')
    user.login = user_in.get('login') or user.login
    if user_in.get('password'):
        if not user_in.get('old_password'):
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors='To change password, enter your old password.')
        if not user.check_password(user_in.get('old_password')):
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors='Incorrect old password.')
        user.set_password(user_in['password'])
    try:
        user.save()
    except ObjectExists as e:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors=str(e))
    return user


def change_profile(profile_in: dict):
    profile = get_current_user()
    if not profile:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors='Login for make changes.')
    profile.email = profile_in.get('email') or profile.email
    profile.name = profile_in.get('name') or profile.name
    try:
        profile.save()
    except ObjectExists as e:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors=str(e))
    return profile


def generate_tokens(profile: Profile, session_id: UUID, fresh=False):
    refresh_jti = str(uuid4())
    roles_db = profile.role
    roles = [role.slug for role in roles_db]
    additional_claims_base = {'session': session_id}
    additional_claims_access = {**additional_claims_base, 'roles': roles}
    additional_claims_refresh = {**additional_claims_base, 'jti': refresh_jti}
    access_token = create_access_token(
        identity=profile.id,
        fresh=fresh,
        additional_claims=additional_claims_access
    )
    refresh_token = create_refresh_token(
        identity=profile.id,
        additional_claims=additional_claims_refresh
    )
    expires = int(REFRESH_TOKEN_EXPIRES.total_seconds())
    redis_db.setex(str(session_id), expires, refresh_jti)

    return access_token, refresh_token


@tracer_help
def login_user(user_in: dict):
    user = User.query.filter(User.login == user_in['login']).one_or_none()
    if user is None or not user.check_password(user_in['password']):
        abort(HTTPStatus.UNAUTHORIZED,
              errors='Login or Password not correct')
    user_agent = request.headers.get('User-Agent')

    session = Session(agent=user_agent, profile=user.profile,
                      login_type='local')
    session.save()
    return generate_tokens(user.profile, session.id, fresh=True)


def logout_user():
    token = get_jwt()
    session_id = token['session']
    refresh_token = redis_db.get(session_id)
    if not refresh_token:
        raise TokenInvalid('you are already logout')
    jwt_redis_blocklist.set(refresh_token,
                            int(REFRESH_TOKEN_EXPIRES.total_seconds()))
    redis_db.delete(session_id)


def refresh_token_process():
    old_token = get_jwt()
    session_id = old_token['session']
    refresh_jti = old_token['jti']

    user = get_current_user()

    validate_token(session_id, refresh_jti)

    access_token, refresh_token = generate_tokens(user, old_token['session'])
    jwt_redis_blocklist.set(refresh_jti,
                            int(REFRESH_TOKEN_EXPIRES.total_seconds()))
    return access_token, refresh_token


def validate_token(session_id, jti):
    refresh_jti = jwt_redis_blocklist.get(jti)
    if refresh_jti:
        raise TokenInvalid('refresh token is black list')

    session_token = redis_db.get(session_id)
    if not session_token or session_token != jti:
        raise TokenInvalid('token session is not correct')


def role_and_permission(roles):
    default_value = 'None'
    roles_result = []
    all_permissions = set()
    for role in roles:
        permissions_raw = redis_db.get(role)
        if not permissions_raw:
            roles_db = Role.query.filter_by(slug=role).one_or_none()
            if roles_db is None:
                continue
            role_permission = roles_db.permission
            permissions_raw = ','.join(
                perm.slug for perm in role_permission if perm
            )
            redis_db.setex(
                role,
                ROLES_EXPIRES,
                permissions_raw or default_value
            )
        permissions = permissions_raw.split(',')
        if default_value in permissions:
            permissions.remove(default_value)
        all_permissions |= set(permissions)
        roles_result.append(role)
    return roles_result, list(all_permissions)


def superuser_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            token = get_jwt()
            if SUPERUSER_ROLE in token['roles']:
                return fn(*args, **kwargs)
            else:
                abort(HTTPStatus.FORBIDDEN,
                      errors='This action is only available for superuser.')

        return decorator

    return wrapper


def save_social_auth(social_user_id, social_name,
                     profile, create=False):
    data = {
        'social_user_id': social_user_id,
        'social_name': social_name
    }
    if create and SocialAuth.query.filter_by(**data).first():
        return
    social_auth = SocialAuth(**data)
    social_auth.profile_id = profile.id
    try:
        social_auth.save()
    except ObjectExists as e:
        if create:
            profile.delete()
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors=str(e))


def create_auth_social(social_user_id, social_name):
    profile = Profile().save()
    save_social_auth(social_user_id, social_name, profile, True)

    user_agent = request.headers.get('User-Agent')
    session = Session(agent=user_agent, profile=profile,
                      login_type=social_name)
    session.save()
    return generate_tokens(profile, session.id, fresh=True)


def add_auth_social(social_user_id, social_name, profile):
    profile_social_names = tuple(
        social.social_name for social in profile.social_auth)
    if social_name in profile_social_names:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors='This social network is already attached.')
    save_social_auth(social_user_id, social_name, profile)


def create_profile_user(user_in: dict):
    profile = get_current_user()
    if not profile:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors='Login for make changes.')
    if profile.user:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY,
              errors='Profile can only have one local user.')
    check_and_create_user(user_in, profile)


def get_profile(id):
    if id:
        try:
            id = UUID(id)
        except ValueError:
            return None
        return Profile.query.get_or_404(id, PROFILE_NOT_FOUND)
    return None
