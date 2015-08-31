__author__ = 'davidl'
from ate_notify_monitor.new_notifier.drivers.base_driver import BaseMonitorDriver
import ate_notify_monitor.new_notifier.config
from tornado.options import options


class DdpMonitorDriver(BaseMonitorDriver):
    def __init__(self, logger):
        self.logger = logger
        self.ddp_host = options.ddp_redis_host

    def notify(self, fixture_id, info):
        print (info)

    def notify_blocking_request(self, fixture_id, info):
        print (info)
        return True
