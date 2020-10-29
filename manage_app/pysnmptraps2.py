# python snmp trap receiver
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

snmpEngine = engine.SnmpEngine()

TrapAgentAddress = '192.168.8.106'  # Trap listerner address
Port = 162  # trap listerner port

print("Agent is listening SNMP Trap on " + TrapAgentAddress + " , Port : " + str(Port))
print('--------------------------------------------------------------------------')
config.addTransport(
    snmpEngine,
    udp.domainName + (1,),
    udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
)

# Configure community here

config.addV1System(snmpEngine, 'password123', 'public')


def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
          varBinds, cbCtx):
    print("Received new Trap message")
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1)

try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
