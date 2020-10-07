from pysnmp.hlapi import *

iterator = getCmd(SnmpEngine(),
                  UsmUserData('rskalban', 'cisco123',
                              'cisco123',
                              authProtocol=usmHMACMD5AuthProtocol,
                              privProtocol=usmAesCfb128Protocol),

                  UdpTransportTarget(('192.168.8.129', 161)),
                  ContextData(),
                  ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)))

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:  # SNMP engine errors
    print(errorIndication)
else:
    if errorStatus:  # SNMP agent errors
        print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex) - 1] if errorIndex else '?'))
    else:
        for varBind in varBinds:  # SNMP response contents
            print(' = '.join([x.prettyPrint() for x in varBind]))
