import napalm
import netmiko
import threading
from config_app.backend import general_functions
from queue import Queue


class ConnectionManager:
    def __init__(self, initial_config_data, login_params, available_hosts):
        self.initial_config_data = initial_config_data
        self.login_params = login_params
        self.available_hosts = available_hosts

    def __connect_and_configure_single(self, host, config_commands):
        output = list()
        login_params = self.login_params['netmiko']

        try:
            with netmiko.ConnectHandler(ip=host, **login_params) as net_connect:
                net_connect.enable(cmd='enable 15')
                output = net_connect.send_config_set(config_commands)
                output += net_connect.save_config()
                net_connect.disconnect()
        except Exception:
            pass
        return output

    def connect_and_configure_multiple(self, config_commands):
        threads_list = list()
        connection_que = Queue()

        for host in self.available_hosts:
            connect_thread = threading.Thread(
                target=lambda in_que, args: in_que.put(self.__connect_and_configure_single(host, config_commands)),
                args=(connection_que, [host, config_commands]))

            connect_thread.start()
            threads_list.append(connect_thread)

        conf_output = general_functions.get_thread_output(connection_que, threads_list)
        conf_output = list(filter(lambda single_conf_output: len(single_conf_output) > 0, conf_output))
        return conf_output if len(conf_output) > 0 else None

    def get_command_output(self):
        driver = napalm.get_network_driver(self.initial_config_data['system'].get('network_dev_os', 'ios'))
        login_params = self.login_params['napalm']

        threads_list = list()
        connection_que = Queue()

        for host in self.available_hosts:
            device = driver(hostname=host, **login_params)
            connect_thread = threading.Thread(
                target=lambda in_que, args: in_que.put(general_functions.connect_and_get_output(device)),
                args=(connection_que, device,))

            connect_thread.start()
            threads_list.append(connect_thread)

        command_output = general_functions.get_thread_output(connection_que, threads_list)
        command_output = list(filter(lambda data: data is not None, command_output))
        return command_output
