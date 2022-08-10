get_profile_role_spec = {
    'tags': ['profile_role'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb',
            'required': 'true',
            'description': 'id пользователя',
        },
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
        },
        '404': {
            'description': 'Error: NOT FOUND',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'User not found'
                    }
                }
            }
        }
    },
}
put_profile_role_spec = {
    'tags': ['profile_role'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb',
            'required': 'true',
            'description': 'id пользователя',
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
                    '$ref': '#/definitions/Role'
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
                        'example': 'User not found'
                    }
                }
            }
        }
    },
}
delete_profile_role_spec = {
    'tags': ['profile_role'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb',
            'required': 'true',
            'description': 'id пользователя',
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/ProfileRoleEdit'
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
                        'example': 'Profile not found'
                    }
                }
            }
        }
    },
}

get_user_access_spec = {
    'tags': ['profile'],
    'security': [{
        'api_key': []
    }],
    "parameters": [],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                '$ref': '#/definitions/ProfileAccess'
            }
        },
        '401': {
            'description': 'Error: UNAUTHORIZED',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Missing JWT in headers, query_string or json (Missing Authorization Header; Missing \'r_token\' query paramater; Invalid content-type. Must be application/json.)'
                    }
                }
            }
        }
    },
}

get_profile_history_spec = {
    'tags': ['profile'],
    'security': [{
        'api_key': []
    }],
    "parameters": [],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/ProfileHistory'
                }
            }
        },
        '401': {
            'description': 'Error: UNAUTHORIZED',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Missing JWT in headers, query_string or json '
                                   '(Missing Authorization Header; '
                                   'Missing \'r_token\' query paramater; '
                                   'Invalid content-type. '
                                   'Must be application/json.)'
                    }
                }
            }
        }
    }
}

get_profile_spec = {
    'tags': ['profile'],
    "parameters": [],
    'security': [{
        'api_key': []
    }],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                '$ref': '#/definitions/Profile'
            }
        },
        '401': {
            'description': 'Error: UNAUTHORIZED',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Missing JWT in headers, query_string or '
                                   'json (Missing Authorization Header; '
                                   'Missing \'r_token\' query paramater; '
                                   'Invalid content-type. '
                                   'Must be application/json.)'
                    }
                }
            }
        }
    }
}

put_profile_spec = {
    'tags': ['profile'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/ProfileEdit'
            },
            'required': 'true',
            'description': 'Тело запроса с данными профиля',
        }
    ],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                '$ref': '#/definitions/Profile'
            }
        },
        '401': {
            'description': 'Error: UNAUTHORIZED',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Missing JWT in headers, query_string or '
                                   'json (Missing Authorization Header; M'
                                   'issing \'r_token\' query paramater; '
                                   'Invalid content-type. '
                                   'Must be application/json.)'
                    }
                }
            }
        }
    }
}

put_user_spec = {
    'tags': ['user'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/UserEdit'
            },
            'required': 'true',
            'description': 'Тело запроса с данными пользователя',
        }
    ],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                '$ref': '#/definitions/User'
            }
        },
        '401': {
            'description': 'Error: UNAUTHORIZED',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'Missing JWT in headers, query_string or '
                                   'json (Missing Authorization Header; M'
                                   'issing \'r_token\' query paramater; '
                                   'Invalid content-type. '
                                   'Must be application/json.)'
                    }
                }
            }
        }
    }
}

post_user_spec = {
    'tags': ['user'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/Requests'
            },
            'required': 'true',
            'description': 'Тело запроса с логином и паролем',
        }
    ],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                'type': 'object',
                'properties': {
                    'result': {
                        'type': 'string',
                        'example': 'Ok'
                    }
                }
            },
        },
        '400': {
            'description': 'Error: BAD REQUEST',
            'schema': {
                'type': 'object',
                'properties': {
                    'errors': {
                        'type': 'string',
                    }
                }
            }
        },
        '422': {
            'description': 'Error: UNPROCESSABLE ENTITY',
            'schema': {
                'type': 'object',
                'properties': {
                    'errors': {
                        'type': 'string',
                        'example': 'Login not correct'
                    }
                }
            },
        }
    }
}

post_social_spec = {
    'tags': ['social'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
        {
            'name': 'social_name',
            'in': 'path',
            'type': 'string'
        }
    ],
    'responses': {
        '404': {
            'description': 'Error: NOT_FOUND',
            'schema': {
                'type': 'object',
                'properties': {
                    'errors': {
                        'type': 'string',
                        'example': ('This site doesn`t allow you to '
                                    'connect to the specified '
                                    'social networks')
                    }
                }
            },
        }
    }
}

delete_social_spec = {
    'tags': ['social'],
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
                        'example': 'Social network not found'
                    }
                }
            }
        }
    },
}
