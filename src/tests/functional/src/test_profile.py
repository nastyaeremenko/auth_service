from http import HTTPStatus
from uuid import uuid4

import pytest

URL = '/profile'


@pytest.mark.parametrize(
    (
            'body', 'status'
    ),
    (

            (
                    {
                        'name': 'Александр',
                        'email': 'test@test.ru'
                    },
                    HTTPStatus.OK
            ),
            (
                    {
                        'email': 'test@test.ru'
                    },
                    HTTPStatus.OK
            ),
            (
                    {
                        'name': 'Alex',
                        'email': 'alex@test.ru'
                    },
                    HTTPStatus.OK
            ),
            (
                    {
                        'email': 'test.ru'
                    },
                    HTTPStatus.BAD_REQUEST
            ),

    )

)
def test_put_get_profile(make_fetch_request, login_test_user,
                         clear_postgres, body, status):
    access_token = login_test_user.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    request = make_fetch_request('PUT', URL,
                                 headers=headers, body=body)
    assert request.status == status
    if request.status == HTTPStatus.OK:
        request_get = make_fetch_request('GET', URL,
                                         headers=headers)
        for k in body.keys():
            assert request_get.body[k] == body[k]


@pytest.mark.parametrize(
    (
            'body', 'status'
    ),
    (

            (
                    {
                        'login': 'test',
                    },
                    HTTPStatus.OK
            ),
            (
                    {
                        'password': 'test12345',
                        'old_password': 'test_user'
                    },
                    HTTPStatus.OK
            ),
            (
                    {
                        'login': 'test_user',
                        'password': 'test_user',
                        'old_password': 'test12345'
                    },
                    HTTPStatus.OK
            ),
            (
                    {
                        'login': '12'
                    },
                    HTTPStatus.BAD_REQUEST
            ),
            (
                    {
                        'login': 'admin'
                    },
                    HTTPStatus.UNPROCESSABLE_ENTITY
            ),
            (
                    {
                        'password': 'test1ru'
                    },
                    HTTPStatus.UNPROCESSABLE_ENTITY
            ),

    )

)
def test_put_profile_user(make_fetch_request, login_test_user,
                          create_superuser, clear_postgres,
                          body, status):
    access_token = login_test_user.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    request = make_fetch_request('PUT', f'{URL}/user',
                                 headers=headers, body=body)
    assert request.status == status
