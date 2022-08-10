from http import HTTPStatus

import jwt
import pytest

from tests.functional.conftest import settings


@pytest.mark.parametrize(
    (
            'body', 'status', 'message'
    ),
    (
            ({}, HTTPStatus.BAD_REQUEST, {
                'errors': {'login': ['Missing data for required field.'],
                           'password': ['Missing data for required field.']}}),
            ({'login': 'ds', 'password': 'ds'},
             HTTPStatus.BAD_REQUEST, {
                 'errors': {'login': ['Shorter than minimum length 3.'],
                            'password': ['Shorter than minimum length 6.']}}),
            ({'login': settings.user_test_login,
              'password': settings.user_test_password},
             HTTPStatus.CREATED, {'result': 'ok'}),
    )
)
def test_register(make_fetch_request, body, status, message, clear_postgres):
    request = make_fetch_request('POST', '/register', body=body)
    assert request.status == status
    assert request.body == message


@pytest.mark.parametrize(
    (
            'body', 'status', 'response'
    ),
    (

            (
                    {
                        'login': settings.user_test_login
                    },
                    HTTPStatus.BAD_REQUEST,
                    ['errors']
            ),
            (
                    {
                        'password': settings.user_test_password,
                        'login': settings.user_test_login
                    },
                    HTTPStatus.OK,
                    ['access_token', 'refresh_token']
            ),

    )

)
def test_login(make_fetch_request, clear_postgres, body, status, response):
    request = make_fetch_request('POST', '/login', body=body)
    assert request.status == status
    assert list(request.body) == response


def test_check_access_token(make_fetch_request, clear_postgres):
    body = {
        'password': settings.user_test_password,
        'login': settings.user_test_login
    }
    request = make_fetch_request('POST', '/login', body=body)
    assert request.status == HTTPStatus.OK
    access_token = request.body.get('access_token')

    payload = jwt.decode(
        access_token,
        key=settings.jwt_secret_key,
        algorithms=['HS256', ]
    )
    assert settings.jwt_access_payload_keys == list(payload)
    expires = payload.get('exp') - payload.get('nbf')
    assert expires == settings.jwt_access_token_expires


def test_check_refresh_token(make_fetch_request, clear_postgres):
    body = {
        'password': settings.user_test_password,
        'login': settings.user_test_login
    }
    request = make_fetch_request('POST', '/login', body=body)
    assert request.status == HTTPStatus.OK
    refresh_token = request.body.get('refresh_token')

    payload = jwt.decode(
        refresh_token,
        key=settings.jwt_secret_key,
        algorithms=['HS256', ]
    )
    assert settings.jwt_refresh_payload_keys == list(payload)
    expires = payload.get('exp') - payload.get('nbf')
    assert expires == settings.jwt_refresh_token_expires


def test_refresh(make_fetch_request, clear_postgres):
    body = {
        'password': settings.user_test_password,
        'login': settings.user_test_login
    }
    request = make_fetch_request('POST', '/login', body=body)
    assert request.status == HTTPStatus.OK
    refresh_token = request.body.get('refresh_token')
    refresh_body = {
        'r_token': refresh_token
    }
    response_refresh = make_fetch_request('POST', '/refresh',
                                          body=refresh_body)
    assert response_refresh.status == HTTPStatus.OK
    response_refresh = make_fetch_request('POST', '/refresh',
                                          body=refresh_body)
    assert response_refresh.status == HTTPStatus.UNAUTHORIZED


def test_logout(make_fetch_request, clear_postgres):
    body = {
        'password': settings.user_test_password,
        'login': settings.user_test_login
    }
    request = make_fetch_request('POST', '/login', body=body)
    assert request.status == HTTPStatus.OK
    access_token = request.body.get('access_token')
    refresh_token = request.body.get('refresh_token')
    refresh_body = {
        'r_token': refresh_token
    }
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    request_logout = make_fetch_request('POST', '/logout', headers=headers)
    assert request_logout.status == HTTPStatus.OK
    response_refresh = make_fetch_request('POST', '/refresh',
                                          body=refresh_body)
    assert response_refresh.status == HTTPStatus.UNAUTHORIZED
