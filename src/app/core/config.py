import os
from datetime import timedelta
from logging import config as logging_config

from dotenv import load_dotenv

from app.core.logger import LOGGING
from app.docs.definitions import definitions_spec

load_dotenv()
# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', os.getenv('PROJECT_NAME'))

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', os.getenv('REDIS_HOST'))
REDIS_PORT = os.getenv('REDIS_PORT', os.getenv('REDIS_PORT'))

# Настройки Postgres
POSTGRES_HOST = os.getenv('POSTGRES_HOST', os.getenv('POSTGRES_HOST'))
POSTGRES_PORT = os.getenv('POSTGRES_PORT', os.getenv('POSTGRES_PORT'))
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

REFRESH_TOKEN_EXPIRES = timedelta(days=30)
ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PERMISSION_NOT_FOUND = 'Permission not found'
ROLE_NOT_FOUND = 'Role not found'
USER_NOT_FOUND = 'User not found'
PROFILE_NOT_FOUND = 'Profile not found'
SOCIAL_NOT_FOUND = 'Social network not found'

ROLES_EXPIRES = 300

SUPERUSER_ROLE = 'superuser'

# reCapcha
RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')


class Config:
    """Установка переменных конфигурации Flask"""
    # Database
    SQLALCHEMY_DATABASE_URI = (f'postgresql://{POSTGRES_USER}:'
                               f'{POSTGRES_PASSWORD}@{POSTGRES_HOST}:'
                               f'{POSTGRES_PORT}/'
                               f'{POSTGRES_DB}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # config JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret')
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_TOKEN_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_TOKEN_EXPIRES
    JWT_TOKEN_LOCATION = ('headers', 'query_string', 'json')
    JWT_REFRESH_JSON_KEY = 'r_token'
    JWT_QUERY_STRING_NAME = 'r_token'
    JWT_REFRESH_COOKIE_NAME = 'r_token'

    PATH_MIGRATION = os.getenv('migrations', os.getenv('PATH_MIGRATION'))

    JAEGER_TRACE = 'auth_jaeger'
    JAEGER_PORT = 6831

    # swagger
    SWAGGER_TEMPLATE = {
        'swagger': "2.0",
        'info': {
            'description': 'sdsds',
            'version': '1.0.0',
            'title': 'Auth Server',

        },
        'schemes': ['http', 'https'],
        'securityDefinitions': {
            'api_key': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
        },
        'definitions': definitions_spec
    }

    # OAUTH Yandex
    YANDEX_CLIENT_ID = os.getenv('YANDEX_CLIENT_ID')
    YANDEX_CLIENT_SECRET = os.getenv('YANDEX_CLIENT_SECRET')
    YANDEX_AUTHORIZE_URL = os.getenv('YANDEX_AUTHORIZE_URL')
    YANDEX_API_BASE_URL = os.getenv('YANDEX_API_BASE_URL')
    YANDEX_ACCESS_TOKEN_URL = os.getenv('YANDEX_ACCESS_TOKEN_URL')
    YANDEX_USERINFO_ENDPOINT = os.getenv('YANDEX_USERINFO_ENDPOINT')

    # OAUTH Mail
    MAIL_CLIENT_ID = os.getenv('MAIL_CLIENT_ID')
    MAIL_CLIENT_SECRET = os.getenv('MAIL_CLIENT_SECRET')
    MAIL_AUTHORIZE_URL = os.getenv('MAIL_AUTHORIZE_URL')
    MAIL_API_BASE_URL = os.getenv('MAIL_API_BASE_URL')
    MAIL_ACCESS_TOKEN_URL = os.getenv('MAIL_ACCESS_TOKEN_URL')
    MAIL_USERINFO_ENDPOINT = os.getenv('MAIL_USERINFO_ENDPOINT')
