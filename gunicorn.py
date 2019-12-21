import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
reload = True

loglevel = 'debug'
errorlog = 'gunicorn_access.log'
accesslog = 'gunicorn_debug.log'

