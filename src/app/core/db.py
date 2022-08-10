import redis as redis
from flask_migrate import Migrate, upgrade
from flask_sqlalchemy import SQLAlchemy

from app.core.config import REDIS_HOST, REDIS_PORT, SUPERUSER_ROLE

migrate_db = Migrate()
db = SQLAlchemy()
redis_db = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True
)
jwt_redis_blocklist = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=1, decode_responses=True
)


def init_db(app):
    db.init_app(app)
    migrate_db.init_app(app, db)
    app.app_context().push()
    upgrade(app.config['PATH_MIGRATION'])
    from app.models import Role
    role = Role.query.filter(Role.slug == SUPERUSER_ROLE).one_or_none()
    if not role:
        superuser = Role(slug=SUPERUSER_ROLE, description='Суперпользователь')
        superuser.save()
