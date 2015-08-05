
from tornado.options import define, options


define('mongodb', default='localhost:27017', help='mongodb host name or ip address +port', type=str)
define('app_port', default=7919, help='application port', type=int)

