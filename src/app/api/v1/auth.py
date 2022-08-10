from http import HTTPStatus

from flasgger import swag_from
from flask import url_for, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from app.api.v1.schemas import RegisterUser, LoginUser
from app.core import config
from app.core.check_capctha import check_recaptcha
from app.core.oauth import oauth
from app.docs.auth_docs import (spec_login, spec_register,
                                spec_refresh, spec_logout,
                                spec_login_social, spec_authorize_social)
from app.excepions import TokenInvalid
from app.services.user_help import (check_and_create_user, login_user,
                                    refresh_token_process, logout_user,
                                    create_auth_social, add_auth_social,
                                    get_profile)
from app.utils.helper import validate_request
from app.core.limiter_conf import limiter_login

parser = reqparse.RequestParser()
parser.add_argument('login', type=str)
RECAPTCHA_PUBLIC_KEY = config.RECAPTCHA_SITE_KEY
RECAPTCHA_PRIVATE_KEY = config.RECAPTCHA_SECRET_KEY


class SignupView(Resource):
    @swag_from(spec_register)
    def post(self):
        '''Регистрация нового пользователя'''
        user_validate = RegisterUser()
        user_in = validate_request(user_validate)
        if not check_recaptcha(user_in['g_recaptcha_response'],
                               RECAPTCHA_PRIVATE_KEY):
            return {'msg': str('Invalid captcha.')}, HTTPStatus.BAD_REQUEST
        check_and_create_user(user_in)
        return {'result': 'ok'}, HTTPStatus.CREATED


class LoginView(Resource):
    @limiter_login.limit(duration=10, limit=1)
    @swag_from(spec_login)
    def post(self):
        '''Аутентификация пользователя'''
        user_validate = LoginUser()
        user_in = validate_request(user_validate)
        access_token, refresh_token = login_user(user_in)
        return {'access_token': access_token, 'refresh_token': refresh_token}


class LogoutView(Resource):
    '''Выход'''

    @swag_from(spec_logout)
    @jwt_required()
    def post(self):
        try:
            logout_user()
        except TokenInvalid as err:
            return {'msg': str(err)}, HTTPStatus.UNAUTHORIZED
        return {'result': 'logout success'}, HTTPStatus.OK


class RefreshView(Resource):
    @jwt_required(refresh=True)
    @swag_from(spec_refresh)
    def post(self):
        '''Обновление access-токена по refresh-токену'''
        try:
            access_token, refresh_token = refresh_token_process()
        except TokenInvalid as err:
            return {'error': str(err)}, HTTPStatus.UNAUTHORIZED
        return {'access_token': access_token, 'refresh_token': refresh_token}


class LoginSocialView(Resource):
    @swag_from(spec_login_social)
    def get(self, social_name):
        '''Авторизация в соцсети'''
        client = oauth.create_client(social_name)
        if not client:
            return {'error': 'This site doesn`t allow you to '
                             'connect to the specified '
                             'social networks'}, HTTPStatus.NOT_FOUND
        redirect_uri = url_for('api.authorize', _external=True,
                               social_name=social_name)
        return client.authorize_redirect(redirect_uri)


class AuthorizeSocialView(Resource):
    @swag_from(spec_authorize_social)
    def get(self, social_name):
        '''Создание профиля после успешной авторизации в соцсети'''
        social_function = getattr(oauth, social_name)

        # проверка, на тот случай, если мы пытаемся привязать
        # соц сеть к имеющемуся профилю, его id передаётся через state
        profile_id = request.args.get('state')
        profile = get_profile(profile_id)

        social_response = social_function.authorize_access_token()
        params = {'access_token': social_response['access_token']}
        user_info = social_function.userinfo(params=params)
        if 'error' in user_info:
            return (
                f'{user_info["error"]}: {user_info["description"]}',
                HTTPStatus.BAD_REQUEST
            )
        social_user_id = user_info['id']

        if profile:
            add_auth_social(social_user_id, social_name, profile)
            return {'result': 'ok'}, HTTPStatus.OK

        access_token, refresh_token = create_auth_social(
            social_user_id, social_name
        )
        result = {'access_token': access_token, 'refresh_token': refresh_token}
        return result, HTTPStatus.CREATED
