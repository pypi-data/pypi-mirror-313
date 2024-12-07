import asyncio
import random
from abc import ABCMeta
from scan.core.spiders.spider import Spider
from scan import logger


class RabbitSpider(Spider, metaclass=ABCMeta):

    async def _task(self):
        """
        分布式队列任务，在任务分发使用rabbitmq时
        """
        await asyncio.sleep(random.randint(2, 20))
        task_queue = self.config.rabbitmq().get('task_queue')
        if not self.rabbitmq:
            logger.error('The task queue connection is not initialized')
            return
        arguments = None
        # 优先级队列
        if self.config.rabbitmq().get('priority'):
            arguments = {'x-max-priority': int(self.config.rabbitmq().get('priority'))}
        if self.config.rabbitmq().get('auto_ack'):
            auto_ack = True
        else:
            auto_ack = False
        while self.spider_status == 'running':
            try:
                logger.info('rabbitmq task consume started...')
                await self.rabbitmq.consume(self._process, task_queue, auto_ack=auto_ack, arguments=arguments)
            except Exception as e:
                logger.error(e)
