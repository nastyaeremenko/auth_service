spec_register = {
    'tags': ['auth'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/Auth'
            },
            'required': 'true',
            'description': 'Тело запроса с регистрационными данными',
        }
    ],
    'responses': {
        '201': {
            'description': 'successful operation',
            'schema': {
                'type': 'object',
                'properties': {
                    'result': {
                        'type': 'string',
                        'example': 'ok'
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

spec_refresh = {
    'tags': ['auth'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                '$ref': '#/definitions/Refresh'
            },
            'required': 'true',
            'description': 'Тело запроса для обновления токена',
        }
    ],

    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                '$ref': '#/definitions/Tokens'
            }

        },
        '401': {
            'description': 'Error: UNAUTHORIZED',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
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
                    'msg': {
                        'type': 'string',
                        'example': 'Signature verification failed'
                    }
                }
            },
        }
    }
}

spec_login = {
    'tags': ['auth'],
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
                '$ref': '#/definitions/Tokens'
            }

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
        '401': {
            'description': 'Error: UNAUTHORIZED',
            'schema': {
                'type': 'object',
                'properties': {
                    'errors': {
                        'type': 'string',
                        'example': 'Login or Password not correct'
                    }
                }
            },
            'examples': {
                'errors': 'Введен некорректный логин или пароль.'
            }
        }
    }
}

spec_logout = {
    'tags': ['auth'],
    'security': [{
        'api_key': []
    }],
    'parameters': [
    ],
    'responses': {
        '200': {
            'description': 'successful operation',
            'schema': {
                'type': 'object',
                'properties': {
                    'result': {
                        'type': 'string',
                        'example': 'logout success'
                    }
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
                    }
                }
            }
        },
    }
}

spec_login_social = {
    'tags': ['auth'],
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

spec_authorize_social = {
    'tags': ['auth'],
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
            }
        },
        '201': {
            'description': 'successful creation',
            'schema': {
                '$ref': '#/definitions/Tokens'
            }
        },
        '400': {
            'description': 'Error: BAD_REQUEST',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'invalid request: Неверные параметры'
                    }
                }
            }
        },
        '422': {
            'description': 'Error: UNAUTHORIZED',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'example': 'This social network is already attached.'
                    }
                }
            }
        },
    }
}
