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
sync_count=$(psql -tf /ha-scripts/sync_standby_count.sql postgres)

current_sync_count=$(psql -Atc "SELECT COUNT(*) FROM pg_stat_replication WHERE sync_state = 'sync'" postgres)

echo $sync_count - $current_sync_count