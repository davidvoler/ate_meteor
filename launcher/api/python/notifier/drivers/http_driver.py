__author__ = 'davidl'
from ate_notify_monitor.new_notifier.drivers.base_driver import BaseMonitorDriver
import ate_notify_monitor.new_notifier.config
from tornado.options import options


class HttpMonitorDriver(BaseMonitorDriver):
    def __init__(self, logger):
        self.logger = logger
        self.monitor_http_host = options.monitor_http_host

    def notify(self, fixture_id, info):
        url = 'http://{}/wssrv/api/notification'.format(self.monitor_url)
        self.__logger.debug(url)

        status_list['fixture_id'] = fixture_id
        status_list['timestamp'] = time.time()

        # data = {'fixture_id': fixture_id,'status_list':status_list}
        headers = {'content-type': 'application/json'}
        # self.__logger.debug('url:  {}'.format( url))
        try:
            r = requests.post(url, data=json.dumps(status_list), headers=headers, timeout=5.0)
        except Exception as e:
            self.__logger.debug('updating monitor failed: {}'.format(str(e)))

    def notify_blocking_request(self, fixture_id, info):
        print (info)
        return True
