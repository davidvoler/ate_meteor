from server_process_base import BaseXmlRpcProcess
import subprocess

SERVICE_NAME = 'xml_rpc_server'

def service_installed():
    exit_code = subprocess.call(['supervisorctl',SERVICE_NAME,'status' ])
    return exit_code == 0


class XmlRpcProcess(BaseXmlRpcProcess):

    def is_running(self):
        running = False
        cmd = 'supervisorctl status {}'.format(SERVICE_NAME)
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

        cmd = 'supervisorctl start {}'.format(SERVICE_NAME)
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

        cmd = 'supervisorctl start {}'.format(SERVICE_NAME)
        exit_code = subprocess.call(cmd.split())
        if exit_code == 0:
            self.logger.info('server was stopped')
        else:
            self.logger.warning('unable stop server')
        return exit_code == 0

    def restart(self):
        cmd = 'supervisorctl restart {}'.format(SERVICE_NAME)
        exit_code = subprocess.call(cmd.split())
        if exit_code == 0:
            self.logger.info('server was stopped')
        else:
            self.logger.warning('unable stop server')
        return exit_code == 0