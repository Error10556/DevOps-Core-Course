#!/bin/sh

if [ $(whoami) = root ]; then
    chown infoservice:infoservice /data
    exec su infoservice -s /docker-entrypoint.sh -- "$@"
fi

exec gunicorn "$@"
