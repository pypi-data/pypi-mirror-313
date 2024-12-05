#!/bin/bash
set -euxo pipefail

source .tinyenv

BACKFILL_VALUE=$(curl "${TB_HOST}/v0/pipes/releases_log_view?token=$TB_ENV_TOKEN&__tb__semver=$VERSION" | grep -o '"backfill_value": *"[^"]*"' | awk -F'"' '{print $4}')
echo $BACKFILL_VALUE

# wait for the backfill value, default is 30s
sleep 30
tb --semver $VERSION pipe populate releases_log_view --node releases_event_types_to_releases_log --sql-condition "start_datetime > now() - interval 1 month and start_datetime <= '$BACKFILL_VALUE'" --wait

echo "preview count:"
tb --semver ${VERSION} sql "select count() from releases_log"
