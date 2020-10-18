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
    return mac_address


def parse_up_time(system_ticks):
    dt = datetime.now() - timedelta(microseconds=int(system_ticks) * 10000)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt


def parse_and_save_to_database(devices, user):
    for device in devices:
        splitted_system_description = device.system.system_description.split(',')
        device_model = {
            'user': user,
            'system_description': device.system.system_description,
            'system_type': splitted_system_description[0],
            'system_image': splitted_system_description[1].strip().split(' ')[-1].capitalize().replace('(', '').replace(
                ')', ''),
            'system_version': splitted_system_description[2].replace('Version', '').strip(),
            'system_contact': device.system.system_contact,
            'system_name': device.system.system_name,
            'system_location': device.system.system_location,
            'system_up_time': parse_up_time(device.system.system_up_time),
            'if_number': device.if_number
        }
        dev_model = DeviceModel(**device_model)
        dev_model.save()

        for intf in device.interfaces:
            interface = {
                'user': user,
                'device_model': dev_model,
                'interface_name': intf.interface_name,
                'interface_description': intf.interface_description,
                'interface_mtu': intf.interface_mtu,
                'interface_speed': intf.interface_speed[:-3],
                'interface_physical_addr': parse_mac_address(intf.interface_physical_addr),
                'interface_admin_status': 'Up' if intf.interface_admin_status == '1' else 'Down',
                'interface_operational_status': intf.interface_operational_status,
                'interface_ip': intf.interface_ip
            }

            interface_model = DeviceInterface(**interface)
            interface_model.save()
