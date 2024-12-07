import time
import asyncio
from requests import session
from scan import logger
from threading import Thread

from scan.middleware.mongo_middleware import MongoMiddleware


class Scheduler:
    def __init__(self, spider):
        self.spider = spider
        self.__monitor = False
        self.__last_report_time = 0
        self.__monitor_complete = False
        self._mongo_middleware = MongoMiddleware()
        self.session = session()
        self.admin_url = self.spider.admin.get('url')
        self.admin_token = self.spider.admin.get('token')

    def _heartbeat(self, status):
        """
        发送心跳  0:注册  1：运行中  -1：停止
        :param status:
        :return:
        """
        timestamp = int(time.time())
        try:
            logger.debug(f'发送心跳: {self.spider.spider_id} {status} {timestamp}')
            resp = self.session.post(f'{self.admin_url}/heartbeat', headers={'Authorization': self.admin_token},
                                     json={'id': self.spider.spider_id,
                                           'name': self.spider.spider_name,
                                           'host_ip': self.spider.host_ip,
                                           'host_name': self.spider.host_name,
                                           'status': status,
                                           'timestamp': timestamp},
                                     timeout=30)
            if resp.status_code != 200:
                logger.error(f'发送心跳异常:{resp.status_code} {resp.text}')
        except Exception as e:
            logger.error(f'发送心跳异常:{e}')
        time.sleep(10)
        return timestamp

    def _report(self, immediate=False):
        """
        发送成功失败计数
        1分钟一次
        """
        if immediate or int(time.time()) - self.__last_report_time >= 60:
            self.__last_report_time = int(time.time())
        else:
            return
        timestamp = int(time.time())
        task_success_count, task_fail_count = self.spider.get_count()
        insert_success_count, insert_repeat_count, insert_fail_count, update_success_count, update_fail_count = \
            self._mongo_middleware.get_count()
        try:
            resp = self.session.post(f'{self.admin_url}/report', headers={'Authorization': self.admin_token},
                                     json={'id': self.spider.spider_id,
                                           'name': self.spider.spider_name,
                                           'host_ip': self.spider.host_ip,
                                           'host_name': self.spider.host_name,
                                           'task_success_count': task_success_count,
                                           'task_fail_count': task_fail_count,
                                           'insert_success_count': insert_success_count,
                                           'insert_repeat_count': insert_repeat_count,
                                           'insert_fail_count': insert_fail_count,
                                           'update_success_count': update_success_count,
                                           'update_fail_count': update_fail_count,
                                           'timestamp': timestamp},
                                     timeout=30)
            if resp.status_code != 200:
                logger.error(f'发送统计数据异常:{resp.status_code} {resp.text}')
        except Exception as e:
            logger.error(f'发送统计数据异常:{e}')
        logger.debug(f'{self.spider.spider_id} {self.spider.spider_name} 成功任务数:{task_success_count}'
                     f' 失败任务数:{task_fail_count} 入库数:{insert_success_count} 重复数:{insert_repeat_count} '
                     f'入库失败数:{insert_fail_count} 更新数:{update_success_count} 更新失败数:{update_fail_count}'
                     )

    def _monitor(self):
        """
        监控守护线程
        """
        self._heartbeat(0)
        while self.__monitor:
            self._heartbeat(1)
            self._report()
        self._heartbeat(-1)
        self._report()
        self.__monitor_complete = True

    async def start(self, monitor: bool):
        """
        开始任务调度
        """
        self.__monitor = monitor
        logger.info(f'开始调度...')
        if monitor:
            logger.info(f'注册爬虫...')
            monitor_thread = Thread(target=self._monitor)
            monitor_thread.daemon = True  # 设置为守护线程
            monitor_thread.start()
        else:
            self.__monitor_complete = True

    async def stop(self):
        """
        结束任务调度
        """
        self.__monitor = False
        while not self.__monitor_complete:
            await asyncio.sleep(1)
        logger.info(f'结束调度...')
