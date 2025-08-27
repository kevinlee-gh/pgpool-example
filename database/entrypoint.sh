#!/bin/bash
set -e

NODE_NAME=${NODE_NAME:-$(hostname)}

if [ -z "${PGDATA}" ]; then
    PGDATA=/var/lib/postgresql/data/pgdata
    echo "INFO - PGDATA is not set, using default: $PGDATA"
fi

if [ -d "${PGDATA}" ]; then
    echo "INFO - PostgreSQL data directory exists"
elif [ -n "${MASTER_HOST}" ]; then
    echo "INFO - Starting replication setup from master node"

    RETRIES=10
    for i in $(seq 1 $RETRIES); do
        pg_isready -h ${MASTER_HOST} -U ${MASTER_REPLICATOR_USER} && \
        PGPASSWORD=${MASTER_REPLICATOR_PASSWORD} psql -U ${MASTER_REPLICATOR_USER} -h ${MASTER_HOST} -c  "select version();" postgres && \
        break
        
        if [ $i -eq $RETRIES ]; then
            echo "ERROR - Master node is not ready after $RETRIES attempts"
            exit 1
        else
            echo "INFO - Master node is still not ready, retrying..."
            sleep 10
        fi
    done

    PGPASSWORD=${MASTER_REPLICATOR_PASSWORD} pg_basebackup -h ${MASTER_HOST} -D ${PGDATA} -U ${MASTER_REPLICATOR_USER} -vRC -X stream -S ${NODE_NAME}
else
    echo "INFO - Bootstrapping PostgreSQL server!"
fi

docker-entrypoint.sh $@