from base_handler import BaseHandler
from bson.json_util import dumps, loads
from utils import get_mongodb_connection
import uuid
import datetime


class LaunchHandler(BaseHandler):
    def get(self):
        connection = get_mongodb_connection()
        db = connection['launcher']
        self.write(dumps({'status': 0,
                          'data': db['execution'].find()}))

    def post(self):
        """
        launch execution
        :return:
        """

        execution_key = str(uuid.uuid4())
        info = loads(self.request.body.decode("utf-8"))
        execution_doc = {'_id': execution_key,'uuts':[],'start':datetime.datetime.now(),'status':'init'}
        for uut in info['uuts']:
            uut_key= str(uuid.uuid4())
            execution_doc['uuts'].append({'key':uut_key,'name':uut['name'],'status':'init','info':uut})
        connection = get_mongodb_connection()
        db = connection['launcher']
        db['execution'].insert(execution_doc)
        self.write(dumps({'status': 0,
                          'data': db['execution'].find()}))

    def put(self):
        """
        update execution status
        :return:
        """
        execution_key = str(uuid.uuid4())
        self.write(dumps({'status': 0,
                          'data': 'a list of tasks that have been launched'}))

    def delete(self):
        """
        Stop running execution
        :return:
        """
        self.write(dumps({'status': 0,
                          'data': 'a list of tasks that have been launched'}))
        self.render('web/index.html')
