#!/bin/bash
set -e

if [[ -z "${MONITOR_USER}" || -z "${MONITOR_PASSWORD}" ]]; then
    echo "ERROR - MONITOR_USER and MONITOR_PASSWORD must be set"
    exit 1
fi

export PGUSER=${MONITOR_USER}
export PGPASSWORD=${MONITOR_PASSWORD}

# Ready check
pg_isready

# Synchronous standby check
if [[ -z "$(psql -Atc 'show synchronous_standby_names' postgres)" ]]; then
    echo "ERROR - No synchronous standby names found"
    exit 1
fi

sync_node=$(psql -Atc "SELECT application_name FROM pg_stat_replication WHERE sync_state = 'sync'" postgres)

echo $sync_node