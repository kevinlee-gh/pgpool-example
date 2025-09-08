#!/bin/bash
set -e

# Ready check
pg_isready

# Synchronous standby check
sync_count=$(psql -tf /ha-scripts/sync_standby_count.sql postgres)

current_sync_count=$(psql -Atc "SELECT COUNT(*) FROM pg_stat_replication WHERE sync_state = 'sync'" postgres)

echo $sync_count - $current_sync_count - $(if [ $sync_count == $current_sync_count ]; then echo "OK"; else echo "NOT OK"; exit 1; fi)