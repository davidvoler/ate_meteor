
from tornado.options import define, options


define('mongo_db_host', default='localhost:27017', help='mongodb host name or ip address +port', type=str)
define('mongo_db_name', default='ate_meteor', help='database name', type=str)
define('app_port', default=7919, help='application port', type=int)

