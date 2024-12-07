import asyncio
import datetime
import os
from abc import ABC, abstractmethod
from hashlib import md5

from pymongo.errors import DuplicateKeyError

from scan import logger
from scan.common import ProjectInfo
from scan.config import Config
from scan.core.scheduler import Scheduler
from scan.util import get_local_ip


class Spider(ABC):

    def __init__(self, spider_name=None, cfg_path=None):
        self.spider_status = 'pending'
        if not spider_name:
            self.spider_name = self.__class__.__name__
        else:
            self.spider_name = spider_name
        self.config = Config(cfg_path)
        self.admin = self.config.admin()
        self.rabbitmq = None
        self.mongo_db = None
        self.redis = None
        self.redis_conn = None
        self.kafka = None
        self.oss_conn = None
        self.postgresql = None
        self.task_num = None
        self.spider_id = self._spider_id()
        self.host_ip = None
        self.host_name = None
        self.task_success_count = 0
        self.task_fail_count = 0
        self.scheduler = Scheduler(self)

    def _spider_id(self):
        # Docker
        host_name = os.getenv('CONTAINER_NAME')  # docker run -e CONTAINER_NAME=***
        if not host_name:
            if ProjectInfo.is_linux:
                host_name = os.getenv('HOSTNAME')
            elif ProjectInfo.is_macos:
                host_name = os.uname().nodename
            else:
                host_name = os.environ['COMPUTERNAME']
        self.host_name = host_name
        host_ip = os.getenv('HOST_IP')  # Docker
        if not host_ip:
            host_ip = get_local_ip()
        self.host_ip = host_ip
        spider_id = self.spider_name + '-' + self.host_ip + '-' + self.host_name
        spider_id = md5(spider_id.encode()).hexdigest()[:10]
        return spider_id

    @staticmethod
    def counter(ct=None):
        def handle(func):
            async def wrapper(self, *args, **kwargs):
                result = await func(self, *args, **kwargs)
                if not self.mongo_db:
                    logger.error('There is no connection of mongoDB')
                else:
                    try:
                        collection_name = None
                        if not result and ct is False:
                            collection_name = 'hscan_fail_log'
                        elif result and ct is True:
                            collection_name = 'hscan_success_log'
                        elif ct is None and not result:
                            collection_name = 'hscan_fail_log'
                        elif ct is None and result:
                            collection_name = 'hscan_success_log'
                        if collection_name:
                            today = datetime.date.today()
                            start_of_day = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
                            timestamp = int(start_of_day.timestamp())
                            _id = f'{self.spider_name}{timestamp}'
                            save_data = {'_id': _id, 'date': str(today), 'timestamp': timestamp,
                                         'name': self.spider_name, 'count': 1}
                            try:
                                db_data = await self.mongo_db.get_collection(collection_name).find_one({'_id': _id})
                                if db_data:
                                    await self.mongo_db.get_collection(collection_name).update_one(
                                        {'_id': _id}, {'$inc': {'count': 1}})
                                else:
                                    await self.mongo_db.get_collection(collection_name).insert_one(save_data)
                            except DuplicateKeyError:
                                await self.mongo_db.get_collection(collection_name).update_one(
                                    {'_id': _id}, {'$inc': {'count': 1}})
                    except Exception as e:
                        logger.error(f'counter process error:{e}')
                if result:
                    return result
                return True
            return wrapper
        return handle

    def get_count(self):
        result = self.task_success_count, self.task_fail_count
        self.task_success_count = self.task_fail_count = 0
        return result

    async def _process(self, task_info):
        """
        在_task中调用
        包一层统计数据
        """
        try:
            res = await self.process(task_info)
            if res:
                self.task_success_count += 1
            else:
                self.task_fail_count += 1
            return res
        except Exception as e:
            self.task_fail_count += 1
            raise e

    @abstractmethod
    async def process(self, task_info):
        """
        爬虫业务逻辑入口
        :param task_info: 队列任务信息
        :return:
        """

    async def stop(self):
        self.spider_status = 'stopped'
        await self.scheduler.stop()

    async def site(self):
        """
        1. 可以对配置文件进行修改
        eg：
            self.config.config.set('client', 'task_num', 1)
        :return:
        2. 可以设置新的成员变量
        eg:
            self.mq2 = ''
        """

    @abstractmethod
    async def init(self):
        """
        初始化数据处理连接
        eg:
            mq_config = self.config.rabbitmq()
            self.rabbitmq = RabbitMQ(host=mq_config.get('host'), port=mq_config.get('port'), user=mq_config.get('user'),
                           password=mq_config.get('password'))
            await self.rabbitmq.init()
        :return:
        """

    @abstractmethod
    async def _task(self):
        """
        :return:
        """

    async def run(self, task_num=1, monitor=False):
        """
        :param task_num: 爬虫并发数
        :param monitor:  是否心跳开启监控
        :return:
        """
        logger.info('爬虫程序初始化开始...')
        # 获取爬虫配置
        await self.site()
        # 初始化数据库配置
        await self.init()
        await self.scheduler.start(monitor)
        self.spider_status = 'running'
        logger.info('爬虫程序初始化结束...')
        logger.info('开始执行任务...')
        task_list = []
        for _ in range(task_num):
            t = asyncio.create_task(self._task())
            task_list.append(t)
        await asyncio.gather(*task_list)
        logger.info('结束执行任务...')
        await self.scheduler.stop()
