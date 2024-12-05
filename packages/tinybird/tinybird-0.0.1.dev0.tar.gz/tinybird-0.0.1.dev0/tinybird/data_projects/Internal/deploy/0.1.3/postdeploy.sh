set -euxo pipefail

source .tinyenv

BACKFILL_VALUE=$(curl "${TB_HOST}/v0/pipes/pipe_stats_view?token=$TB_ENV_TOKEN&__tb__semver=$VERSION" | grep -o '"backfill_value": *"[^"]*"' | awk -F'"' '{print $4}')
echo $BACKFILL_VALUE
# wait for the backfill value, default is 30s
sleep 30

CURRENT_DATETIME=$(date +"%Y-%m-%d 00:00:00")
YESTERDAY=$(date -d "yesterday" +"%Y-%m-%d")
tb --semver ${VERSION} pipe copy run backfill_pipe_stats_from_spans --param start_backfill_timestamp="$CURRENT_DATETIME" --param end_backfill_timestamp="$BACKFILL_VALUE" --yes --wait
tb --semver ${VERSION} pipe copy run backfill_pipe_stats_from_pipe_stats --param start_backfill_date='2019-01-01' --param end_backfill_date="$YESTERDAY" --yes --wait

echo "preview count:"
tb --semver ${VERSION} sql "select count() from pipe_stats"

echo "live count:"
tb sql "select count() from pipe_stats"