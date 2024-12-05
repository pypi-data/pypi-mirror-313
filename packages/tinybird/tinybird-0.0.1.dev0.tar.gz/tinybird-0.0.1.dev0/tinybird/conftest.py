from tinybird.model import RedisModel
from tinybird_shared.redis_client.redis_client import TBRedisClientSync, TBRedisConfig


def pytest_configure(config):
    redis_client = TBRedisClientSync(TBRedisConfig())
    redis_client.flushdb()
    RedisModel.config(redis_client)
