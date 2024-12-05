#!/bin/bash
source .tinyenv

tb --semver ${VERSION} deploy --v3
BACKFILL_VALUE=$(curl "${TB_HOST}/v0/pipes/endpoint_errors__v1?token=$TB_ADMIN_TOKEN&__tb__semver=$VERSION" | grep -o '"backfill_value": *"[^"]*"' | awk -F'"' '{print $4}')
echo $BACKFILL_VALUE
# wait for the backfill value, default is 30s
sleep 30
tb --semver ${VERSION} pipe populate endpoint_errors__v1 --node endpoint_errors_0 --sql-condition "start_datetime >= now() - interval 30 day and start_datetime < '$BACKFILL_VALUE'" --wait