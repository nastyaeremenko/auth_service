from enum import Enum

from authlib.integrations.flask_client import OAuth

oauth = OAuth()


class ProviderOauth(Enum):
    YANDEX = 'yandex'
    MAIL = 'mail'


def init_oauth(app):
    oauth.register(
        ProviderOauth.YANDEX.value,
        userinfo_endpoint=app.config['YANDEX_USERINFO_ENDPOINT']
    )
    oauth.register(
        ProviderOauth.MAIL.value,
        userinfo_endpoint=app.config['MAIL_USERINFO_ENDPOINT']
    )

    oauth.init_app(app)
