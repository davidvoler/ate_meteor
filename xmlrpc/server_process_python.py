import os
import subprocess
import time
import psutil
from server_process_base import BaseXmlRpcProcess


class XmlRpcProcess(BaseXmlRpcProcess):

    def __init__(self):
        super(XmlRpcProcess, self).__init__()
        self.server = None

    def start(self):
        server_path = os.path.dirname(__file__)
        if self.server is None:
            self.server = subprocess.Popen(['python', '{}/server.py'.format(server_path)])
            self.logger.info('server is running - pid:{}'.format(self.server.pid))
            time.sleep(5)
            if self.server.poll() is None:
                return True
            else:
                self.logger.error('unable to run server - pid:{}'.format(self.server.pid))
                self.server = None
                return False
        self.logger.warning('server already running - pid:{}'.format(self.server.pid))
        return True

    def stop(self):
        if self.server is not None:
            self.server.kill()
            self.logger.info('XMLRPCServer was stopped - pid:{}'.format(self.server.pid))
            self.server = None
        else:
            self.logger.warning('server already stopped')
        return True

    def restart(self):
        self.logger.info('restart xml rpc server')
        self.stop()
        time.sleep(1)  # Sleep for one second
        if not self.start():
            return False
        return True

    def is_running(self):
        if self.server is not None:
            pid_exist = psutil.pid_exists(self.server.pid)
        else:
            pid_exist = False
        return pid_exist
