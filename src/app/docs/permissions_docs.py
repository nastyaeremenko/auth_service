get_permissions_list_spec = {
    'tags': ['permission'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
    ],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Permission'
                }
            }
        }
    },
}
create_permissions_list_spec = {
    'tags': ['permission'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/PermissionCreate'
            },
            'required': 'true',
            'description': 'Тело запроса для создания разрешения',
        }
    ],
    'responses': {
        '201': {
            'description': 'successful operation',
            'schema': {
                '$ref': '#/definitions/Permission'
            }
        }
    },
}

get_permission_spec = {
    'tags': ['permission'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb',
            'required': 'true',
            'description': 'id разрешения',
        }
    ],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                '$ref': '#/definitions/Permission'
            }
        },
        '404': {
            'description': 'Error: NOT FOUND',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Permission not found'
                    }
                }
            }
        }
    },
}

put_permission_spec = {
    'tags': ['permission'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb',
            'required': 'true',
            'description': 'id разрешения',
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/PermissionCreate'
            },
            'required': 'true',
        }
    ],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                '$ref': '#/definitions/Permission'
            }
        },
        '404': {
            'description': 'Error: NOT FOUND',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Permission not found'
                    }
                }
            }
        }
    },
}

delete_permission_spec = {
    'tags': ['permission'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb',
            'required': 'true',
            'description': 'id разрешения',
        },
    ],
    'responses': {
        '204': {
            'description': 'successful operation',
        },
        '404': {
            'description': 'Error: NOT FOUND',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Permission not found'
                    }
                }
            }
        }
    },
}
