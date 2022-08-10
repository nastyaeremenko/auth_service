from http import HTTPStatus

from flasgger import swag_from
from flask_restful import abort, Resource, reqparse

from app.api.v1.schemas import RoleSchema, PermissionSchema
from app.core.config import PERMISSION_NOT_FOUND, ROLE_NOT_FOUND
from app.docs.role_docs import (
    get_role_list_spec,
    create_role_list_spec,
    get_role_spec,
    put_role_spec,
    delete_role_spec,
    get_role_permission_spec,
    put_role_permission_spec,
    delete_role_permission_spec
)
from app.excepions import ObjectExists
from app.models import Role, Permission
from app.services.cache_help import cache_clear_role
from app.services.user_help import superuser_required

parser = reqparse.RequestParser()
parser.add_argument('slug', type=str)
parser.add_argument('description', type=str)

parser_permission_id = reqparse.RequestParser()
parser_permission_id.add_argument('permission_id', type=str)


class RolesListViewSet(Resource):
    @swag_from(get_role_list_spec)
    @superuser_required()
    def get(self):
        '''Получить все роли'''
        roles = Role.query.all()
        role_schema = RoleSchema(many=True)
        role_result = role_schema.dump(roles)
        return role_result, HTTPStatus.OK

    @swag_from(create_role_list_spec)
    @superuser_required()
    def post(self):
        '''Создание роли'''
        args = parser.parse_args()
        role = Role(**args)
        role_schema = RoleSchema()
        try:
            role.save()
        except ObjectExists as e:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors=str(e))
        result = role_schema.dump(role)
        return result, HTTPStatus.CREATED


class RoleViewSet(Resource):
    @swag_from(get_role_spec)
    @superuser_required()
    def get(self, id):
        '''Получение данных роли по id'''
        role = Role.query.get_or_404(id, ROLE_NOT_FOUND)
        role_schema = RoleSchema()
        role_result = role_schema.dump(role)
        return role_result, HTTPStatus.OK

    @swag_from(put_role_spec)
    @superuser_required()
    def put(self, id):
        '''Изменение данных роли'''
        data = parser.parse_args()
        role = Role.query.get_or_404(id, ROLE_NOT_FOUND)
        cache_clear_role(role)
        role.slug = data.get('slug') or role.slug
        role.description = data.get('description') or role.description
        role_schema = RoleSchema(only=['id', 'slug', 'description'])
        try:
            role.save()
        except ObjectExists as e:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors=str(e))
        role_result = role_schema.dump(role)
        return role_result, HTTPStatus.OK

    @swag_from(delete_role_spec)
    @superuser_required()
    def delete(self, id):
        '''Удаление роли'''
        role = Role.query.get_or_404(id, ROLE_NOT_FOUND)
        cache_clear_role(role)
        role.delete()
        return '', HTTPStatus.NO_CONTENT


class RolePermissionView(Resource):
    @swag_from(get_role_permission_spec)
    @superuser_required()
    def get(self, id):
        '''Получение списка прав для роли'''
        role = Role.query.get_or_404(id, ROLE_NOT_FOUND)
        permission_schema = PermissionSchema(many=True)
        permission_result = permission_schema.dump(role.permission)
        return permission_result, HTTPStatus.OK

    @swag_from(put_role_permission_spec)
    @superuser_required()
    def post(self, id):
        '''Добавление права для роли'''
        role = Role.query.get_or_404(id, ROLE_NOT_FOUND)
        args = parser_permission_id.parse_args()
        permission = Permission.query.get_or_404(args.get('permission_id'),
                                                 PERMISSION_NOT_FOUND)
        role.permission.append(permission)
        try:
            role.save()
        except ObjectExists as e:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  errors=str(e))
        permission_schema = PermissionSchema(many=True)
        role_result = permission_schema.dump(role.permission)
        cache_clear_role(role)
        return role_result, HTTPStatus.CREATED

    @swag_from(delete_role_permission_spec)
    @superuser_required()
    def delete(self, id):
        '''Удаление права для роли'''
        role = Role.query.get_or_404(id, ROLE_NOT_FOUND)
        args = parser_permission_id.parse_args()
        permission = Permission.query.get_or_404(args.get('permission_id'),
                                                 PERMISSION_NOT_FOUND)
        try:
            role.permission.remove(permission)
        except ValueError:
            pass
        else:
            role.save()
        permission_schema = PermissionSchema(many=True)
        role_result = permission_schema.dump(role.permission)
        cache_clear_role(role)
        return role_result, HTTPStatus.OK
