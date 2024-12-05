import os

if os.environ.get('MODE') == 'dev':
    reload = True

preload_app = True
worker_class = "uvicorn.workers.UvicornWorker"
bind = '0.0.0.0:8000'
workers = 4
threads = 4
