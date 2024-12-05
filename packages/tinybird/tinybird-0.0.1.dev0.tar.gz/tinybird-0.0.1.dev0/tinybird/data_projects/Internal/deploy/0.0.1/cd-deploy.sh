#!/bin/bash
source .tinyenv

retry_duration=12 
retry_interval=1
max_retries=$((retry_duration / retry_interval))

BACKFILL_TIME=""
retry_count=0

while [[ $retry_count -lt $max_retries ]]; do
    output=$(tb --no-version-warning sql "select min(start_datetime) as t from pipe_stats_rt" --semver $VERSION --format json)
    if [ -z "$output" ]; then
        echo "Output is empty"
        result=""
    else
        result=$(echo "$output" | python -c "import sys, json; print(json.load(sys.stdin)['data'][0]['t'])")
    fi

    if [[ -z $result || $result == "1970-01-01 00:00:00" ]]; then
        sleep $retry_interval
        retry_count=$((retry_count + 1))
    else
        BACKFILL_TIME=$result
        break
    fi
done

if [[ -z $BACKFILL_TIME ]]; then
    BACKFILL_TIME=$(date +"%Y-%m-%d %H:%M:%S")
fi

tb pipe populate pipe_stats_rt_view --node pipe_stats_rt_view_0 --sql-condition "start_datetime < '$BACKFILL_TIME' and toStartOfInterval(start_datetime, INTERVAL 6 HOUR) >= now() - INTERVAL 7 DAY - INTERVAL 6 HOUR" --wait --semver $VERSION --wait

count_live=$(tb --no-version-warning sql "select count() from pipe_stats_rt" --format json | python -c "import sys, json; print(json.load(sys.stdin)['data'][0]['count()'])")
echo "Live count: $count_live"
count_preview=$(tb --no-version-warning sql "select count() from pipe_stats_rt" --format json --semver $VERSION | python -c "import sys, json; print(json.load(sys.stdin)['data'][0]['count()'])")
echo "Preview count: $count_preview"

if [ $count_live -eq $count_preview ]; then
    echo "Both counts are equal."
    exit 0
else
    echo "Counts are not equal."
    exit 1
fi