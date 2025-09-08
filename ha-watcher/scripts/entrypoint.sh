#!/bin/bash
set -e

while true; do
    /scripts/health_check.sh
    sleep 5
done