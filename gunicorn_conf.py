import multiprocessing
import os

if os.environ.get('TRAVIS') == 'true':
    workers = 2
else:
    workers = max(multiprocessing.cpu_count(), 2)

bind = '0.0.0.0:80'
keepalive = 120
errorlog = 'gunicorn.log'
pidfile = 'gunicorn.pid'

worker_class = 'aiohttp.worker.GunicornUVLoopWebWorker'
