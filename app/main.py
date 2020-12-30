import os
from pathlib import Path

import aiohttp_jinja2
import aiopg.sa
import asyncpg
import jinja2
from aiohttp import web
from sqlalchemy.engine.url import URL

from .views import (
    json,
    single_database_query_orm,
    multiple_database_queries_orm,
    fortunes,
    updates,
    plaintext,

    single_database_query_raw,
    multiple_database_queries_raw,
    fortunes_raw,
    updates_raw,
)

THIS_DIR = Path(__file__).parent


def pg_dsn() -> str:
    """
    :return: DSN url suitable for sqlalchemy and aiopg.
    """
    return str(URL(
        database='hello_world',
        password=os.getenv('PGPASS', 'benchmarks'),
        host='localhost',
        port='5432',
        username=os.getenv('PGUSER', 'postgres'),
        drivername='postgres',
    ))


async def startup(app: web.Application):
    dsn = pg_dsn()
    min_size, max_size = 10, 20
    app['pg_orm'] = await aiopg.sa.create_engine(dsn=dsn, minsize=min_size, maxsize=max_size)
    app['pg_raw'] = await asyncpg.create_pool(dsn=dsn, min_size=min_size, max_size=max_size)


async def cleanup(app: web.Application):
    app['pg_orm'].close()
    await app['pg_orm'].wait_closed()
    await app['pg_raw'].close()


def setup_routes(app):
    app.router.add_get('/json', json)
    app.router.add_get('/plaintext', plaintext)

    app.router.add_get('/orm/db', single_database_query_orm)
    app.router.add_get('/orm/queries/{queries:.*}', multiple_database_queries_orm)
    app.router.add_get('/orm/fortunes', fortunes)
    app.router.add_get('/orm/updates/{queries:.*}', updates)

    app.router.add_get('/raw/db', single_database_query_raw)
    app.router.add_get('/raw/queries/{queries:.*}', multiple_database_queries_raw)
    app.router.add_get('/raw/fortunes', fortunes_raw)
    app.router.add_get('/raw/updates/{queries:.*}', updates_raw)


def create_app():
    app = web.Application()

    jinja2_loader = jinja2.FileSystemLoader(str(THIS_DIR / 'templates'))
    aiohttp_jinja2.setup(app, loader=jinja2_loader)

    app.on_startup.append(startup)
    app.on_cleanup.append(cleanup)

    setup_routes(app)
    return app
