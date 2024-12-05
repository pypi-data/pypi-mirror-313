source .tinyenv

BACKFILL_VALUE=$(curl "${TB_HOST}/v0/pipes/pipe_stats_rt_view?token=$TB_ENV_TOKEN&__tb__semver=$VERSION" | grep -o '"backfill_value": *"[^"]*"' | awk -F'"' '{print $4}')
echo $BACKFILL_VALUE
# wait for the backfill value, default is 30s
sleep 30
tb --semver ${VERSION} pipe populate pipe_stats_rt_view --node pipe_stats_rt_view_0 --sql-condition "start_datetime >= now() - interval 7 day and start_datetime <= '$BACKFILL_VALUE'" --wait
