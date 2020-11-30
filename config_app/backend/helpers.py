import json
import ipcalc
import subprocess
import threading
import logging
from queue import Queue

from config_app.models import AvailableDevices


def convert_mask(config):
    """
    Function which creates a subnet object from given network IP and CIDR string.

    Positional arguments:
    - config -- dictionary with device parameters

    Returns:
    - subnet -- ipcalc.Network object
    """
    network_ip = config['ip_range'].get('network_ip')
    cidr = config['ip_range'].get('subnet')

    subnet = "{network_ip}/{cidr}".format(network_ip=network_ip, cidr=cidr)
    subnet = ipcalc.Network(subnet)

    return subnet


def ping_ip(current_ip_address):
    """
    Function which sends three ICMP packets to specified destination.

    Positional arguments:
    - current_ip_address -- destination IP to which ICMP packets are send

    Returns:
    - current_ip_address -- boolean value of device reachability
    """

    try:
        output = subprocess.check_output("ping -{} 3 {}".format('c', current_ip_address), shell=True,
                                         universal_newlines=True)
        if 'unreachable' in output:
            return current_ip_address, False
        else:
            return current_ip_address, True
    except Exception as e:
        logging.warning(e)
        return current_ip_address, False


def ping_all(config):
    """
    Function which spawns multiple threads to check IP connectivity by using ping_ip function.

    Positional arguments:
    - config -- dictionary with device parameters

    Returns:
    - pingable_ips -- list of reachable IPs
    """
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
    """
    Helper function which retrieves output from multiple threads.

    Positional arguments:
    - que_object -- Queue object in which all output threads are based
    - threads_list -- list with all Thread objects

    Returns:
    - thread_outputs -- list of thread outputs
    """
    thread_outputs = list()
    for thread in threads_list:
        thread.join()

    while not que_object.empty():
        result = que_object.get()
        thread_outputs.append(result)
    return thread_outputs


def connect_and_get_output(device):
    """
    Helper function which get LLDP data from specified device

    Positional argument:
    - device -- NAPALM driver object

    Returns:
    - json_output -- LLDP device data serialized to JSON
    """
    try:
        device.open()
        output = device.get_lldp_neighbors_detail()
        device.close()
    except Exception as exception:
        logging.warning(exception)
    else:
        json_output = json.dumps(output, indent=5)
        return json_output


def get_available_devices():
    """
    Helper function which returns network IP addresses list from AvailableDevices database table.
    """
    return [host.network_address for host in AvailableDevices.objects.all()]
