__author__ = 'davidl'
from tornado.options import define

define("monitor_http_driver", default=False, help='use http driver to send notification', type=bool)
define("monitor_redis_driver", default=False, help='use redis driver to send notification', type=bool)
define("monitor_ddp_driver", default=False, help='use ddp driver to send notification', type=bool)



define("monitor_http_host", default='', help='address of http server for notification', type=str)
define("monitor_http_timeout", default=60, help='http timeout in seconds', type=int)

define("monitor_redis_host", default='', help='address of redis server for notification', type=str)
define("monitor_redis_port", default=6379, help='address of redis server for notification', type=int)
define("monitor_redis_db", default=0, help='address of redis server for notification', type=int)

define("monitor_ddp_host", default='', help='address of ddp server for notification', type=str)


define("monitor_user_timeout", default=60, help='User response timeout in seconds', type=int)

