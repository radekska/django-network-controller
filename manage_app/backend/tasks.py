import logging

# from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .TrapEngine import TrapEngine
from .static import snmp_host_port


@shared_task
def run_trap_engine(snmp_host, snmp_config):
    my_trap_engine = TrapEngine(snmp_host, snmp_host_port, snmp_config)
    try:
        my_trap_engine.run_engine()
    except Exception as exception:
        logging.basicConfig(format='!!! %(asctime)s %(message)s')
        logging.warning(exception)

        my_trap_engine.close_engine()
