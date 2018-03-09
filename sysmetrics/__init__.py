import psutil
import asyncio
import functools
import signal
import graypy
import logging
import json


loop = asyncio.get_event_loop()
logger = logging.getLogger('sysmetrics')
RESOLUTION = .5


def _exit(signame):
    loop.stop()


def _probe():
    info = {}
    info['cpu'] = {'percent': psutil.cpu_percent(interval=None)}
    disk_counters = psutil.disk_io_counters()
    disk_io = {'read_count': disk_counters.read_count,
               'write_count': disk_counters.write_count,
               'read_bytes': disk_counters.read_bytes,
               'write_bytes': disk_counters.write_bytes}

    info['disk'] = disk_io
    memory = {}
    vm = psutil.virtual_memory()
    memory['total'] = vm.total
    memory['available'] = vm.available
    memory['used'] = vm.used
    memory['free'] = vm.free
    info['memory'] = memory

    logger.info(json.dumps(info))
    loop.call_later(RESOLUTION, _probe)


def main():
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                functools.partial(_exit, signame))

    handler = graypy.GELFHandler('localhost', 12201)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    loop.call_later(RESOLUTION, _probe)
    print("Probing cpu, memory and disk...")
    try:
        loop.run_forever()
    finally:
        loop.close()
