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

