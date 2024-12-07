import asyncio
from abc import ABCMeta
from scan.core.spiders.spider import Spider
from scan import logger


class SimpleSpider(Spider, metaclass=ABCMeta):

    task_queue = asyncio.Queue()

    async def add_url(self, url: str):
        """
        把下次需要请求的url放入队列
        """
        await self.task_queue.put({'url': url})

    async def add_task(self, task_info: dict):
        """
        添加任务对象
        """
        await self.task_queue.put(task_info)

    async def init(self):
        """
        普通抓取不要求初始化配置
        """

    async def _task(self):
        while self.spider_status == 'running' and not self.task_queue.empty():
            try:
                if self.task_queue.empty():
                    await asyncio.sleep(0.1)
                    continue
                try:
                    task_info = self.task_queue.get_nowait()
                except asyncio.QueueEmpty:
                    continue
                try:
                    res = await self._process(task_info)
                finally:
                    self.task_queue.task_done()  # 减少队列计数
            except Exception as e:
                logger.error(e)
