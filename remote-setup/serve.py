import asyncio
import sys
from pathlib import Path

import uvloop
from aiohttp import web

if Path('/vagrant').exists():
    d = '/vagrant'
else:
    d = str(Path.home())

sys.path.append(str(d))

from app.main import create_app

asyncio.get_event_loop().close()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = create_app()
web.run_app(app, port=80, print=lambda v: None, access_log=None)
