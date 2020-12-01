import logging
from celery import shared_task

from .TrapEngine import TrapEngine
from .static import snmp_host_port


@shared_task
def run_trap_engine(snmp_host, snmp_config):
    """
    This function creates a Celery Trap Engine task in order to run it in parallel to main django app process.

    Positional Arguments:
    - snmp_host -- destination IP address for SNMP traps
    - snmp_config -- SNMP configuration details for accessing device
    """
    my_trap_engine = TrapEngine(snmp_host, snmp_host_port, snmp_config)
    try:
        my_trap_engine.run_engine()
    except Exception as exception:
        logging.basicConfig(format='!!! %(asctime)s %(message)s')
        logging.warning(exception)

        my_trap_engine.close_engine()
