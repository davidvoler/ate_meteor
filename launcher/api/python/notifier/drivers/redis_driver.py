__author__ = 'davidl'
import redis
from ate_notify_monitor.new_notifier.drivers.base_driver import BaseMonitorDriver
import ate_notify_monitor.new_notifier.config
from tornado.options import options


class RedisMonitorDriver(BaseMonitorDriver):
    def __init__(self, logger):
        self.logger = logger
        self.redis_host = options.monitor_redis_host
        self.redis_db = options.monitor_redis_db
        self.redis_port = options.monitor_redis_port
        self.pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        self._redis_connection = redis.Redis(connection_pool=self.pool)
        self.pub_sub_channel = self._redis_connection.pubsub()

    def notify(self, fixture_id, info):
        self._redis_connection.publish(fixture_id, info)

    def notify_blocking_request(self, fixture_id, info):
        """
        TODO: use publish and subscribe to a new channel for response
        :param info:
        :return:
        """
        print (info)
        return True
