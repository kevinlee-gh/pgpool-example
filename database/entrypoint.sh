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
    (
        export PGHOST=${MASTER_HOST}
        export PGPORT=${MASTER_PORT:-5432}
        export PGUSER=${MASTER_REPLICATOR_USER}
        export PGPASSWORD=${MASTER_REPLICATOR_PASSWORD}
        export PGDATABASE=postgres

        RETRIES=10
        for i in $(seq 1 $RETRIES); do
            pg_isready && \
            psql -c  "select version();" && \
            break
            
            if [ $i -eq $RETRIES ]; then
                echo "ERROR - Master node is not ready after $RETRIES attempts"
                exit 1
            else
                echo "INFO - Master node is still not ready, retrying..."
                sleep 10
            fi
        done


        if ! (pg_basebackup -D ${PGDATA} -vRC -X stream -S ${NODE_NAME}); then
            psql -c  "SELECT pg_drop_replication_slot('${NODE_NAME}');"
        fi
    )
fi

docker-entrypoint.sh postgres -ccluster_name=$NODE_NAME $@