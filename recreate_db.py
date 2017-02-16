#!/usr/bin/env python3
import os
from pathlib import Path

import psycopg2

connection_kwargs = dict(
    password=os.getenv('PGPASS', ''),
    host='localhost',
    port=5432,
    user=os.getenv('PGUSER', 'postgres'),
)

conn = psycopg2.connect(**connection_kwargs)
db_name = 'hello_world'
conn.autocommit = True
cur = conn.cursor()
cur.execute('DROP DATABASE IF EXISTS {}'.format(db_name))
cur.execute('CREATE DATABASE {}'.format(db_name))
cur.close()
conn.close()

conn = psycopg2.connect(dbname=db_name, **connection_kwargs)
db_name = 'hello_world'
conn.autocommit = True
cur = conn.cursor()
cur.execute(Path('data.sql').read_text())
cur.close()
conn.close()
