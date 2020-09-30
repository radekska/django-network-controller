import json
import ipcalc
import subprocess
import threading
from queue import Queue


def convert_mask(config):
    network_ip = config['ip_range'].get('network_ip')
    cidr = config['ip_range'].get('subnet')

    subnet = "{network_ip}/{cidr}".format(network_ip=network_ip, cidr=cidr)
    subnet = ipcalc.Network(subnet)

    return subnet


def ping_ip(current_ip_address):
    try:
        output = subprocess.check_output("ping -{} 3 {}".format('c', current_ip_address), shell=True,
                                         universal_newlines=True)
        if 'unreachable' in output:
            return current_ip_address, False
        else:
            return current_ip_address, True

    except Exception:
        return current_ip_address, False


def ping_all(config):
    subnet = convert_mask(config)

    threads_list = list()
    que = Queue()

    for host in subnet:
        host = str(host)
        ping_thread = threading.Thread(target=lambda q, arg1: q.put(ping_ip(arg1)), args=(que, host))
        ping_thread.start()
        threads_list.append(ping_thread)

    pingable_ips = get_thread_output(que, threads_list)

    pingable_ips = filter(lambda ip_tuple: ip_tuple[1] is True, pingable_ips)
    pingable_ips = [ip_tuple[0] for ip_tuple in pingable_ips]
    return pingable_ips


def get_thread_output(que_object, threads_list):
    thread_outputs = list()
    for thread in threads_list:
        thread.join()

    while not que_object.empty():
        result = que_object.get()
        thread_outputs.append(result)
    return thread_outputs


def connect_and_get_neighbors(device):
    try:
        device.open()
        output = device.get_lldp_neighbors_detail()
        device.close()
    except:
        pass
    else:
        json_output = json.dumps(output, indent=5)
        return json_output
