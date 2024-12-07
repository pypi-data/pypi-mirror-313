import json
import time
import aiomysql
from scan import crawl
from hashlib import md5
from scan.common import logger


class Monitor:
    def __init__(self):
        self.__logs = {}

    def _need_send(self, send_data):
        data_md5 = md5(json.dumps(send_data).encode()).hexdigest()
        now = int(time.time())
        for k, v in self.__logs.items():
            if v + 60 * 30 < now:
                self.__logs.pop(k)
        if self.__logs.get(data_md5):
            return False
        else:
            self.__logs.update({data_md5: int(time.time())})
            return True

    async def send_warn_fs(self, web_hook_url, product_name, message, at='', uid=''):
        post_data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "爬虫项目异常推送",
                        "content": [
                            [{"tag": "text", "text": f"项目:【{product_name}】"}],
                            [{"tag": "text", "text": f"描述: {message}"}],
                            [{"tag": "text", "text": f"项目负责人:@{at}"}]
                        ]
                    }
                }
            }
        }
        if not self._need_send(post_data):
            return
        try:
            resp = await crawl.fetch(web_hook_url, json=post_data)
            data = resp.json()
            logger.info(f'告警返回:{data}')
        except Exception as e:
            logger.error(f'发送告警数据异常:{e}')

    @staticmethod
    async def async_check_mysql_update_time(conn, db, table, host=None, port=3306, user=None, password=None):
        try:
            if not conn:
                if not host and not port:
                    logger.error('需要数据库连接信息')
                    return
                conn = await aiomysql.connect(host=host, port=port, user=user, password=password)
            async with conn.cursor() as cur:
                find = f"SELECT UPDATE_TIME FROM  information_schema.tables WHERE  TABLE_SCHEMA = '{db}'" \
                       f" AND TABLE_NAME = '{table}'"
                await cur.execute(find)
                db_data = await cur.fetchone()
                timestamp = int(db_data[0].timestamp())
                if int(time.time()) - timestamp > 60 * 30:
                    return False
                return True
        except Exception as e:
            logger.error(f'检查表更新时间异常:{e}')
        finally:
            try:
                conn.close()
            except Exception as e:
                logger.error(f'关闭数据库连接异常:{e}')

    def check_mysql_update_time(self, conn, db, table):
        pass


monitor = Monitor()
__all__ = monitor
