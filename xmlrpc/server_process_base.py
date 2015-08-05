import xmlrpclib
from tornado.options import options
from ate_logger import AteLogger


class BaseXmlRpcProcess(object):

    def __init__(self):
        self.logger = AteLogger('XmlRpcProcess')
        self._tf_status = False

    def status(self):
        self.logger.debug('Calling status')
        traceback = None
        try:
            c = xmlrpclib.ServerProxy('http://127.0.0.1:{}'.format(options.xmlrpc_server_port))
            process, tf, traceback = c.sys.status()
            self._tf_status = tf
            tf_health, _ = self._tf_health(force=False)
            xmlrpc = True
        except Exception as exc:
            process = False
            tf = False
            tf_health = {}
            xmlrpc = False
            traceback = str(exc)
            self.logger.warning("Can't access XML RPC")
        return {
            'error': traceback,
            'type': 'system',
            'result': [
                {'type': 'process', 'status': process, 'description': 'TF Server process'},
                {'type': 'xmlrpc', 'status': xmlrpc, 'description': 'TF Network connection'},
                {'type': 'test_fixture', 'status': tf, 'description': 'TF Object status'},
                {'type': 'test_fixture_health',
                 'status': tf_health.get('fixture_status', False),
                 'description': 'TF Hardware status'},
            ]
        }

    def _tf_health(self, force=False):
        self.logger.debug('Calling tf_health')
        traceback = None
        tf_health = {}
        if self._tf_status:
            try:
                c = xmlrpclib.ServerProxy('http://127.0.0.1:{}'.format(options.xmlrpc_server_port))
                tf_health = c.sys.tf_health(force)
            except Exception as exc:
                tf_health = {}
                traceback = str(exc)
                self.logger.warning("Can't access XML RPC")
        return tf_health, traceback

    def tf_health(self, force=False):
        tf_health, traceback = self._tf_health(force=force)
        return {
            'type': 'test_fixture_health',
            'error': traceback,
            'result': tf_health
        }

    def cavities(self):
        self.logger.debug('Calling cavities')
        traceback = None
        cavities_list = []
        tf_health, traceback = self._tf_health(force=False)
        cavities = tf_health.get('cavities', {})
        for cavity_name, cavity in cavities.items():
            cavity['name'] = cavity_name
            devices = cavity.get('devices', {})
            for key, device in devices.items():
                cavity['devices'][key].pop('error', 0)
                cavity['devices'][key].pop('traceback', 0)
            cavities_list.append(cavity)
        return {
            'type': 'cavities',
            'error': traceback,
            'result': cavities_list
        }
