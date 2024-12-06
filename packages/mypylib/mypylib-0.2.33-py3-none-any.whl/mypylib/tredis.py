import redis
import threading
from loguru import logger
import traceback
from time import sleep
from typing import Union
import queue


class redis_channel:
    RAYIN_ORDER_CHANNEL_TEST = 'RAYIN_ORDER_CHANNEL_TEST'
    RAYIN_ORDER_CHANNEL_FORMAL = 'RAYIN_ORDER_CHANNEL_FORMAL'



class base_tredis_msg_sender:
    def __init__(self, tredis=None):
        self.tredis: Tredis = tredis

    def redis_msg_sender(self, channel, data):
        logger.info(f'This is what I got: {data} from {channel}')
        if self.tredis is not None and self.tredis.r is not None:
            ret = self.tredis.r.get(str(data))
            if ret is not None:
                logger.info(f'This is what I have found {ret} {type(ret)}')
                return ret
            else:
                logger.info(f'Cannot find {data} on server')
        return None


# TODO: 怪怪的，效率很差...
class Tredis_publish(threading.Thread):
    str_exit_magic_words = 'Exit Exit Exit now'

    def __init__(self,
                 server='localhost',
                 port=6379,
                 db=0,
                 password=''):
        threading.Thread.__init__(self)
        self.server = server
        self.port = port
        self.db = db
        self.password = password
        self.queue_publish = queue.Queue()

        self.r = redis.StrictRedis(host=self.server,
                                   port=self.port,
                                   db=self.db,
                                   charset="utf-8",
                                   decode_responses=True,
                                   password=self.password)
        self.start()

    def run(self):
        while True:
            try:
                channel, message = self.queue_publish.get(timeout=1)
                self.r.publish(channel, message)
                self.queue_publish.task_done()
                if channel == Tredis_publish.str_exit_magic_words and message == Tredis_publish.str_exit_magic_words:
                    break
            except queue.Empty:
                pass

    def publish(self, channel, message):
        # logger.info(f'queue publish: {channel} {message}')
        self.queue_publish.put((channel, message), block=True)

    def stop(self):
        self.publish(Tredis_publish.str_exit_magic_words, Tredis_publish.str_exit_magic_words)


class Tredis_subscribe(threading.Thread):
    def __init__(self,
                 server='localhost',
                 port=6379,
                 db=0,
                 password='',
                 channel='test',
                 prefix='test',
                 redis_msg_sender=base_tredis_msg_sender()):
        threading.Thread.__init__(self)
        self.server = server
        self.port = port
        self.db = db
        self.password = password
        self.channel = channel
        self.prefix = prefix
        self.redis_msg_sender = redis_msg_sender
        # 很奇怪的 bug。如果加了這行，warrant_detector.py 那邊第一個 redis 就會送不出東西
        # self.redis_msg_sender.tredis = self
        self.r: redis.client.Redis = None
        self.str_thread_exit_magic = 'redis thread exit'

        self.sub: Union[redis.client.PubSub, None] = None

        # For test
        # r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
        self.r = redis.StrictRedis(host=self.server,
                                   port=self.port,
                                   db=self.db,
                                   charset="utf-8",
                                   decode_responses=True,
                                   password=self.password)

        logger.info(f'Redis connected to {self.server}, port {self.port}, db: {self.db}')
        self.sub: redis.client.PubSub = self.r.pubsub()
        logger.info(f'Redis subscribe to channel [{self.channel}]')

        self.start()
        sleep(1)

    def subscribe(self, channel):
        logger.info(f'Redis subscribe to extra channel [{channel}]')
        self.sub.subscribe(channel)

    def run(self):
        t = threading.current_thread()
        self.sub.subscribe(self.channel)
        for message in self.sub.listen():
            if message:
                # logger.info(f'REDIS got message: [{message}]')
                try:
                    channel = message['channel']
                    data = message['data']
                    # logger.info(f'redis_working_thread got msg: {data}')

                    if isinstance(data, str) and data.startswith(self.str_thread_exit_magic):
                        if data[len(self.str_thread_exit_magic) + 1:] == str(self):
                            logger.info(f'{self} to exit')
                            break
                    else:
                        function_send = getattr(self.redis_msg_sender, 'redis_msg_sender', None)
                        if function_send is not None and callable(function_send):
                            # logger.info(f'function_send: {data}')
                            function_send(channel, data)
                except Exception as e:
                    traceback.print_exc()
                    logger.exception(f'\033[1;33mredis subscribe\n{message}\n{e}\033[0m')
        logger.info(f'redis thread: {self} stopped.')

    @logger.catch()
    def stop(self):
        t = threading.current_thread()
        self.r.publish(self.channel, f'{self.str_thread_exit_magic} {str(self)}')


