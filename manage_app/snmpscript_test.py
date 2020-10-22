from manage_app.static import lldp_defined_valuse
from easysnmp import Session

# Create an SNMP session to be used for all our requests
session = Session(hostname='192.168.8.31', version=3, security_level='auth_with_privacy', security_username='rskalban',
                  privacy_protocol='AES128', privacy_password='cisco12345', auth_protocol='MD5',
                  auth_password='Cisco123')

# You may retrieve an individual OID using an SNMP GET

# You may also specify the OID as a tuple (name, index)
# Note: the index is specified as a string as it can be of other types than
# just a regular integer
#
# # And of course, you may use the numeric OID too
#description = session.get('1.0.8802.1.1.2')
#
# # Set a variable using an SNMP SET
# # session.set('sysLocation.0', 'The SNMP Lab')
# print(description)
# Perform an SNMP walk
system_items = session.walk(lldp_defined_valuse['lldpRemoteSystemsData'])
print(system_items)

# Each returned item can be used normally as its related type (str or int)
# but also has several extended attributes with SNMP-specific information


# int_desc = list(filter(lambda snmp_var: snmp_var.oid == 'ifDescr', system_items))
# print(int_desc)

for item in system_items:
    print(item)

# for item in system_items:
#     mac_addr = ['{:02x}'.format(int(ord(val))) for val in item.value]
#     for i in range(2, 6, 3):
#         mac_addr.insert(i, '.')
#
#     mac_addr = ''.join(mac_addr)
#     print(mac_addr)

# TO DO - easy snmp dziala elegancko, pobiera poszczegolne MIBy.
# Teraz tylko zastanowic sie jak fajnie to wszystko ubrac w Manage Network tab...
