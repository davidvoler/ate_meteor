from home.home_handler import HomeHandler
from launcher.launch_handler import LaunchHandler
from status.status_handler import StatusHandler
url_handlers = [
    (r'/', HomeHandler),
    (r'/api/launch', LaunchHandler),
    (r'/api/status', StatusHandler),
]
