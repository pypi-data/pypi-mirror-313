#!/bin/bash
set -euxo pipefail

source .tinyenv

RETRY_DURATION=12
RETRY_INTERVAL=1
RETRY_COUNT=0
MAX_RETRIES=$((RETRY_DURATION / RETRY_INTERVAL))
BACKFILL_TIME=""

while [[ $RETRY_COUNT -lt $MAX_RETRIES ]]; do
    output=$(tb --no-version-warning sql "select min(timestamp) as t from v0_5_0.external_datasource_connector_ops_log" --format json)
    if [ -z "$output" ]; then
        echo "Output is empty"
        result=""
    else
        result=$(echo "$output" | python -c "import sys, json; print(json.load(sys.stdin)['data'][0]['t'])")
    fi

    if [[ -z $result || $result == "1970-01-01 00:00:00" ]]; then
        sleep $RETRY_INTERVAL
        RETRY_COUNT=$((RETRY_COUNT + 1))
    else
        BACKFILL_TIME=$result
        break
    fi
done

if [[ -z $BACKFILL_TIME ]]; then
    BACKFILL_TIME=$(date +"%Y-%m-%d %H:%M:%S")
fi

echo "** Backfill time:"
echo $BACKFILL_TIME

tb --semver $VERSION pipe populate external_datasource_connector_ops_log_view --node external_datasource_connector_ops_log_data --sql-condition "timestamp < '$BACKFILL_TIME'" --wait

echo "** Preview count:"
tb sql "select count() as current_count from external_datasource_connector_ops_log"
tb --semver $VERSION sql "select count() as populate_count from external_datasource_connector_ops_log"
