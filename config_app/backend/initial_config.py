import napalm
import netmiko
import threading
from config_app.backend import static, general_functions
from queue import Queue


class Config:
    def __init__(self, initial_config_data, login_params):
        self.initial_config_data = initial_config_data
        self.login_params = login_params
        self.available_hosts = general_functions.ping_all(self.initial_config_data)

    def __connect_and_configure(self, host, config_commands):
        output = list()
        login_params = self.login_params['netmiko']

        try:
            with netmiko.ConnectHandler(ip=host, **login_params) as net_connect:
                net_connect.enable(cmd='enable 15')
                output = net_connect.send_config_set(config_commands)
                output += net_connect.save_config()
                net_connect.disconnect()
        except:
            pass
        return output

    def conf_disc_proto(self):
        threads_list = list()
        que = Queue()

        config_commands = [
            'lldp run',
        ]

        for host in self.available_hosts:
            connect_thread = threading.Thread(
                target=lambda q, args: q.put(self.__connect_and_configure(host, config_commands)),
                args=(que, [host, config_commands]))

            connect_thread.start()
            threads_list.append(connect_thread)

        conf_output = general_functions.get_thread_output(que, threads_list)
        conf_output = list(filter(lambda c_output: len(c_output) > 0, conf_output))
        return conf_output if len(conf_output) > 0 else None

    def get_disc_details(self):
        driver = napalm.get_network_driver(self.initial_config_data['system'].get('network_dev_os', 'ios'))
        login_params = self.login_params['napalm']

        threads_list = list()
        que = Queue()

        for host in self.available_hosts:
            device = driver(hostname=host, **login_params)
            connect_thread = threading.Thread(
                target=lambda q, args: q.put(general_functions.connect_and_get_neighbors(device)), args=(que, device,))

            connect_thread.start()
            threads_list.append(connect_thread)

        discovery_data = general_functions.get_thread_output(que, threads_list)
        discovery_data = list(filter(lambda data: data is not None, discovery_data))
        return discovery_data


# #
# initial_config = Config(static.config, static.login_params)
# #
# cf_output = initial_config.conf_disc_proto()
# # dsc_details = initial_config.get_disc_details()
# #
# # for output in cf_output:
# #     print(output)
# #
# # for details in dsc_details:
# #     print(details)
