import re
import logging
from datetime import datetime, timedelta
from manage_app.models import DeviceModel, DeviceInterface
from config_app.models import SNMPConfigParameters


def parse_to_session_parameters(snmp_config_id):
    snmp_config = SNMPConfigParameters.objects.filter(id=snmp_config_id)[0]
    snmp_session_parameters = {
        'version': 3,
        'security_level': 'auth_with_privacy',
        'security_username': snmp_config.snmp_user,
        'privacy_protocol': snmp_config.snmp_privacy_protocol.replace(' ', ''),
        'privacy_password': snmp_config.snmp_encrypt_key,
        'auth_protocol': snmp_config.snmp_auth_protocol,
        'auth_password': snmp_config.snmp_password
    }

    return snmp_session_parameters


def parse_mac_address(mac_address):
    mac_address = ['{:02x}'.format(int(ord(val))) for val in mac_address]
    for i in range(2, 6, 3):
        mac_address.insert(i, '.')

    mac_address = ''.join(mac_address)

    return mac_address if mac_address != '..' else "None"


def parse_up_time(system_ticks):
    dt = datetime.now() - timedelta(microseconds=int(system_ticks) * 10000)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt


def save_to_database_lldp_data(lldp_neighbor_details):
    current_device = DeviceModel.objects.filter(full_system_name=lldp_neighbor_details['lldp_local_hostname'])[0]
    current_interfaces = DeviceInterface.objects.filter(device_model=current_device)

    current_interface = current_interfaces.filter(interface_description=lldp_neighbor_details['lldp_local_interface'])[
        0]
    current_interface.lldp_neighbor_hostname = lldp_neighbor_details['lldp_neighbor_hostname']
    current_interface.lldp_neighbor_interface = lldp_neighbor_details['lldp_neighbor_interface']

    current_interface.save()


def format_lldp_data(devices):
    all_lldp_data = dict()
    for device in devices:
        for key, value in device.lldp_data.items():
            all_lldp_data.setdefault(key, []).append(value)

    for device in devices:
        lldp_local_hostname = device.system.full_system_name  # CoreSwitch1
        lldp_neighbor_correlations = all_lldp_data[lldp_local_hostname][0]

        for lldp_neighbor_interface, lldp_neighbor_hostname in lldp_neighbor_correlations.items():
            lldp_neighbor = all_lldp_data[lldp_neighbor_hostname]

            for iner_lldp_neighbor_intf, iner_lldp_neighbor_host in lldp_neighbor[0].items():
                if iner_lldp_neighbor_host == lldp_local_hostname:
                    lldp_neighbor_details = {
                        'lldp_local_hostname': lldp_local_hostname,
                        'lldp_local_interface': iner_lldp_neighbor_intf,
                        'lldp_neighbor_interface': lldp_neighbor_interface,
                        'lldp_neighbor_hostname': lldp_neighbor_hostname

                    }
                    save_to_database_lldp_data(lldp_neighbor_details)


def parse_and_save_to_database(devices, user):
    for device in devices:
        splitted_system_description = device.system.system_description.split(',')
        system_image = splitted_system_description[1].strip().split(' ')[-1].capitalize().replace('(', '').replace(
            ')', '')
        device_type = 'Router' if 'l2' not in system_image else 'Switch'

        device_model = {
            'user': user,
            'system_description': device.system.system_description,
            'system_type': splitted_system_description[0],
            'system_image': system_image,
            'system_version': splitted_system_description[2].replace('Version', '').strip(),
            'system_contact': device.system.system_contact,
            'full_system_name': device.system.full_system_name,
            'system_name': device.system.full_system_name.split('.')[0],
            'system_location': device.system.system_location,
            'system_up_time': parse_up_time(device.system.system_up_time),
            'if_number': device.if_number,
            'device_type': device_type
        }

        dev_model = DeviceModel(**device_model)
        dev_model.save()

        matched_list = list()

        for intf in device.interfaces:
            matched = re.findall('^N', intf.interface_name)
            matched_list.append(matched)

            if not matched:
                interface = {
                    'user': user,
                    'device_model': dev_model,
                    'interface_name': intf.interface_name,
                    'interface_description': intf.interface_description,
                    'interface_mtu': intf.interface_mtu,
                    'interface_speed': intf.interface_speed[:-3],
                    'interface_physical_addr': parse_mac_address(intf.interface_physical_addr),
                    'interface_admin_status': 'Up' if intf.interface_admin_status == '1' else 'Down',
                    'interface_operational_status': 'Up' if intf.interface_operational_status == '1' else 'Down',
                    'interface_in_unicast_packets': intf.interface_in_unicast_packets,
                    'interface_in_errors': intf.interface_in_errors,
                    'interface_out_unicast_packets': intf.interface_out_unicast_packets,
                    'interface_out_errors': intf.interface_out_errors,
                    'interface_ip': intf.interface_ip
                }

                interface_model = DeviceInterface(**interface)
                interface_model.save()

        real_inf_number = dev_model.if_number - len(list(filter(lambda item: len(item) > 0, matched_list)))
        dev_model.if_number = real_inf_number
        dev_model.save()

    format_lldp_data(devices)


def parse_trap_model(device_trap_models, trap_data):

    for trap_model in device_trap_models:
        filtered_trap_data = trap_data.filter(trap_model=trap_model)

        string_data = list()
        for trap in filtered_trap_data:
            try:
                int(trap.trap_data)
            except ValueError as exception:
                # logging.warning('Parsing wanted exception: {exception}'.format(exception=exception))
                string_data.append(str(trap.trap_data))

        string_data = ', '.join(string_data[1:])

        trap_model.trap_string_data = string_data
        trap_model.save()
