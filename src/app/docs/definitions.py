definitions_spec = {
    'Auth': {
        'type': 'object',
        'required': [
            'login',
            'password',
            'g_recaptcha_response'
        ],
        'properties': {
            'login': {
                'type': 'string',
                'example': 'tester',
                'minLength': 3
            },
            'password': {
                'type': 'string',
                'example': 'qwerty',
                'minLength': 6
            },
            'g_recaptcha_response': {
                'type': 'string',
                'example': ('03AGdBq265eF2y8-Wh1GL28Xo57qBqGLUWEmWORjp'
                            '3O8sNPvswwUns6GjhwURmOrpyAjlkyVJQkOjblCBO'
                            'Q9oRaJ66lh2C3N2gHgvOGPAplUBGGv9tUCM2SeEC6'
                            'Rfcdr-9cDWBfKrzg_xgjaTwGiBLz_IHgdxgA3AVCS'
                            'M-iVFq_0zcWVs-JwWpkTpJux4g99-CMbGdS1KoEaV'
                            'u7NtBaDujyxKGczoYTNGcIrXJ6h9Gefwkv7q3loCr'
                            'JUNepuhgppm4T0WGPKFu8RhdXrm5ue-yQtWk_DPI1'
                            'kcIlq8sXveTKT7g_PnJ-RNDH9kgpDIQZD8SLKH9bN'
                            'vMa50iPE_XBuqhZHydJpXfQzSXW8vnIhDrXfzPBmc'
                            'Q1omCcr2cCe-CGC35ZPjwqq404oqqeux37smo-bXz'
                            'MYX6fmvFpUFYnxmA_4WJRFhZtEkux6k2JjpshoYVg'
                            'SEjHaisSGZv')
            },
        },
    },
    'Permission': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb'
            },
            'description': {
                'type': 'string',
                'example': 'чтото правит'
            },
            'slug': {
                'type': 'string',
                'example': 'edit'
            }
        },
    },
    'PermissionCreate': {
        'type': 'object',
        'properties': {
            'description': {
                'type': 'string',
                'example': 'что-то правит'
            },
            'slug': {
                'type': 'string',
                'example': 'edit'
            }
        },
    },
    'Refresh': {
        'type': 'object',
        'required': [
            'r_token',
        ],
        'properties': {
            'r_token': {
                'type': 'string',
                'example': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MDExNDY1MCwianRpIjoiOTQxMjAyZGQtMDUyYS00NGNiLWE0OTctMzE5MmUzODczYWYyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJzc3NzIiwibmJmIjoxNjUwMTE0NjUwLCJleHAiOjE2NTI3MDY2NTAsImF1ZCI6InNvbWVfYXVkaWVuY2UiLCJmb28iOiJiYXIiLCJ1cGNhc2VfbmFtZSI6IlNTU1MifQ.ATpiX1IgT2Hl3pUcb1OCDvxFAJlCzqDaN9uE40kM23A'
            }
        },
    },
    'Requests': {
        'type': 'object',
        'required': [
            'login',
            'password'
        ],
        'properties': {
            'login': {
                'type': 'string',
                'example': 'tester',
                'minLength': 3
            },
            'password': {
                'type': 'string',
                'example': 'qwerty',
                'minLength': 6
            }
        },
    },
    'Role': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb'
            },
            'description': {
                'type': 'string',
                'example': 'Администратор'
            },
            'slug': {
                'type': 'string',
                'example': 'admin'
            }
        },
    },
    'RoleCreate': {
        'type': 'object',
        'properties': {
            'description': {
                'type': 'string',
                'example': 'Тестировщик'
            },
            'slug': {
                'type': 'string',
                'example': 'tester'
            }
        },
    },
    'RolePermissionEdit': {
        'type': 'object',
        'properties': {
            'permission_id': {
                'type': 'string',
                'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb'
            },
        },
    },
    'Tokens': {
        'type': 'object',
        'properties': {
            'access_token': {
                'type': 'string',
                'example': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MDExNDY1MCwianRpIjoiZWIwMDhiY2YtMjc4NC00NGYzLTk2YzUtZTEwMmU0MDFlYmMzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNzc3MiLCJuYmYiOjE2NTAxMTQ2NTAsImV4cCI6MTY1MDExNTU1MCwiYXVkIjoic29tZV9hdWRpZW5jZSIsImZvbyI6ImJhciIsInVwY2FzZV9uYW1lIjoiU1NTUyJ9.l1cB3OWdJcaTI7CaqGYZO55U57LVXqh_hGYn32IeuFw',
            },
            'refresh_token': {
                'type': 'string',
                'example': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MDExNDY1MCwianRpIjoiOTQxMjAyZGQtMDUyYS00NGNiLWE0OTctMzE5MmUzODczYWYyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJzc3NzIiwibmJmIjoxNjUwMTE0NjUwLCJleHAiOjE2NTI3MDY2NTAsImF1ZCI6InNvbWVfYXVkaWVuY2UiLCJmb28iOiJiYXIiLCJ1cGNhc2VfbmFtZSI6IlNTU1MifQ.ATpiX1IgT2Hl3pUcb1OCDvxFAJlCzqDaN9uE40kM23A'

            }
        },
    },
    'User': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'example': '005211d8-3d2a-4436-9249-10e42265a783'
            },
            'login': {
                'type': 'string',
                'example': '22112'
            }
        },
    },
    'UserEdit': {
        'type': 'object',
        'properties': {
            'login': {
                'type': 'string',
                'example': 'tester',
                'minLength': 3
            },
            'password': {
                'type': 'string',
                'example': 'qwerty',
                'minLength': 6
            }
        },
    },
    'Profile': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'example': '005211d8-3d2a-4436-9249-10e42265a783'
            },
            'created_date': {
                'type': 'datetime',
                'example': '2022-04-18T17:39:22.972991'
            },
            'name': {
                'type': 'string',
                'example': 'Alex'
            },
            'email': {
                'type': 'string',
                'example': 'test@test.ru'
            },
            'user': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'example': '005211d8-3d2a-4436-9249-10e42265a783'
                    },
                    'login': {
                        'type': 'string',
                        'example': '22112'
                    }
                }
            },
            'social_auth': {
                'type': 'array',
                'items': {'$ref': '#/definitions/SocialAuth'}
            }
        },
    },
    'ProfileEdit': {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
                'example': 'Alex',
                'minLength': 3
            },
            'email': {
                'type': 'string',
                'example': 'test@test.ru',
            }
        },
    },
    'SocialAuth': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'example': 'b0470dc5-282d-4a21-8bc3-d14c92976173'
            },
            'social_name': {
                'type': 'string',
                'example': 'yandex'

            },
            'social_user_id': {
                'type': 'string',
                'example': 'id929030302'

            }
        },
    },
    'ProfileHistory': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'example': 'b0470dc5-282d-4a21-8bc3-d14c92976173'
            },
            'auth_date': {
                'type': 'datetime',
                'example': '2022-04-18T17:39:27.499483'

            },
            'last_active_date': {
                'type': 'datetime',
                'example': '2022-04-18T17:39:27.499483'

            },
            'agent': {
                'type': 'string',
                'example': 'PostmanRuntime/7.29.0'

            }
        },
    },
    'ProfileAccess': {
        'type': 'object',
        'properties': {
            'roles': {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'example': 'admin'
                }
            },
            'permissions': {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'example': 'edit'
                }
            },
        },
    },
    'ProfileRoleEdit': {
        'type': 'object',
        'properties': {
            'role_id': {
                'type': 'string',
                'example': 'fa3d8247-c717-4aa1-8de9-cfe5fc0233bb'
            },
        },
    },
}
