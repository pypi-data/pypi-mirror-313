set -euxo pipefail

source .tinyenv

BACKFILL_VALUE=$(curl "${TB_HOST}/v0/pipes/pipe_stats_rt_view?token=$TB_ENV_TOKEN&__tb__semver=$VERSION" | grep -o '"backfill_value": *"[^"]*"' | awk -F'"' '{print $4}')
echo $BACKFILL_VALUE
# wait for the backfill value, default is 30s
sleep 30
tb --semver ${VERSION} datasource copy pipe_stats_rt --sql "select *, '' user_agent from live.pipe_stats_rt where start_datetime >= now() - interval 7 day and start_datetime <= '$BACKFILL_VALUE'" --wait
echo "preview count:"
tb --semver ${VERSION} sql "select count() from pipe_stats_rt"
echo "live count:"
tb sql "select count() from pipe_stats_rt"