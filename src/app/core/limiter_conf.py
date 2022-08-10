from app.core.db import redis_db
from app.utils.limiter import Limiter
from app.utils.limiter_help import get_login

limiter_login = Limiter(
    db=redis_db,
    key_func=get_login
)