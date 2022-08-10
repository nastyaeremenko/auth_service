import asyncio

import redis
import backoff
from functional.settings import TestSettings

settings = TestSettings()


@backoff.on_exception(backoff.expo, redis.exceptions.ConnectionError)
def ping(redis):
    if not redis.ping():
        raise redis.exceptions.ConnectionError


async def run_test():
    redis_db = redis.from_url(
        f'redis://{settings.redis_host}:{settings.redis_port}'
    )
    ping(redis_db)
    redis_db.close()


if __name__ == '__main__':
    asyncio.run(run_test())
