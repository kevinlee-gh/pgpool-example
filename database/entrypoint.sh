#!/bin/bash
set -e 

if [ -n "$CUSTOM_LOAD_BACKUP" ]; then
    if [ -d "$CUSTOM_LOAD_BACKUP" ]; then
        timeSuffix=$(date +"%Y-%m-%dT%H-%M")
        mv $PG_DATA $PG_DATA.bak-$timeSuffix
        mv $CUSTOM_LOAD_BACKUP $PG_DATA
        echo "INFO - Loaded backup from $CUSTOM_LOAD_BACKUP"
    else
        echo "WARN - Custom load backup directory does not exist!"
        # exit 1
    fi
fi


docker-entrypoint.sh $@