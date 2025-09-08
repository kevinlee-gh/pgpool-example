#!/bin/bash
set -e

# Ready check
pg_isready

# Synchronous standby check
sync_count=$(psql -tf /sql/sync_standby_count.sql postgres)

current_sync_count=$(psql -Atc "SELECT COUNT(*) FROM pg_stat_replication WHERE sync_state = 'sync'" postgres)

if [ $sync_count == $current_sync_count ]; then
    echo $(date +%Y-%m-%dT%H:%M:%S) - Synchronous standby check: OK
else
    echo $(date +%Y-%m-%dT%H:%M:%S) - Synchronous standby check: NOT OK
    exit 1
fi