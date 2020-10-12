device_os_netmiko = {
    'Cisco IOS': 'cisco_ios',
    'Arista vEOS': 'arista_eos',
    'Cisco ASA': 'cisco_asa',
    'Cisco IOS-XE': 'cisco_xe',
    'Cisco IOS-XR': 'cisco_xr',
    'Cisco NX-OS': 'cisco_nxos',
    'Juniper Junos': 'juniper_junos',
    'Linux': 'linux'
}

device_os_napalm = {
    'Cisco IOS': 'ios',
    'Arista vEOS': 'eos',
    'Cisco IOS-XR': 'iosxr',
    'Cisco NX-OS': 'nxos',
    'Juniper Junos': 'junos',
}

discovery_protocol = 'LLDP'

snmp_auth_protocols = (
    'md5',
    'sha'
)
snmp_privacy_protocols = (
    'aes 128',
    'aes 192',
    'aes 256',
    '3des',
    'des'
)
