import sys

xml_rpc_process = None

if sys.platform == 'win32':
    from server_process_win import service_installed
    if service_installed():
        from server_process_win import XmlRpcProcess
    else:
        from server_process_python import XmlRpcProcess
else:
    from xmlrpc.server_process_linux import service_installed
    if service_installed():
        from server_process_linux import XmlRpcProcess
    else:
        from server_process_python import XmlRpcProcess


def get_xml_process():
    global xml_rpc_process
    if xml_rpc_process is None:
        xml_rpc_process = XmlRpcProcess()
        print type(xml_rpc_process)
    return xml_rpc_process
