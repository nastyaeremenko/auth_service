from http import HTTPStatus

from flasgger import swag_from
from flask_restful import abort, Resource, reqparse

from app.api.v1.schemas import PermissionSchema
from app.core.config import PERMISSION_NOT_FOUND
from app.docs.permissions_docs import (
    get_permissions_list_spec,
    create_permissions_list_spec,
    get_permission_spec,
    put_permission_spec,
    delete_permission_spec
)
from app.excepions import ObjectExists
from app.models import Permission
from app.services.cache_help import cache_clear_roles
from app.services.user_help import superuser_required

parser = reqparse.RequestParser()
parser.add_argument('slug', type=str)
parser.add_argument('description', type=str)


class PermissionsListViewSet(Resource):
    @swag_from(get_permissions_list_spec)
    @superuser_required()
    def get(self):
        '''Получить все права'''
        permissions = Permission.query.all()
        permission_schema = PermissionSchema(many=True)
        permission_result = permission_schema.dump(permissions)
        return permission_result, HTTPStatus.OK

    @swag_from(create_permissions_list_spec)
    @superuser_required()
    def post(self):
        '''Создание права'''
        args = parser.parse_args()
        permission = Permission(**args)
        permission_schema = PermissionSchema()
        try:
            permission.save()
        except ObjectExists as e:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors=str(e))
        result = permission_schema.dump(permission)
        return result, HTTPStatus.CREATED


class PermissionViewSet(Resource):
    @swag_from(get_permission_spec)
    @superuser_required()
    def get(self, id):
        '''Получение данных прав по id'''
        permission = Permission.query.get_or_404(id, PERMISSION_NOT_FOUND)
        permission_schema = PermissionSchema()
        permission_result = permission_schema.dump(permission)
        return permission_result, HTTPStatus.OK

    @swag_from(put_permission_spec)
    @superuser_required()
    def put(self, id):
        '''Изменение права'''
        data = parser.parse_args()
        permission = Permission.query.get_or_404(id, PERMISSION_NOT_FOUND)
        permission.slug = data.get('slug') or permission.slug
        permission.description = data.get(
            'description') or permission.description
        permission_schema = PermissionSchema(
            only=['id', 'slug', 'description'])
        try:
            permission.save()
        except ObjectExists as e:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors=str(e))
        permission_result = permission_schema.dump(permission)
        cache_clear_roles(permission.role)
        return permission_result, HTTPStatus.OK

    @swag_from(delete_permission_spec)
    @superuser_required()
    def delete(self, id):
        '''Удаление права'''
        permission = Permission.query.get_or_404(id, PERMISSION_NOT_FOUND)
        permission.delete()
        cache_clear_roles(permission.role)
        return '', HTTPStatus.NO_CONTENT
