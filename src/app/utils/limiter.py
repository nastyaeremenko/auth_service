import time
from functools import wraps
from http import HTTPStatus
from typing import Callable

from redis import Redis


class Limiter:
    def __init__(self, db: Redis, key_func: Callable) -> None:
        self.db = db
        self.key_func = key_func

    def limit(self, duration, limit):
        def wrap(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                pipe = self.db.pipeline(transaction=True)
                key = self.key_func()
                key = '{}:{}:{}'.format(key, duration,
                                        int(time.time() // duration))
                count = pipe.incr(key)
                pipe.expire(key, duration)
                if pipe.execute()[0] > limit:
                    return (
                        {'msg': str(
                            'The user has sent too many requests '
                            'in  a given amount of time'
                        )},
                        HTTPStatus.TOO_MANY_REQUESTS
                    )
                return fn(*args, **kwargs)

            return decorator

        return wrap

