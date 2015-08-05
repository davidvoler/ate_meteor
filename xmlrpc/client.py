__author__ = 'avraham'

from xmlrpclib import ServerProxy
port = 9876


class Client(ServerProxy):
    def __init__(self, ip='127.0.0.1'):
        ServerProxy.__init__(self, ('http://{}:{}'.format(ip, port)))

    def get_methods(self):
            return [x for x in self.system.listMethods() if not x.startswith('sys')]
