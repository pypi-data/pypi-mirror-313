import json
import zlib
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, TopicPartition
from scan.common import logger


class Kafka:

    def __init__(self, bootstrap_servers, task_queue, security_protocol='PLAINTEXT',
                 group_id='hscan', ssl_context=None, user=None, password=None, api_version='auto'):
        self.task_queue = task_queue
        self.bootstrap_servers = bootstrap_servers
        self.user = user
        self.password = password
        self.ssl_context = ssl_context
        self.security_protocol = security_protocol
        self.api_version = api_version
        self.group_id = group_id

    async def producer(self, gen_func, topic=None, **kwargs):
        """
        :param topic:
        :param gen_func:  generator func
        :return:
        """
        _producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            security_protocol=self.security_protocol,
            api_version=self.api_version,
            ssl_context=self.ssl_context,
            sasl_plain_username=self.user,
            sasl_plain_password=self.password,
            **kwargs
        )
        await _producer.start()
        if not topic:
            topic = self.task_queue
        try:
            data = gen_func()
            async for d in data:
                if not isinstance(d, str):
                    d = json.dumps(d)
                await _producer.send_and_wait(topic, d.encode())
                logger.info(f'send data: {d}')
        except Exception as e:
            logger.error(f'producer error:{e}')
        finally:
            await _producer.stop()

    async def send_one(self, message,  topic=None, **kwargs):
        """
        :param topic:
        :param message:
        :return:
        """
        _producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            security_protocol=self.security_protocol,
            api_version=self.api_version,
            ssl_context=self.ssl_context,
            sasl_plain_username=self.user,
            sasl_plain_password=self.password,
            **kwargs
        )
        await _producer.start()
        if not topic:
            topic = self.task_queue
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            if isinstance(message, bytes):
                await _producer.send_and_wait(topic, message)
            else:
                await _producer.send_and_wait(topic, message.encode())
        except Exception as e:
            logger.error(f'producer error:{e}')
        finally:
            await _producer.stop()

    async def consumer(self, call_back, topic=None, group_id=None, auto_offset_reset='earliest', **kwargs):
        """
        :param call_back: async func
        :param topic:
        :param group_id:
        :param auto_offset_reset:
        :return:
        """
        try:
            if not topic:
                topic = self.task_queue
            _consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id if group_id else self.group_id,
                auto_offset_reset=auto_offset_reset,
                enable_auto_commit=False,
                sasl_plain_username=self.user,
                sasl_plain_password=self.password,
                **kwargs
            )
            await _consumer.start()
            try:
                # while 1:
                    # msg = await _consumer.getone()
                    # if not msg:
                    #     continue
                    # data = json.loads(msg.value)
                    # res = await call_back(data)
                    # if res:
                    #     tp = TopicPartition(msg.topic, msg.partition)
                    #     await _consumer.commit({tp: msg.offset + 1})
                async for msg in _consumer:
                    try:
                        data = json.loads(msg.value)
                    except UnicodeDecodeError:
                        data = json.loads(zlib.decompress(msg.value).decode())
                    tp = TopicPartition(msg.topic, msg.partition)
                    await _consumer.commit({tp: msg.offset + 1})
                    # if data is None:
                    #     tp = TopicPartition(msg.topic, msg.partition)
                    #     await _consumer.commit({tp: msg.offset + 1})
                    #     continue
                    res = await call_back(data)
                    # if res:
                        # tp = TopicPartition(msg.topic, msg.partition)
                        # await _consumer.commit({tp: msg.offset + 1})
            except Exception as e:
                logger.error(f'consumer process error:{e}')
            finally:
                await _consumer.stop()
        except Exception as e:
            logger.error(f'consumer error:{e}')

    async def lag(self, topic, group_id='hscan', auto_offset_reset='earliest', **kwargs):
        try:
            _consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                auto_offset_reset=auto_offset_reset,
                enable_auto_commit=False,
                sasl_plain_username=self.user,
                sasl_plain_password=self.password,
                **kwargs
            )
            await _consumer.start()
            try:
                partitions = [TopicPartition(topic, p) for p in _consumer.partitions_for_topic(topic)]
                # 总偏移
                toff = await _consumer.end_offsets(partitions)
                toff = [(key.partition, toff[key]) for key in toff.keys()]
                toff.sort()
                # 当前消费偏移
                coff = [(x.partition, await _consumer.committed(x)) for x in partitions]
                coff.sort()
                # 堆积量
                toff_sum = sum([x[1] for x in toff])
                cur_sum = sum([x[1] for x in coff if x[1] is not None])
                left_sum = toff_sum - cur_sum
                return left_sum
            finally:
                await _consumer.stop()
        except Exception as e:
            logger.error(f'get heap error:{e}')
