from dataclasses import dataclass
from typing import Optional

import pytest
import redis
import requests
from flask import Flask
from multidict import CIMultiDictProxy
from sqlalchemy import create_engine

from tests.functional.settings import TestSettings

settings = TestSettings()
from app.core.config import SUPERUSER_ROLE, Config
from app.core.db import init_db
# from app.main import app
from app.models import User, Role, Profile

API_URL = 'http://{}:{}/{}'.format(settings.app_host, settings.app_port,
                                   settings.api_version)


@pytest.fixture(scope="session")
def init_app():
    Config.SQLALCHEMY_DATABASE_URI = (f'postgresql://{settings.postgres_user}:'
                                      f'{settings.postgres_password}@{settings.postgres_host}:'
                                      f'{settings.postgres_port}/'
                                      f'{settings.postgres_db}')
    Config.PATH_MIGRATION = settings.path_migration
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)


@pytest.fixture(scope="session")
def redis_db():
    redis_db0 = redis.Redis(
        host=settings.redis_host, port=settings.redis_port, db=0,
        decode_responses=True
    )
    yield redis_db0
    redis_db0.close()


@pytest.fixture(scope="session")
def postgres_client():
    str_conn = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        settings.postgres_user,
        settings.postgres_password,
        settings.postgres_host,
        settings.postgres_port,
        settings.postgres_db,
    )
    engine = create_engine(str_conn)
    db = engine.connect()
    yield db
    db.close()


@pytest.fixture(scope="module")
def clear_postgres(postgres_client):
    yield
    tables = ['profile', 'role', 'permission']
    for table in tables:
        postgres_client.execute('truncate table {} cascade'.format(table))


@pytest.fixture(scope="session")
def redis_blocklist():
    redis_db1 = redis.Redis(
        host=settings.redis_host, port=settings.redis_port, db=1,
        decode_responses=True
    )
    yield redis_db1
    redis_db1.close()


@pytest.fixture
def session():
    session = requests.session()
    yield session
    session.close()


@pytest.fixture(scope="session")
def redis_flush(redis_db, redis_blocklist):
    redis_db.flushall()
    redis_blocklist.flushall()
    yield


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
def make_fetch_request():
    def inner(method: str, route,
              params: Optional[dict] = None,
              body: Optional[dict] = None,
              headers: Optional[dict] = None) -> HTTPResponse:
        params = params or "{}"
        body = body or {}
        headers = headers or {}
        url = '{}{}'.format(API_URL, route)
        methods = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'delete': requests.delete,
        }

        response = methods[method.lower()](url, params=params, json=body,
                                           headers=headers, timeout=10)

        response_body = ''
        try:
            response_body = response.json()
        except:
            pass

        return HTTPResponse(
            body=response_body,
            headers=response.headers,
            status=response.status_code,
        )

    return inner


@pytest.fixture(scope="module")
def create_superuser(init_app):
    user = User(login=settings.superuser_login)
    user.set_password(settings.superuser_password)
    superuser_role = Role.query.filter_by(slug=SUPERUSER_ROLE).first()
    if not superuser_role:
        superuser_role = Role(slug=SUPERUSER_ROLE)
        superuser_role.save()
    profile = Profile()
    profile.role.append(superuser_role)
    profile.save()
    user.profile_id = profile.id
    user.save()
    yield user


@pytest.fixture(scope="module")
def create_test_user(init_app):
    user = User(login=settings.user_test_login)
    user.set_password(settings.user_test_password)
    profile = Profile().save()
    user.profile_id = profile.id
    user.save()
    yield user


@pytest.fixture(scope="module")
def login_superuser(create_superuser):
    body = {
        'password': settings.superuser_password,
        'login': settings.superuser_login
    }
    url = '{}{}'.format(API_URL, '/login')
    response = requests.post(url, json=body, timeout=10)
    return response


@pytest.fixture(scope="module")
def login_test_user(create_test_user):
    body = {
        'password': settings.user_test_password,
        'login': settings.user_test_login
    }
    url = '{}{}'.format(API_URL, '/login')
    response = requests.post(url, json=body, timeout=10)
    return response
