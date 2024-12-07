import json
import aioredis
from scan.common import logger


class Redis:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host') or 'localhost'
        self.port = kwargs.get('port') or 6379
        self.password = kwargs.get('password')
        self.db = kwargs.get('db') or 1
        self.pool_size = kwargs.get('pool_size') or 10
        self.user = kwargs.get('user')
        self.redis_conn = None
        self.group_name = None

    async def get_redis(self, pool_size=None):
        if pool_size and isinstance(pool_size, int):
            self.pool_size = pool_size
        pool = aioredis.ConnectionPool.from_url(f"redis://{self.host}", port=int(self.port), username=self.user, password=self.password,
                                                db=int(self.db), max_connections=int(self.pool_size))
        redis = aioredis.Redis(connection_pool=pool)
        self.redis_conn = redis
        return redis

    async def publish(self, data, queue_name, priority=None):
        if not self.redis_conn:
            await self.get_redis()
        try:
            data = json.dumps(data)
            res = await self.redis_conn.lpush(queue_name, data)
            if not res:
                logger.error(f'redis queue publish message error: {queue_name} {data}')
        except Exception as e:
            logger.error(f'publish process error: {e}')

    async def consume(self, queue_name, count=1):
        if not self.redis_conn:
            await self.get_redis()
        try:
            message = await self.redis_conn.rpop(queue_name)
            if message:
                message = json.loads(message.decode())
            return message
        except Exception as e:
            logger.error(f'consume process error: {e}')

    async def ack(self, queue_name, message):
        try:
            await self.redis_conn.srem(f'temp_{queue_name}', json.dumps(message))
        except Exception as e:
            logger.error(f'ack message error:{e}')

    async def resend(self, data, queue_name):
        await self.publish(data, queue_name)


__all__ = Redis
