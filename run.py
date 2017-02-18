#!/usr/bin/env python3
import itertools
import json
import logging
import os
import re
import shlex
import subprocess
import time
from datetime import datetime
from pathlib import Path

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s', datefmt='%H:%M:%S'))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

RUN_PREFIX = ''
REMOTE = os.getenv('REMOTE').upper() in ('1', 'TRUE')
if REMOTE:
    SSH_COMMAND = 'ssh', '-i', 'benchmarks.pem', os.environ['SSH_ADDRESS']
    SERVER = os.environ['HTTP_ADDRESS']
    print('Running on remote machine...')
else:
    SSH_COMMAND = 'vagrant', 'ssh', '-c'
    SERVER = 'http://localhost:8080'
    RUN_PREFIX = 'cd /vagrant && '
    print('Running on vagrant...')

print(f'ssh command: {SSH_COMMAND}')
print(f'server:      {SERVER}')


INSTALL_COMMAND = '~/env3{py_v}/bin/pip install "{package}"'
RUN_COMMAND = RUN_PREFIX + 'sudo ~/env3{py_v}/bin/gunicorn app.gunicorn:app -c gunicorn_conf.py'
KILL_COMMAND = 'sudo killall gunicorn'

AIOH_VERSIONS = {
    '1.2': 'aiohttp>=1.2,<1.3',
    '1.3': 'aiohttp>=1.3,<1.4',
    '2.0a': 'https://github.com/KeepSafe/aiohttp/archive/9218c264d57c633bc21cb7a14cd7890a272d4e34.zip',
}


COMMAND_TEMPLATE = (
    'wrk -H "Host: localhost" -H "Connection: keep-alive" '
    '-d {duration} -c {concurrency} --timeout 8 -t {threads} '
    '"{server}{url}"'
)

DURATION = 10
# DURATION = 3
results = []

cases = itertools.product(
    (5, 6),                  # python version
    ('1.2', '1.3', '2.0a'),  # aiohttp
    ('orm', 'raw'),          # connection type
    ('/{c}/db', '/{c}/queries/{q}', '/{c}/fortunes', '/{c}/updates/{q}', '/json', '/plaintext'),  # url
    (5, 10, 20),             # queries
    (32, 64, 128, 256),      # concurrency
)
versions_previous = None
server = None
for py_v, aiohttp_v, connection, url, queries, conc in cases:

    if '{c}' not in url:
        if connection != 'orm':
            continue
        else:
            connection = '-'

    if '{q}' in url:
        if conc != 256:
            continue
    else:
        if queries != 20:
            continue
        else:
            queries = '-'

    url_ = url.format(q=queries, c=connection)

    logger.info('===============================================================================')
    logger.info(f'==== Python 3.{py_v}, aiohttp {aiohttp_v}, conn {connection}, url {url_}, concurrency {conc}')
    logger.info('===============================================================================')

    versions = py_v, aiohttp_v
    if versions != versions_previous:
        versions_previous = versions
        if server:
            assert server.returncode is None, 'gunicorn server command should still be running'
            server.terminate()

        kill = SSH_COMMAND + (KILL_COMMAND,)
        logger.info(f'running {kill}')
        subprocess.run(kill)
        time.sleep(1)

        install = SSH_COMMAND + (INSTALL_COMMAND.format(py_v=py_v, package=AIOH_VERSIONS[aiohttp_v]),)
        logger.info(f'running {install}')
        subprocess.run(install, check=True)

        run = SSH_COMMAND + (RUN_COMMAND.format(py_v=py_v),)
        logger.info(f'starting {run}')
        server = subprocess.Popen(run, env={'HOME': os.getenv('HOME'), 'PATH': os.getenv('PATH')})

        logger.info('gunicorn started, waiting for it to be ready...')
        time.sleep(2)
        subprocess.run(('stty', 'sane'))

    logger.info('running wrk...')
    wrk_command = COMMAND_TEMPLATE.format(server=SERVER, concurrency=conc, duration=DURATION, threads=8, url=url_)
    p = subprocess.run(shlex.split(wrk_command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert p.returncode == 0, 'bad exit code for wrk: {}'.format(p.returncode)
    stdout = p.stdout.decode()
    logger.info(stdout.strip('\n '))

    request_rate = float(re.search('Requests/sec: *([\d.]+)', stdout).groups()[0])
    logger.info('request rate: {:0.2f}'.format(request_rate))

    latency, s_ms = re.search(r'Latency *([\d.]+)(m?s)', stdout).groups()
    latency = float(latency)
    if s_ms == 's':
        latency *= 1000
    logger.info('latency:      {:0.2f}'.format(latency))

    m = re.search('Non-2xx or 3xx responses: *(\d+)', stdout)
    errors = int(m.groups()[0]) if m else 0
    logger.info('errors:       {}'.format(errors))

    results.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%s'),
        'python': f'3.{py_v}',
        'aiohttp': aiohttp_v,
        'concurrency': conc,
        'queries': queries,
        'url': url,
        'db': connection,
        'errors': errors,
        'request_rate': request_rate,
        'latency': latency,
    })

p = Path(__file__).parent.joinpath('results.json')
with p.open('w') as f:
    json.dump(results, f, indent=2, sort_keys=True)
