from app.core.db import redis_db
from app.models import Role


def cache_clear_role(role: Role) -> None:
    redis_db.delete(role.slug)


def cache_clear_roles(roles: list[Role]) -> None:
    redis_db.delete(','.join([role.slug for role in roles]))
