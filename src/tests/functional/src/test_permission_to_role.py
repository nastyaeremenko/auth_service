from http import HTTPStatus
from uuid import uuid4, UUID

import pytest

URL = '/role/<uuid:id>/permission'
TEST_URL = f'/role/{uuid4()}/permission'


@pytest.mark.parametrize(
    (
            'body', 'method'
    ),
    (

            (
                    {'slug': 'pretty'},
                    'POST',
            ),
            (
                    {},
                    'GET',
            ),
            (
                    {},
                    'DELETE',
            ),

    )

)
def test_permission_to_role_unauthorized(
        make_fetch_request, clear_postgres, body, method
):
    request = make_fetch_request(method, TEST_URL, body=body)
    assert request.status == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    (
            'body', 'method'
    ),
    (

            (
                    {'slug': 'pretty'},
                    'POST',
            ),
            (
                    {},
                    'GET',
            ),
            (
                    {},
                    'DELETE',
            ),

    )

)
def test_permission_to_role_test_user(
        make_fetch_request, login_test_user, clear_postgres,
        body, method
):
    access_token = login_test_user.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    request = make_fetch_request(method, TEST_URL, body=body,
                                 headers=headers)
    assert request.status == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    (
            'body', 'method'
    ),
    (

            (
                    {'permission_id': str(uuid4())},
                    'POST',
            ),
            (
                    {},
                    'GET',
            ),
            (
                    {'permission_id': str(uuid4())},
                    'DELETE',
            ),

    )

)
def test_error_permission_to_role_superuser(
        make_fetch_request, login_superuser, clear_postgres,
        body, method
):
    access_token = login_superuser.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}

    request_get = make_fetch_request(method, TEST_URL,
                                     headers=headers, body=body)
    assert request_get.status == HTTPStatus.NOT_FOUND


def test_permission_to_role_superuser(
        make_fetch_request, login_superuser, clear_postgres
):
    body = {'slug': 'test', 'description': None}
    access_token = login_superuser.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    request_role = make_fetch_request('POST', '/role',
                                      body=body, headers=headers)
    assert request_role.status == HTTPStatus.CREATED
    role_id = request_role.body['id']

    request_permission = make_fetch_request('POST', '/permission',
                                            body=body, headers=headers)
    assert request_permission.status == HTTPStatus.CREATED
    permission_id = request_permission.body['id']

    url = f'/role/{role_id}/permission'

    request_get = make_fetch_request('GET', url, headers=headers)
    assert request_get.status == HTTPStatus.OK
    assert len(request_get.body) == 0
    body_post = {'permission_id': permission_id}

    request_post = make_fetch_request('POST', url,
                                      headers=headers, body=body_post)
    assert request_post.status == HTTPStatus.CREATED
    assert len(request_post.body) == 1

    request_delete = make_fetch_request('DELETE', url,
                                        headers=headers, body=body_post)
    assert request_delete.status == HTTPStatus.OK
    assert len(request_delete.body) == 0
