import logging

import click
from marshmallow import ValidationError

from app.api.v1.schemas import RegisterUser
from app.core.config import SUPERUSER_ROLE
from app.excepions import ObjectExists
from app.models import User, Role, Profile


@click.command("create-superuser")
@click.argument('login')
@click.argument('password')
def create_superuser(login, password):
    user_validate = RegisterUser()
    try:
        user_validate.load({
            'login': login,
            'password': password
        })
    except ValidationError as errors:
        logging.error(errors.messages)
        return

    user = User(login=login)
    user.set_password(password)

    superuser_role = Role.query.filter_by(slug=SUPERUSER_ROLE).first()
    profile = Profile()
    profile.role.append(superuser_role)
    profile.save()
    user.profile_id = profile.id
    try:
        user.save()
    except ObjectExists as e:
        logging.error(str(e))
    else:
        logging.info(f'Superuser {login} successful created.')
