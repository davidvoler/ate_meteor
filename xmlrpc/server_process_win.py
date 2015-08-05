import subprocess
from server_process_base import BaseXmlRpcProcess

SERVICE_NAME = 'tfe_xmlrpc_server'


def service_installed():
    cmd = 'sc query {}'.format(SERVICE_NAME)
    try:
        subprocess.check_output(cmd.split())
        return True
    except subprocess.CalledProcessError:
        return False


class XmlRpcProcess(BaseXmlRpcProcess):

    def is_running(self):
        running = False
        cmd = 'sc query {}'.format(SERVICE_NAME)
        output = subprocess.check_output(cmd.split())
        for line in output.splitlines():
            line = line.strip()
            tmp = line.split()
            if tmp:
                if tmp[0] == 'STATE':
                    running = True if tmp[-1] == 'RUNNING' else False
        return running

    def start(self):
        if self.is_running():
            self.logger.warning('service already running')
            return False

        cmd = 'net start {}'.format(SERVICE_NAME)
        exit_code = subprocess.call(cmd.split())
        if exit_code == 0:
            self.logger.info('server is running')
        else:
            self.logger.error('unable to run server')
        return exit_code == 0

    def stop(self):
        if not self.is_running():
            self.logger.warning('service already stopped')
            return False

        cmd = 'net stop {}'.format(SERVICE_NAME)
        exit_code = subprocess.call(cmd.split())
        if exit_code == 0:
            self.logger.info('server was stopped')
        else:
            self.logger.warning('unable stop server')
        return exit_code == 0

    def restart(self):
        if self.start():
            return self.stop()
        else:
            return False
