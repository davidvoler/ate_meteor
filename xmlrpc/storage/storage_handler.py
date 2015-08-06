from base_handler import BaseHandler
from tornado.options import options
from bson.json_util import dumps, loads
from utils import get_logger, get_driver

class StorageHandler(BaseHandler):
    def initialize(self):
        self.logger = get_logger('StorageHandler')
        self._storage = get_driver(options.storage_driver)

    def get(self):
        key = self.get_argument('key', None)
        val = self._storage.get_object(key)
        self.write(dumps(val))

    def post(self):
        data = loads(self.request.body.decode("utf-8"))
        val = self._storage.create_object(data['key'],data['value'])
        self.write(dumps({
            'status':0,
            'data':val
        }))

    def delete(self):
        key = self.get_argument('key', None)
        res = self._storage.delete_object(key)
        self.write(dumps({
            'status':0,
            'data':res
        }))