from manage_app.models import DeviceTrapModel, VarBindModel, DeviceModel, DeviceInterface

from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
from pyasn1.codec.ber import decoder
from pysnmp.proto import api

import logging
from datetime import datetime


class TrapEngine:
    def __init__(self, snmp_host, snmp_host_port):
        self.snmp_host = snmp_host
        self.snmp_host_port = snmp_host_port

        self.udp_domain_name = udp.domainName
        self.udp_socket_transport = udp.UdpSocketTransport

    @staticmethod
    def _receive_and_save(transportDispatcher, transportDomain, transportAddress, wholeMsg):
        logging.basicConfig(format='!!! %(asctime)s %(message)s')

        while wholeMsg:

            msgVer = int(api.decodeMessageVersion(wholeMsg))
            if msgVer in api.protoModules:
                pMod = api.protoModules[msgVer]

            else:
                logging.warning('Unsupported SNMP version %s' % msgVer)
                return

            reqMsg, wholeMsg = decoder.decode(
                wholeMsg, asn1Spec=pMod.Message(),
            )

            logging.warning('########## RECEIVED NEW TRAP ########## ')
            logging.warning('Notification message from %s:%s: ' % (transportDomain,
                                                                   transportAddress))

            reqPDU = pMod.apiMessage.getPDU(reqMsg)
            if reqPDU.isSameTypeWith(pMod.TrapPDU()):
                if msgVer == api.protoVersion1:
                    trap_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    trap_domain = transportDomain
                    trap_address = transportAddress
                    trap_enterprise = pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                    trap_agent_address = pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                    trap_generic = pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                    trap_uptime = pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()

                    logging.warning('Enterprise: {trap_enterprise}'.format(trap_enterprise=trap_enterprise))
                    logging.warning('Agent Address: {trap_agent_address}'.format(trap_agent_address=trap_agent_address))
                    logging.warning('Generic Trap: {trap_generic}'.format(trap_generic=trap_generic))
                    logging.warning('Uptime: {trap_uptime}'.format(trap_uptime=trap_uptime))

                    device_interface = DeviceInterface.objects.filter(interface_ip=trap_agent_address)[0]

                    trap_model_parameters = {
                        'device_model': device_interface.device_model,
                        'trap_domain': trap_domain,
                        'trap_address': trap_address,
                        'trap_enterprise': trap_enterprise,
                        'trap_agent_address': trap_agent_address,
                        'trap_generic': trap_generic,
                        'trap_uptime': trap_uptime,
                        'trap_date': trap_date
                    }
                    trap_model = DeviceTrapModel(**trap_model_parameters)
                    trap_model.save()
                    varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)

                    for trap_oid, trap_data in varBinds:
                        var_bids_parameters = {
                            'trap_model': trap_model,
                            'trap_oid': trap_oid,
                            'trap_data': trap_data
                        }

                        var_bids_model = VarBindModel(**var_bids_parameters)
                        var_bids_model.save()

                else:
                    varBinds = pMod.apiPDU.getVarBinds(reqPDU)

                logging.warning('Var-binds:')
                for oid, val in varBinds:
                    logging.warning('%s = %s' % (oid, val))

        return wholeMsg

    def _initialize_engine(self):
        self.transport_dispatcher = AsyncoreDispatcher()
        self.transport_dispatcher.registerRecvCbFun(self._receive_and_save)
        self.transport_dispatcher.registerTransport(self.udp_domain_name,
                                                    self.udp_socket_transport().openServerMode(
                                                        (self.snmp_host, self.snmp_host_port)))
        self.transport_dispatcher.jobStarted(1)

    def run_engine(self):
        self._initialize_engine()
        self.transport_dispatcher.runDispatcher()

    def close_engine(self):
        self.transport_dispatcher.closeDispatcher()
