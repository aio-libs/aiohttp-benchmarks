import multiprocessing
from pathlib import Path

if Path('/vagrant').exists():
    chdir = '/vagrant'
else:
    chdir = str(Path.home())

workers = max(multiprocessing.cpu_count(), 2)

bind = '0.0.0.0:80'
keepalive = 120
errorlog = 'gunicorn.log'
pidfile = 'gunicorn.pid'
timeout = 5

worker_class = 'aiohttp.worker.GunicornUVLoopWebWorker'
