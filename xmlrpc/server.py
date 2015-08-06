"""
server.py
revision 11.05.2014
Multi threaded RPC server for selected TF class listening on port 9876
"""
import sys
sys.path.append(r'C:\CROW\ATE')
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
import inspect
import traceback
import tendo.singleton
import xmlrpclib
import copy

from xmlrpc.utils import load_config

load_config()

from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCDispatcher
from datetime import datetime, timedelta
from SocketServer import ThreadingMixIn
from xmlrpc.utilities import get_tf_class, set_tf_class
from ate_logger import AteLogger
from tornado.options import options
from threading import Event, Lock

######################################################################
# code
######################################################################
logger = AteLogger('XmlRpcServer')
logger.debug("Starting XML RPC server...")


class Server(ThreadingMixIn, SimpleXMLRPCServer):
    """Server class
    Multi threaded XML RPC Server, specific for TF Classes with added features:
    Listens on port 9876
    Function execution is timed
    """

    allow_reuse_address = True
    _event = Event()
    _health = {}
    _timestamp = datetime.now()
    _lock = Lock()
    _cavities = {}

    def __init__(self):
        self.port = options.xmlrpc_server_port
        SimpleXMLRPCServer.__init__(self, ('0.0.0.0', self.port), allow_none=True)

    def _dispatch(self, method, params):
        """Executes the requested method and measure how long it took

        :param method: method name
        :param params: method parameters
        :return: Returns a tuple: the method result and the measured time, unless it is a sys method,
        doesn't need to measure sys methods
        :raise xmlrpclib.Fault:
        """
        logger.info("CALL {}({})".format(method, ", ".join([repr(p) for p in params])))
        try:
            before = datetime.now()
            if params:
                cavity = None
                first = params[0]
                print type(first), first
                if isinstance(first, str):
                    print self._cavities
                    cavity = self._cavities.get(first, None)
                    print 'cavity is', cavity
                    if cavity is not None:
                        logger.set_tid(cavity)
                        logger.info('hahaha')
            result = SimpleXMLRPCDispatcher._dispatch(self, method, params)
            delta = datetime.now() - before
            delta = unicode('%s.%06d' % (delta.seconds, delta.microseconds))
            if not method.startswith('sys'):
                return result, delta
            else:
                return result
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = traceback.format_exc()
            msg = "%s: %s\n%s" % (exc_type, exc_value, tb)
            logger.exception("FAULT {}: {}".format(method, msg))
            raise xmlrpclib.Fault(1, msg)

    def start(self, tf_cls, tf_obj, tf_name, traceback_msg=None):
        """
        Test fixture initialization...
        :param tf_cls: The class object
        :param tf_obj: The instantiated class
        :param tf_name: Name of the class
        :param traceback_msg: If failed to instantiate the class the traceback will be given
        """

        def params(func_name):
            """Return the function parameters given its name

            ArgSpec(args=['a', 'b', 'x'], varargs=None, keywords=None, defaults=('blah',))
            print(inspect.getargspec(getattr(tf_cls, func_name)))
            http://docs.python.org/2/library/inspect.html#inspect.getargspec


            :param func_name: Method name in the current TF class
            :return: dict where each key is the argument name,
             key value is the default value for the argument when present, if not value is '' (empty string)
            """
            args, varargs, keywords, defaults = inspect.getargspec(getattr(tf_cls, func_name))
            if 'self' in args:
                args.remove('self')
            if defaults is None:
                defaults = ['' for _ in range(len(args))]
                # defaults = []
            else:
                defaults = list(defaults)  # because it is a tuple and we need to manipulate it
            diff = len(args) - len(defaults)
            defaults.extend(['' for _ in range(diff)])
            defaults.reverse()
            ordered = []
            for idx, val in enumerate(args):
                ordered.append((val, defaults[idx]))
            return ordered
            # return {args[i]: defaults[i] for i in range(len(args))}
            # dict where the key is the arg name and it's default value when present, else ''

        def srv_forever():
            """
            Set server work in background
            """
            tf_cavities()
            while True:
                self.handle_request()

        def doc(func_name):
            """Return the method docstring in the loaded TF class

            :param func_name: Method name
            :return: Docstring or empty string if method doesn't have
            """
            the_doc = getattr(tf_cls, func_name).__doc__
            if the_doc is None:
                return ''
            return the_doc

        def name():
            """Return loaded TF class name
            """
            return tf_name

        def info():
            """Returns general info on the loaded class, web interface uses this to fill the Class info panel
            """
            return tf_name, tf_cls.__doc__

        def status():
            return tf_name, traceback_msg is None, '' if traceback_msg is None else traceback_msg

        def tf_health(force):
            if not self._event.is_set():
                logger.debug('TF not under test and force is {}'.format(force))
                now = datetime.now()
                if force is True or now - self._timestamp > timedelta(seconds=30):
                    logger.debug('Trying to fetch real data from TF class')
                    health = tf_obj.tf_health()
                    with self._lock:
                        self._timestamp = datetime.now()
                        self._health = health
                    return health
            logger.debug('TF under test and force is {}'.format(force))
            logger.debug('Return cached data')
            with self._lock:
                health = copy.deepcopy(self._health)
            return health

        def tf_cavities():
            if tf_obj is None:
                cavities = {}
            else:
                cavities = tf_obj.tf_cavities()
            self._cavities = {cavity: str(idx + 1) for idx, cavity in enumerate(cavities)}
            return cavities

        def _shutdown():
            """Just calls super shutdown method, overloaded here to add logging
            """
            logger.info("Shutdown requested...")
            os._exit(1)  # TODO: Implement clean and fast way to shutdown the server
            # self.shutdown()
            return True

        def set_execution_key(execution_id):
            logger.set_execution_key(execution_id)
            self._event.set()

        def drop_execution_key():
            logger.set_execution_key('')
            self._event.clear()

        def set_cavity_info(cav_info):
            logger.info(cav_info)
            for cav_name, cav_params in cav_info.items():
                uid, serial = cav_params
                logger.info('cavity {} sn {} uid {}'.format(cav_name, serial, uid))
                logger.set_cavity_info(int(cav_name), serial, uid)

        def drop_cavity_info():
            return logger.drop_cavity_info()

        def set_class(class_name):
            """Change the class name in configuration file and shutdown so RPC can reload with new class
            """
            return set_tf_class(class_name)

        def methods():
            """Get a list of methods available to call in the loaded TF class
            """
            print self.system_listMethods()
            return {func_name: {'doc': doc(func_name), 'params': params(func_name)} for func_name in
                    self.system_listMethods() if not (func_name.startswith('sys') or func_name == 'Cavity')}

        logger.info("Listening on port {}".format(self.port))
        logger.set_cavity_info('1', sn='123131', uid='129038123901278301')
        self.register_introspection_functions()
        self.register_function(set_class, 'sys_setclass')
        if tf_obj is not None:
            self.register_instance(tf_obj)
            self.register_function(params, 'sys.params')
            self.register_function(name, 'sys.name')
            self.register_function(doc, 'sys.doc')
            self.register_function(info, 'sys.info')
            self.register_function(methods, 'sys_myinspect')
            self.register_function(tf_health, 'sys.tf_health')
            self.register_function(tf_cavities, 'sys.tf_cavities')
            self.register_function(set_execution_key, 'sys.set_execution_key')
            self.register_function(drop_execution_key, 'sys.drop_execution_key')
            self.register_function(set_cavity_info, 'sys.set_cavity_info')
            self.register_function(drop_cavity_info, 'sys.drop_cavity_info')
            self.register_function(info, 'sys.info')
        self.register_function(status, 'sys.status')
        srv_forever()


def import_class(class_object):
    """
    Import a class given a string with its name in the format module.module.classname
    """
    d = class_object.rfind(".")
    class_name = class_object[d + 1:len(class_object)]
    m = __import__(class_object[0:d], globals(), locals(), [class_name])
    return getattr(m, class_name)


def main():
    """
    Entry point
    """
    logger.info('Starting RPC server on {}'.format(sys.platform))
    cls_name = get_tf_class()
    logger.info('TF Class name:{}'.format(cls_name))

    server = Server()
    msg = None

    try:
        cls = import_class(cls_name)
        if not hasattr(cls, 'tf_health'):
            raise Exception('TF Class has no tf_basic_info method defined')
        tf = cls()
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.format_exc()
        msg = "%s: %s\n%s" % (exc_type, exc_value, tb)
        logger.error(msg)
        logger.exception(e)
        tf = None
        cls = None
    finally:
        server.start(cls, tf, cls_name, traceback_msg=msg)


if __name__ == '__main__':
    me = tendo.singleton.SingleInstance()
    main()
