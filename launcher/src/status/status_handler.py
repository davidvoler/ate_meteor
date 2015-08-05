from base_handler import BaseHandler
from bson.json_util import dumps, loads
from utils import get_mongodb_connection

class StatusHandler(BaseHandler):
    def get(self):
        connection = get_mongodb_connection()
        db = connection['launcher']
        self.write(dumps({'status':0,
                          'data':db['tasks'].find()}))

    def post(self):
        """
        launch execution
        :return:
        """
        self.write(dumps({'status':0,
                          'data':'a list of tasks that have been launched'}))
        self.render('web/index.html')


