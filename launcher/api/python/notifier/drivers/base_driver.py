__author__ = 'davidl'


class BaseMonitorDriver(object):
    def notify(self,fixture_id, info):
        print (info)

    def notify_blocking_request(self,fixture_id, info):
        print (info)
        return True
