#!/usr/bin/env python3
import os
import shlex
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path

import psycopg2

if os.getenv('VIRTUAL_ENV', '').endswith('-asyncpg'):
    os.environ['CONNECTION'] = 'RAW'

CONNECTION_ORM = os.getenv('CONNECTION', 'ORM').upper() == 'ORM'

Path('gunicorn.log').exists() and Path('gunicorn.log').unlink()


def prepare_db():
    conn = psycopg2.connect(
        password=os.getenv('PGPASS', ''),
        host='localhost',
        port=5432,
        user=os.getenv('PGUSER', 'postgres'),
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(Path('data.sql').read_text())


@contextmanager
def run_gunicorn():
    server = subprocess.Popen(['gunicorn', 'app.gunicorn:app', '-c', 'gunicorn_conf.py'])
    print('gunicorn started, waiting for it to be ready...')
    time.sleep(2)
    yield
    assert server.returncode is None, 'gunicorn server should still be running, check gunicorn.log'
    server.terminate()


COMMAND_TEMPLATE = (
    'wrk -H "Host: localhost" -H "Connection: keep-alive" '
    '--latency -d 10 -c {concurrency} --timeout 4 -t {threads} '
    '"http://localhost:8000{url}"'
)

prepare_db()
with run_gunicorn():
    command = COMMAND_TEMPLATE.format(concurrency=256, threads=8, url='/json')
    print('running wrk...')
    p = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, encoding='utf8')
    print('wrk finished')
    print('work returncode:', p.returncode)
    print('stdout:', p.stdout)
