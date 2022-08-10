from http import HTTPStatus

from flasgger import swag_from
from flask import url_for
from flask_jwt_extended import jwt_required, get_current_user
from flask_jwt_extended import verify_jwt_in_request
from flask_restful import abort, Resource
from flask_restful import reqparse

from app.api.v1.schemas import (ChangeUser, SessionSchema, UserSchema,
                                ProfileSchema, ChangeProfile,
                                RegisterUser,)
from app.api.v1.schemas import RoleSchema
from app.core.config import ROLE_NOT_FOUND, PROFILE_NOT_FOUND, SOCIAL_NOT_FOUND
from app.core.oauth import oauth
from app.docs.profile_docs import (delete_profile_role_spec, put_user_spec,
                                   put_profile_role_spec, put_profile_spec,
                                   get_profile_role_spec, get_user_access_spec,
                                   get_profile_history_spec, get_profile_spec,
                                   post_user_spec, post_social_spec,
                                   delete_social_spec)
from app.excepions import ObjectExists
from app.models import Role, Profile, SocialAuth
from app.services.user_help import (change_user, superuser_required,
                                    role_and_permission, change_profile,
                                    create_profile_user)
from app.utils.helper import validate_request

parser_role_id = reqparse.RequestParser()
parser_role_id.add_argument('role_id', type=str)
parser_social = reqparse.RequestParser()
parser_social.add_argument('social_name', type=str)


class ProfileRoleView(Resource):
    @swag_from(get_profile_role_spec)
    @superuser_required()
    def get(self, id):
        '''Получение списка ролей для профиля'''
        profile = Profile.query.get_or_404(id, PROFILE_NOT_FOUND)
        role_schema = RoleSchema(many=True)
        role_result = role_schema.dump(profile.role)
        return role_result, HTTPStatus.OK

    @swag_from(put_profile_role_spec)
    @superuser_required()
    def post(self, id):
        '''Добавление роли для профиля'''
        profile = Profile.query.get_or_404(id, PROFILE_NOT_FOUND)
        args = parser_role_id.parse_args()
        role = Role.query.get_or_404(args.get('role_id'), ROLE_NOT_FOUND)
        profile.role.append(role)
        try:
            profile.save()
        except ObjectExists as e:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors=str(e))
        role_schema = RoleSchema(many=True)
        role_result = role_schema.dump(profile.role)
        return role_result, HTTPStatus.CREATED

    @swag_from(delete_profile_role_spec)
    @superuser_required()
    def delete(self, id):
        '''Удаление роли для профиля'''
        profile = Profile.query.get_or_404(id, PROFILE_NOT_FOUND)
        args = parser_role_id.parse_args()
        role = Role.query.get_or_404(args.get('role_id'), ROLE_NOT_FOUND)
        try:
            profile.role.remove(role)
        except ValueError:
            pass
        else:
            profile.save()
        role_schema = RoleSchema(many=True)
        role_result = role_schema.dump(profile.role)
        return role_result, HTTPStatus.OK


class ProfileAccessView(Resource):
    @swag_from(get_user_access_spec)
    @jwt_required()
    def get(self):
        '''Получение всех прав профиля по токену'''
        _, jwt_data = verify_jwt_in_request()
        jwt_roles = jwt_data.get('roles')
        roles, permissions = role_and_permission(jwt_roles)
        return {'roles': roles, 'permissions': permissions}, HTTPStatus.OK


class ProfileView(Resource):
    @jwt_required()
    @swag_from(put_profile_spec)
    def put(self):
        '''Изменение данных профиля'''
        profile_validate = ChangeProfile()
        profile_in = validate_request(profile_validate)
        profile = change_profile(profile_in)
        profile_schema = ProfileSchema()
        profile_result = profile_schema.dump(profile)
        return profile_result, HTTPStatus.OK

    @jwt_required()
    @swag_from(get_profile_spec)
    def get(self):
        '''Текущие данные профиля'''
        profile = get_current_user()
        profile_schema = ProfileSchema()
        profile_result = profile_schema.dump(profile)
        return profile_result, HTTPStatus.OK


class ProfileUserView(Resource):
    @jwt_required()
    @swag_from(put_user_spec)
    def put(self):
        '''Изменение данных пользователя'''
        user_validate = ChangeUser()
        user_in = validate_request(user_validate)
        user = change_user(user_in)
        user_schema = UserSchema()
        user_result = user_schema.dump(user)
        return user_result, HTTPStatus.OK

    @jwt_required()
    @swag_from(post_user_spec)
    def post(self):
        '''Добавление локального пользователя к профилю'''
        user_validate = RegisterUser()
        user_in = validate_request(user_validate)
        create_profile_user(user_in)
        return {'result': 'ok'}, HTTPStatus.CREATED


class ProfileLoginHistoryView(Resource):
    @jwt_required()
    @swag_from(get_profile_history_spec)
    def get(self):
        '''История входа профиля'''
        profile = get_current_user()
        if not profile:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors='Login for watching login history.')
        session = profile.session
        session_schema = SessionSchema(many=True)
        session_result = session_schema.dump(session)
        return session_result, HTTPStatus.OK


class ProfileSocialAuthView(Resource):
    @jwt_required()
    @swag_from(post_social_spec)
    def post(self):
        '''Добавление социальной сети к профилю'''
        args = parser_social.parse_args()
        social_name = args.get('social_name')
        client = oauth.create_client(social_name)
        if not client:
            return {'error': 'This site doesn`t allow you to '
                             'connect to the specified '
                             'social networks'}, HTTPStatus.NOT_FOUND
        redirect_uri = url_for('api.authorize', _external=True,
                               social_name=social_name)
        profile = get_current_user()
        return client.authorize_redirect(redirect_uri, state=profile.id)


class ProfileSocialDeleteView(Resource):
    @jwt_required()
    @swag_from(delete_social_spec)
    def delete(self, id):
        '''Удаление социальной сети у профиля'''
        profile = get_current_user()
        social = SocialAuth.query.get_or_404(id, SOCIAL_NOT_FOUND)
        if social not in profile.social_auth:
            abort(HTTPStatus.NOT_FOUND,
                  errors=SOCIAL_NOT_FOUND)
        socials_count = len(profile.social_auth)
        if not (profile.user or socials_count > 1):
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors='You can`t remove single login source of a profile.')
        try:
            profile.social_auth.remove(social)
            social.delete()
        except ValueError:
            pass
        else:
            profile.save()
        return '', HTTPStatus.NO_CONTENT
