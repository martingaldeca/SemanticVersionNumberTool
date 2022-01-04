#! /bin/sh

set -e
set -u
set -x

# Wait for DB
dockerize -wait tcp://postgres:5432 -timeout 30s

umask 000 # setting broad permissions to share log volume

celery -A backend.celery_backend beat --loglevel=$CELERY_LOG_LEVEL --logfile="/src/logs/$WORKER_NAME.log"
