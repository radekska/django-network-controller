from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .TrapEngine import TrapEngine


@shared_task
def add(x, y):
    return x + y


@shared_task
def run_trap_engine():
    my_trap_engine = TrapEngine('192.168.8.106', 162)
    try:
        my_trap_engine.run_engine()
    except Exception:
        my_trap_engine.close_engine()



