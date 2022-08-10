from flask import request


def get_login():
    return request.args.get('login')