class Tredis:
    default_port = 6379
    default_db = 0

    def __init__(self,
                 server='localhost',
                 port=6379,
                 db=0,
                 password='',
                 channel='test',
                 prefix='test',
                 redis_msg_sender=base_tredis_msg_sender()):
        self.tredis_subscribe = Tredis_subscribe(server, port, db, password, channel, prefix, redis_msg_sender)
        self.tredis_publish = Tredis_publish(server, port, db, password)

        self.r = self.tredis_publish.r

    def subscribe(self, channel):
        self.tredis_subscribe.subscribe(channel)

    def publish(self, channel, message):
        self.tredis_publish.publish(channel, message)

    def stop(self):
        self.tredis_subscribe.stop()
        self.tredis_publish.stop()

    def join(self):
        self.tredis_subscribe.join()
        self.tredis_publish.join()


if __name__ == '__main__':

    class warrant_channel:
        ALL = 'WARRANT_ALL'
        DEALER = 'WARRANT_DEALER'
        LARGE_VOLUME = 'WARRANT_LARGE_VOLUME'
        BURST = 'WARRANT_BURST'

        AMOUNT_STOCK_AND_WARRANT = 'AMOUNT_STOCK_AND_WARRANT'
        AMOUNT_WARRANT = 'AMOUNT_WARRANT'
        AMOUNT_STOCK = 'AMOUNT_STOCK'


    # logger.disable('mypylib.tredis')

    sender = base_tredis_msg_sender()

    tredis = Tredis(server='livewithjoyday.com',
                    port=Tredis.default_port,
                    db=Tredis.default_db,
                    password='5k4g4redisau4a83',
                    channel='warrant_command',
                    prefix='warrant',
                    redis_msg_sender=sender
                    )
    tredis_shioaji = Tredis(server='localhost',
                            port=Tredis.default_port,
                            db=Tredis.default_db,
                            password='',
                            channel='shioaji_wrapper',
                            prefix='shioaji',
                            redis_msg_sender=sender
                            )

    tredis.subscribe(warrant_channel.ALL)
    tredis.subscribe(warrant_channel.DEALER)
    tredis.subscribe(warrant_channel.LARGE_VOLUME)
    tredis.subscribe(warrant_channel.BURST)

    tredis.publish(warrant_channel.ALL, warrant_channel.ALL)
    tredis_shioaji.publish(warrant_channel.ALL, warrant_channel.ALL + ' tredis_shioaji')
    tredis.publish(warrant_channel.DEALER, warrant_channel.DEALER)
    tredis_shioaji.publish(warrant_channel.DEALER, warrant_channel.DEALER + ' tredis_shioaji')
    tredis.publish(warrant_channel.LARGE_VOLUME, warrant_channel.LARGE_VOLUME)
    tredis_shioaji.publish(warrant_channel.LARGE_VOLUME, warrant_channel.LARGE_VOLUME + ' tredis_shioaji')
    tredis.publish(warrant_channel.BURST, warrant_channel.BURST)
    tredis_shioaji.publish(warrant_channel.BURST, warrant_channel.BURST + ' tredis_shioaji')

    index = 0
    while True:
        try:
            sleep(1)
            index += 1
            if index == 3:
                break
        except KeyboardInterrupt:
            break

    tredis_shioaji.stop()
    tredis.stop()
