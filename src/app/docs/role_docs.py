get_role_list_spec = {
    'tags': ['role'],
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
                    '$ref': '#/definitions/Role'
                }
            }
        }
    },
}
create_role_list_spec = {
    'tags': ['role'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/RoleCreate'
            },
            'required': 'true',
            'description': 'Тело запроса для создания разрешения',
        }
    ],
    'responses': {
        '201': {
            'description': 'successful operation',
            'schema': {
                '$ref': '#/definitions/Role'
            }
        }
    },
}

get_role_spec = {
    'tags': ['role'],
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
                '$ref': '#/definitions/Role'
            }
        },
        '404': {
            'description': 'Error: NOT FOUND',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Role not found'
                    }
                }
            }
        }
    },
}

put_role_spec = {
    'tags': ['role'],
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
                '$ref': '#/definitions/Role'
            }
        },
        '404': {
            'description': 'Error: NOT FOUND',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Role not found'
                    }
                }
            }
        }
    },
}

delete_role_spec = {
    'tags': ['role'],
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
                        'example': 'Role not found'
                    }
                }
            }
        }
    },
}

get_role_permission_spec = {
    'tags': ['role_permission'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb',
            'required': 'true',
            'description': 'id роли',
        },
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
        },
        '404': {
            'description': 'Error: NOT FOUND',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Role not found'
                    }
                }
            }
        }
    },
}
put_role_permission_spec = {
    'tags': ['role_permission'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb',
            'required': 'true',
            'description': 'id роли',
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/RolePermissionEdit'
            },
            'required': 'true',
        }
    ],
    'responses': {
        '201': {
            'description': 'successful operation',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Permission'
                }
            }
        },
        '404': {
            'description': 'Error: NOT FOUND',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Role not found'
                    }
                }
            }
        }
    },
}
delete_role_permission_spec = {
    'tags': ['role_permission'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb',
            'required': 'true',
            'description': 'id роли',
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/RolePermissionEdit'
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
                        'example': 'Role not found'
                    }
                }
            }
        }
    },
}
