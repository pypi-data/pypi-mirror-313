set -euxo pipefail

source .tinyenv

BACKFILL_VALUE=$(curl "${TB_HOST}/v0/pipes/endpoint_errors__v1?token=$TB_ENV_TOKEN&__tb__semver=$VERSION" | grep -o '"backfill_value": *"[^"]*"' | awk -F'"' '{print $4}')
echo $BACKFILL_VALUE
# wait for the backfill value, default is 30s
sleep 30
tb --semver ${VERSION} datasource copy endpoint_errors_ds --sql "select * from live.endpoint_errors_ds where start_datetime >= now() - interval 30 day and start_datetime <= '$BACKFILL_VALUE'" --wait
echo "preview count:"
tb --semver ${VERSION} sql "select count() from endpoint_errors_ds"
echo "live count:"
tb sql "select count() from endpoint_errors_ds"