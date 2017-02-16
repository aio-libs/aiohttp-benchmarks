# could do more here for greater performance but that wouldn't help the test
workers = 1

bind = '0.0.0.0:8000'
keepalive = 120
errorlog = 'gunicorn.log'
pidfile = 'gunicorn.pid'

worker_class = 'aiohttp.worker.GunicornUVLoopWebWorker'
