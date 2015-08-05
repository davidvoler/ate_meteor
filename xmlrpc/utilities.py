__author__ = 'davidl'

import pprint
from utils import get_driver
from tornado.options import options
from xmlrpc.server_process import get_xml_process


def xmlrpc_start():
    server = get_xml_process()
    return server.start()


def xmlrpc_stop():
    server = get_xml_process()
    return server.stop()


def xmlrpc_restart():
    server = get_xml_process()
    return server.restart()


def system_status():
    """
    use this format to pass status information
    icons can come from this site
    http://materialdesignicons.com/
    remember to add mdi- as prefix
    :return:
    """
    server = get_xml_process()
    status = server.status()
    return {
        'type': 'system_status',
        'error': status['error'],
        'result': status['result']
    }


def tf_health_status(force=False):
    """
    use this format to pass status information
    icons can come from this site
    http://materialdesignicons.com/
    remember to add mdi- as prefix
    :param force: if true forces tf_health rescan
    :type force: bool
    :return:
    """
    server = get_xml_process()
    status = server.tf_health(force)
    status.pop('cavities', 0)
    return {
        'type': 'test_fixture_health',
        'error': status['error'],
        'result': status['result']
    }


def cavity_status():
    """
    use this format to pass status information
    icons can come from this site
    http://materialdesignicons.com/
    remember to add mdi- as prefix
    :return:
    """
    server = get_xml_process()
    status = server.cavities()
    return {
        'type': 'cavity_status',
        'error': status['error'],
        'result': status['result']
    }


def get_tf_class():
    storage = get_driver(options.storage_driver)
    tf_info = storage.get_tf_info()
    if not tf_info['class_path']:
        print('Test Fixture Class is not defined please use admin to set class')
        exit(0)
    return tf_info['class_path']


def set_tf_class(cls_name):
    storage = get_driver(options.storage_driver)
    tf_info = storage.get_tf_info()
    tf_info['class_path'] = cls_name
    tf_info = storage.set_tf_info(tf_info)
