import json
import asyncio
import aio_pika
from aio_pika import DeliveryMode
from aio_pika.pool import Pool
from aio_pika.exceptions import QueueEmpty
from scan.common import logger
from json import JSONDecodeError


class RabbitMQ:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host') or 'localhost'
        self.port = kwargs.get('port') or 5672
        self.user = kwargs.get('user') or 'root'
        self.password = kwargs.get('password') or 'root'
        self.virtualhost = kwargs.get('virtualhost') or '/'
        self.max_connection_size = kwargs.get('max_connection_size') or 2
        self.connection_pool = None

    async def _get_connection_poll(self):
        async def _get_connection():
            connection = await aio_pika.connect_robust(host=self.host, port=int(self.port), login=self.user,
                                                       password=self.password, virtualhost=self.virtualhost)
            return connection
        async with asyncio.Lock():
            self.connection_pool = Pool(_get_connection, max_size=int(self.max_connection_size))

    async def get_channel(self):
        for _ in range(3):
            try:
                if not self.connection_pool:
                    await self._get_connection_poll()
                if self.connection_pool:
                    async with self.connection_pool.acquire() as connection:
                        return await connection.channel()
            except Exception as e:
                logger.error(f'get channel error:{e}')
                await self._get_connection_poll()

    async def init(self, max_channel_size=None):
        # if max_channel_size and isinstance(max_channel_size, int):
        #     self.max_channel_size = max_channel_size
        await self._get_connection_poll()

    async def consume(self, call_back,  queue_name, no_ack=False, auto_ack=False, durable=True, auto_delete=False,
                      arguments=None, qos=1):
        """
        :param call_back: 回调函数
        :param qos:
        :param auto_delete:
        :param durable:
        :param no_ack:
        :param auto_ack: 拿到消息确认后再执行之后的逻辑
        :param arguments: mq绑定参数
        :param queue_name: 队列名
        :return:
        """
        try:
            channel = await self.get_channel()
            async with channel:
                await channel.set_qos(qos)
                queue = await channel.declare_queue(queue_name, durable=durable, arguments=arguments,
                                                    auto_delete=auto_delete)
                feedback = {}
                async with queue.iterator(no_ack=no_ack) as queue_iter:
                    async for message in queue_iter:
                        body = message.body
                        try:
                            task_info = json.loads(body.decode())
                            task_info.update(feedback)
                        except JSONDecodeError:
                            logger.error(f'Description Failed to format task data:{body}')
                            await message.ack()
                            continue
                        if auto_ack:
                            await message.ack()
                        try:
                            pres = await call_back(task_info)
                        except Exception as e:
                            logger.error(f'consume error:{e}')
                        if pres:
                            if not auto_ack:
                                await message.ack()
                            if isinstance(pres, dict):
                                feedback = pres
                        else:
                            logger.error(f'task fail, resend data:{task_info}')
                            priority = message.priority
                            await self.publish(data=task_info, routing_key=queue_name, priority=priority)
                            if not auto_ack:
                                await message.ack()
        except Exception as e:
            logger.error(f'consume process error: {e}')

    async def get_message(self, queue_name, durable=True, auto_delete=False, arguments=None, timeout=10):
        try:
            channel = await self.get_channel()
            async with channel:
                queue = await channel.declare_queue(queue_name, durable=durable, arguments=arguments,
                                                    auto_delete=auto_delete)
                message = await queue.get(no_ack=True, timeout=timeout)
                if not message:
                    return
                body = message.body
                try:
                    task_info = json.loads(body.decode())
                    return task_info
                except JSONDecodeError:
                    logger.error(f'Description Failed to format task data:{body}')
                return
        except QueueEmpty:
            return
        except Exception as e:
            logger.error(f'get message error: {e}')

    async def publish(self, data, routing_key, priority=None, channel=None, delivery_mode=DeliveryMode.PERSISTENT):
        """
        :param delivery_mode: 默认开启持久化
        :param priority: 消息优先级
        :param data: 要发送的数据
        :param routing_key: 队列名
        :param channel: 通道
        :return:
        """
        try:
            if not channel:
                channel = await self.get_channel()
                async with channel:
                    try:
                        await channel.default_exchange.publish(aio_pika.Message(body=json.dumps(data).encode(),
                                                                                delivery_mode=delivery_mode,
                                                                                priority=priority),
                                                               routing_key=routing_key)
                        return True
                    except Exception as e:
                        logger.error(f'publish error: {e}')
            else:
                try:
                    await channel.default_exchange.publish(aio_pika.Message(body=json.dumps(data).encode(),
                                                                            delivery_mode=delivery_mode,
                                                                            priority=priority),
                                                           routing_key=routing_key)
                    return True
                except Exception as e:
                    logger.error(f'publish error: {e}')
        except Exception as e:
            logger.error(f'publish process error: {e}')

    async def purge(self, queue_name, arguments=None):
        """
        :param arguments: 绑定队列参数
        :param queue_name: 要清空的队列名
        :return:
        """
        try:
            channel = await self.get_channel()
            async with channel:
                try:
                    queue = await channel.declare_queue(queue_name, durable=True, arguments=arguments,
                                                        auto_delete=False)
                    await queue.purge()
                    return True
                except Exception as e:
                    logger.error(f'purge error: {e}')
        except Exception as e:
            logger.error(f'purge process error: {e}')

    async def message_count(self, queue_name, arguments=None):
        try:
            channel = await self.get_channel()
            async with channel:
                try:
                    queue = await channel.declare_queue(queue_name, durable=True, arguments=arguments,
                                                        auto_delete=False)
                    count = queue.declaration_result.message_count
                    return count
                except Exception as e:
                    logger.error(f'message_count error: {e}')
        except Exception as e:
            logger.error(f'message_count process error: {e}')


__all__ = RabbitMQ
