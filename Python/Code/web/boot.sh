#! /usr/bin/env bash

set -e

# setup variables
LOGFILE=/home/siddhant/thesis/Python/Code/web/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=1
USER=siddhant
GROUP=siddhant

# start the main application
cd /home/siddhant/thesis/Python/Code/web/
pythonbrew venv use thesis
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn_django -w $NUM_WORKERS --user=$USER --group=$GROUP --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE
