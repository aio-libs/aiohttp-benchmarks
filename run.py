#!/usr/bin/env python3
import json
import os
import re
import shlex
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import aiohttp

if os.getenv('VIRTUAL_ENV', '').endswith('-asyncpg'):
    os.environ['CONNECTION'] = 'RAW'

CONNECTION_ORM = os.getenv('CONNECTION', 'ORM').upper() == 'ORM'

COMMAND_TEMPLATE = (
    'wrk -H "Host: localhost" -H "Connection: keep-alive" '
    '-d {duration} -c {concurrency} --timeout 8 -t {threads} '
    '"http://localhost:8000{url}"'
)

DURATION = 10
# DURATION = 1
urls = [
    '/db',
    '/queries/{queries}',
    '/fortunes',
    '/updates/{queries}',
]
if CONNECTION_ORM:
    urls += [
        '/json',
        '/plaintext',
    ]

results = []
python_version = '{}{}'.format(sys.version_info.major, sys.version_info.minor)
aiohttp_version = aiohttp.__version__
print('Python {}, aiohttp {}'.format(python_version, aiohttp_version))

Path('gunicorn.log').exists() and Path('gunicorn.log').unlink()
server = subprocess.Popen(['gunicorn', 'app.gunicorn:app', '-c', 'gunicorn_conf.py'])
try:
    print('gunicorn started, waiting for it to be ready...')
    time.sleep(2)
    for url in urls:
        if '{queries}' in url:
            query_steps = [5, 10, 20]
            concurrency_steps = [256] * len(query_steps)
        else:
            concurrency_steps = [32, 64, 128, 256]
            # concurrency_steps = [32, 64]
            query_steps = ['-'] * len(concurrency_steps)

        for queries, concurrency in zip(query_steps, concurrency_steps):
            url_ = url.format(queries=queries)

            command = COMMAND_TEMPLATE.format(concurrency=concurrency, duration=DURATION, threads=8, url=url_)

            db = '-' if url in {'/json', '/plaintext'} else ('orm' if CONNECTION_ORM else 'raw')
            print('\nrunning wrk for {}, concurrency: {}, db: {}...'.format(url_, concurrency, db))
            p = subprocess.run(shlex.split(command), stdout=subprocess.PIPE)
            assert p.returncode == 0, 'bad exit code for work: {}'.format(p.returncode)
            stdout = p.stdout.decode()
            print(stdout.strip('\n '))

            request_rate = float(re.search('Requests/sec: *([\d.]+)', stdout).groups()[0])
            print('request rate: {:0.2f}'.format(request_rate))

            latency, s_ms = re.search(r'Latency *([\d.]+)(m?s)', stdout).groups()
            latency = float(latency)
            if s_ms == 's':
                latency *= 1000
            print('latency:      {:0.2f}'.format(latency))

            m = re.search('Non-2xx or 3xx responses: *(\d+)', stdout)
            errors = int(m.groups()[0]) if m else 0
            print('errors:       {}'.format(errors))

            results.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%s'),
                'python': python_version,
                'aiohttp': aiohttp_version,
                'concurrency': concurrency,
                'queries': queries,
                'url': url,
                'db': db,
                'errors': errors,
                'request_rate': request_rate,
                'latency': latency,
            })

finally:
    assert server.returncode is None, 'gunicorn server should still be running, check gunicorn.log'
    server.terminate()

p = Path(__file__).parent.joinpath('results.json')
if p.exists():
    with p.open() as f:
        results = json.load(f) + results
with p.open('w') as f:
    json.dump(results, f, indent=2, sort_keys=True)
