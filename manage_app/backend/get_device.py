from easysnmp import Session
from manage_app.backend import parse_model
from manage_app.models import DeviceModel, DeviceInterface


class DeviceManager:
    def __init__(self, available_hosts, snmp_config_id):
        self.host = available_hosts
        self.snmp_config_id = snmp_config_id
        self.session_parameters = parse_model.parse_to_session_parameters(self.snmp_config_id)

    def get_device_details(self, hostname):
        session = Session(hostname=hostname, **self.session_parameters)
        device = DeviceSystem_(session)
        return device


class DeviceSystem_:
    def __init__(self, session):
        self.session = session
        self.system_description = session.get(('sysDescr', '0')).value
        self.system_contact = session.get(('sysContact', 0)).value
        self.system_name = session.get(('sysName', 0)).value
        self.system_location = session.get(('sysLocation', 0)).value

# class DeviceInterface_:
#     def __init__(self, session):
#         self.session = session
#         self.interface_
