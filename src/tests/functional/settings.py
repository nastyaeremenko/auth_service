from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    app_host: str = Field('localhost', env='APP_HOST')
    app_port: str = Field('5000', env='APP_PORT')

    redis_host: str = Field('localhost', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')

    postgres_host: str = Field('localhost', env='POSTGRES_HOST')
    postgres_port: str = Field('5433', env='POSTGRES_PORT')
    postgres_user: str = Field('auth_user', env='POSTGRES_USER')
    postgres_password: str = Field('123qwe', env='POSTGRES_PASSWORD')
    postgres_db: str = Field('auth', env='POSTGRES_DB')

    api_version: str = Field('api/v1')

    superuser_login: str = Field('admin', env='SUPERUSER_LOGIN')
    superuser_password: str = Field('admin12', env='SUPERUSER_PASSWORD')
    superuser_email: str = Field('admin@example.com', env='SUPERUSER_EMAIL')

    user_test_login: str = Field('test_user')
    user_test_password: str = Field('test_user')
    user_test_email: str = Field('test_user@example.com')

    jwt_secret_key: str = Field('@EKDMSJF*@IJRFDICSAJnfWAUJQrfnajf3i8jws',
                                env='JWT_SECRET_KEY')

    jwt_access_token_expires: int = Field(3600)
    jwt_refresh_token_expires: int = Field(2592000)
    jwt_access_payload_keys: list = Field(
        ['fresh', 'iat', 'jti', 'type', 'sub', 'nbf', 'exp', 'session','roles']
    )
    jwt_refresh_payload_keys: list = Field(
        ['fresh', 'iat', 'jti', 'type', 'sub', 'nbf', 'exp', 'session']
    )
    role_test_slug: str = Field('subscriber')

    path_migration: str = Field('src/migrations', env='PATH_MIGRATION')

