# gunicorn_django configuration file

from os import getcwd
from os import getenv
from os.path import expanduser
from sys import exit

# paths of the pid/log files depend on the DJANGO_ENV variable
env = getenv("DJANGO_ENV")
if env is None:
    print "Please set the DJANGO_ENV variable"
    exit(1)
else:
    if env == "development":
        home = getcwd()
    else:
        home = expanduser("~")

bind = "0.0.0.0:10001"
workers = 1
debug = True
daemon = True
pidfile = home + "/system/gunicorn.pid"
logfile = home + "/system/gunicorn.log"
accesslog = home + "/system/gunicorn-access.log"
errorlog = home + "/system/gunicorn-error.log"
