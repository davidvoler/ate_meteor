import os
from tornado.options import define, options


define('mongodb', default='localhost:27017', help='mongodb host name or ip address +port', type=str)
define('xmlrpc_server_port', default=9876, help='xmlrpc server port', type=int)

db_dir = os.path.join(os.path.dirname(__file__), '..')
define("storage_file_name", default="{}/tf_storage.db".format(db_dir), help='local db file name', type=str)
define('storage_driver', default='storage.storage_driver.StorageDriver', help='Storage driver', type=str)
