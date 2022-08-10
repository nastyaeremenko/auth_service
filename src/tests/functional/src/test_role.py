from http import HTTPStatus
from uuid import uuid4

import pytest

URL = '/role'
TEST_URL = f'{URL}/{uuid4()}'


def test_get_roles_superuser(make_fetch_request, login_superuser,
                             clear_postgres):
    access_token = login_superuser.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    request = make_fetch_request('GET', '/role', headers=headers)
    assert request.status == HTTPStatus.OK
    assert len(request.body) == 1


@pytest.mark.parametrize(
    (
            'body', 'method', 'url'
    ),
    (

            (
                    {'slug': 'pretty'},
                    'POST',
                    URL,
            ),
            (
                    {},
                    'GET',
                    URL,
            ),
            (
                    {},
                    'GET',
                    TEST_URL,
            ),
            (
                    {'slug': 'pretty2'},
                    'PUT',
                    TEST_URL,
            ),
            (
                    {},
                    'DELETE',
                    TEST_URL,
            ),

    )

)
def test_role_unauthorized(make_fetch_request, clear_postgres,
                           body, method, url):
    request = make_fetch_request(method, url, body=body)
    assert request.status == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    (
            'body', 'method', 'url'
    ),
    (

            (
                    {'slug': 'pretty'},
                    'POST',
                    URL,
            ),
            (
                    {},
                    'GET',
                    URL,
            ),
            (
                    {},
                    'GET',
                    TEST_URL,
            ),
            (
                    {'slug': 'pretty2'},
                    'PUT',
                    TEST_URL,
            ),
            (
                    {},
                    'DELETE',
                    TEST_URL,
            ),

    )

)
def test_role_test_user(make_fetch_request, login_test_user,
                        clear_postgres, body, method, url):
    access_token = login_test_user.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    request = make_fetch_request(method, url, body=body,
                                 headers=headers)
    assert request.status == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    (
            'slug', 'description', 'put_body', 'put_status'
    ),
    (

            (
                    'pretty',
                    None,
                    {'description': 'New description'},
                    HTTPStatus.OK,
            ),
            (
                    'subscriber',
                    'Главный надзиратель',
                    {'slug': 'pretty'},
                    HTTPStatus.UNPROCESSABLE_ENTITY,
            ),
            (
                    'admin',
                    None,
                    {'slug': 'subscriber_new'},
                    HTTPStatus.OK,
            )
    )

)
def test_post_put_role_superuser(make_fetch_request, login_superuser,
                                 clear_postgres, slug, description,
                                 put_body, put_status):
    body = {'slug': slug, 'description': description}
    access_token = login_superuser.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    request = make_fetch_request('POST', URL, body=body,
                                 headers=headers)
    assert request.status == HTTPStatus.CREATED
    request_body = request.body
    assert 'slug' in request_body
    assert request_body['slug'] == body['slug']
    assert 'description' in request_body
    assert request_body['description'] == body['description']
    role_url = f'{URL}/{request_body["id"]}'
    request_get = make_fetch_request('GET', role_url,
                                     headers=headers)
    assert request_get.status == HTTPStatus.OK
    request_put = make_fetch_request('PUT', role_url, body=put_body,
                                     headers=headers)
    assert request_put.status == put_status


@pytest.mark.parametrize(
    (
            'slug', 'description'
    ),
    (
            (
                    None,
                    'Упс'
            ),
            (
                    'subscriber',
                    'Упс'
            ),

    )

)
def test_post_errors_role_superuser(make_fetch_request, login_superuser,
                                    clear_postgres, slug, description):
    body = {'slug': slug, 'description': description}
    access_token = login_superuser.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    request = make_fetch_request('POST', URL, body=body,
                                 headers=headers)
    assert request.status == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_role_superuser(make_fetch_request, login_superuser,
                               clear_postgres):
    body = {'slug': 'test', 'description': 'Test'}
    access_token = login_superuser.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    request = make_fetch_request('POST', URL, body=body,
                                 headers=headers)
    assert request.status == HTTPStatus.CREATED
    request_body = request.body
    role_url = f'{URL}/{request_body["id"]}'
    request_delete = make_fetch_request('DELETE', role_url, headers=headers)
    assert request_delete.status == HTTPStatus.NO_CONTENT
    request_delete_2 = make_fetch_request('DELETE', TEST_URL, headers=headers)
    assert request_delete_2.status == HTTPStatus.NOT_FOUND
