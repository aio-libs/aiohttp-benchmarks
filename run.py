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

import requests

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s', datefmt='%H:%M:%S'))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

REMOTE = os.getenv('REMOTE', 'FALSE').upper() in ('1', 'TRUE')
if REMOTE:
    SSH_COMMAND = 'ssh', '-i', 'benchmarks.pem', os.environ['SSH_ADDRESS']
    SERVER = os.environ['HTTP_ADDRESS']
    print('Running on remote machine...')
else:
    SSH_COMMAND = 'vagrant', 'ssh', '-c'
    SERVER = 'http://localhost:8080'
    print('Running on vagrant...')

print(f'ssh command: {SSH_COMMAND}')
print(f'server:      {SERVER}')


INSTALL_COMMAND = '~/env3{py_v}/bin/pip install "{package}"'
RUN_COMMAND = 'sudo ~/env3{py_v}/bin/python serve.py'

AIOH_VERSIONS = {
    '3.6': 'aiohttp>=3.6,<3.7',
    '3.7': 'aiohttp>=3.7,<3.8',
}


COMMAND_TEMPLATE = (
    'wrk -H "Host: localhost" -H "Connection: keep-alive" '
    '-d {duration} -c {concurrency} --timeout 8 -t {threads} '
    '"{server}{url}"'
)


def run_remote(*commands, check=False):
    c = SSH_COMMAND + commands
    logger.info(f'running  %s', c)
    subprocess.run(c, check=check)


DURATION = 10
results = []

raw_cases = itertools.product(
    (7, 8, 9),                    # python version
    tuple(AIOH_VERSIONS.keys()),  # aiohttp version
    ('orm', 'raw'),               # connection type
    ('/{c}/db', '/{c}/queries/{q}', '/{c}/fortunes', '/{c}/updates/{q}', '/json', '/plaintext'),  # url
    (5, 10, 20),                  # queries
    (32, 64, 128, 256),           # concurrency
)
cases = []
for py_v, aiohttp_v, connection, url, queries, conc in raw_cases:

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

    cases.append((py_v, aiohttp_v, connection, url, queries, conc))

versions_previous = None
case_count = len(cases)
case_no = 0
for py_v, aiohttp_v, connection, url, queries, conc in cases:
    start = time.time()
    case_no += 1
    url_ = url.format(q=queries, c=connection)
    logger.info('===============================================================================')
    logger.info(f'   Python 3.{py_v}, aiohttp {aiohttp_v}, url {url_}, concurrency {conc}, case {case_no}/{case_count}')
    logger.info('===============================================================================')

    versions = py_v, aiohttp_v
    if versions != versions_previous:
        versions_previous = versions
        run_remote(INSTALL_COMMAND.format(py_v=py_v, package=AIOH_VERSIONS[aiohttp_v]), check=True)

    run_remote('sudo killall python')
    # run_remote('sudo service postgresql restart')
    # time.sleep(2)

    run = SSH_COMMAND + (RUN_COMMAND.format(py_v=py_v),)
    logger.info(f'starting %s', run)
    server = subprocess.Popen(run, env={'HOME': os.getenv('HOME'), 'PATH': os.getenv('PATH')})

    try:
        logger.info('server started, waiting for it to be ready...')
        # prevent the vagrant/ssh messing up the tty
        subprocess.run(('stty', 'sane'))
        for i in range(40):
            time.sleep(0.1)
            try:
                r = requests.get(f'{SERVER}/plaintext', timeout=1)
            except Exception:
                continue
            if r.status_code == 200:
                subprocess.run(('stty', 'sane'))
                logger.info('server running after connection %d attempts', i)
                break

        r = requests.get(f'{SERVER}/plaintext')
        logger.info('plaintext response: "%s", status: %d, server: "%s"', r.text, r.status_code, r.headers['server'])
        assert r.status_code == 200
        server_python, server_aiohttp = re.search('Python/3\.(\d) *aiohttp/(\S{3})', r.headers['server']).groups()
        assert py_v == int(server_python)
        assert aiohttp_v[:3] == server_aiohttp

        logger.info('running wrk...')
        wrk_command = COMMAND_TEMPLATE.format(server=SERVER, concurrency=conc, duration=DURATION, threads=8, url=url_)
        p = subprocess.run(shlex.split(wrk_command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdoe = p.stdout.decode()
        logger.info('wrk output: %s', stdoe.strip('\n '))
        assert p.returncode == 0, f'bad exit code for wrk: {p.returncode}'
    finally:
        assert server.returncode is None, 'server command should still be running'
        server.terminate()

    request_rate = float(re.search('Requests/sec: *([\d.]+)', stdoe).groups()[0])
    logger.info('request rate: %0.2f', request_rate)

    latency, s_ms = re.search(r'Latency *([\d.]+)(m?s)', stdoe).groups()
    latency = float(latency)
    if s_ms == 's':
        latency *= 1000
    logger.info('latency:      %0.2f', latency)

    m = re.search('Non-2xx or 3xx responses: *(\d+)', stdoe)
    errors = int(m.groups()[0]) if m else 0
    m = re.search('Socket errors: *connect (\d+), read (\d+), write (\d+), timeout (\d+)', stdoe)
    if m:
        errors += sum(map(int, m.groups()))
    logger.info('errors:       %d', errors)
    logger.info('time taken:   %0.2fs', time.time() - start)

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
