import requests
import redis
from requests.exceptions import Timeout, ConnectionError, HTTPError
import json
import time
from tornado.options import options
import config

from ate_logger import AteLogger


class NotifyMonitor(object):
    def __init__(self, logger=None):
        if logger:
            self.__logger = AteLogger("Notify Monitor", logger.logger_info)
        else:
            self.__logger = AteLogger("Notify Monitor")
        self.driver = None
        if options.monitor_http_driver:
            from ate_notify_monitor.new_notifier.drivers.http_driver import HttpMonitorDriver

            self.driver = HttpMonitorDriver(self.__logger)
        elif options.monitor_redis_driver:
            from ate_notify_monitor.new_notifier.drivers.redis_driver import RedisMonitorDriver

            self.driver = RedisMonitorDriver(self.__logger)
        elif options.monitor_ddp_driver:
            from ate_notify_monitor.new_notifier.drivers.ddp_driver import DdpMonitorDriver

            self.driver = DdpMonitorDriver(self.__logger)

    def notify_fixture(self, fixture_id, status, progress=-1):
        """

        :param fixture_id:
        :param status: 'running', ''......
        :param progress: -1 if progress is unknown , 0-100 if progress is known
        :return:
        """
        return self.driver.notify(fixture_id, {})

    def notify_blocking_request(self, fixture_id, cavity=None, action=None, timeout=options.monitor_user_timeout):
        """

        :param fixture_id:
        :param cavity:
        :param action:
        :param timeout:
        :return:
        """
        self.driver.notify_blocking_request(fixture_id, cavity, action, timeout)


    def notify_cavity(self, fixture_id, cavity_id, status, test_name, atp_number, progress=-1):
        """

        :param fixture_id:
        :param cavity_id:
        :param status: 'running', 'fail', 'success'
        :param test_name: name of the running test
        :param atp_number:
        :param progress: -1 if progress is unknown , 0-100 if progress is known
        :return:
        """
        return self.driver.notify(fixture_id, {})

    def notify_resource(self, fixture_id, resource_id, status):
        return self.driver.notify(fixture_id, {})
