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


def parse_and_save_to_database(devices, user):
    for device in devices:
        device_model = {
            'user': user,
            'system_description': device.system.system_description,
            'system_contact': device.system.system_contact,
            'system_name': device.system.system_name,
            'system_location': device.system.system_location,
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
                'interface_speed': intf.interface_speed,
                'interface_physical_addr': intf.interface_physical_addr,
                'interface_admin_status': intf.interface_admin_status,
                'interface_operational_status': intf.interface_operational_status,
                'interface_ip': intf.interface_ip
            }

            interface_model = DeviceInterface(**interface)
            interface_model.save()
