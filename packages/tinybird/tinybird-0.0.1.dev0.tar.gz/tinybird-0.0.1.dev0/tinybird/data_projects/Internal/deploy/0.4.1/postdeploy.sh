set -euxo pipefail

source .tinyenv

BACKFILL_VALUE=$(curl "${TB_HOST}/v0/pipes/releases_log_view?token=$TB_ENV_TOKEN&__tb__semver=$VERSION" | grep -o '"backfill_value": *"[^"]*"' | awk -F'"' '{print $4}')
echo $BACKFILL_VALUE

sleep 30

CURRENT_DATETIME=$(date -u +"%Y%m%d")
WEEK1=$(date -d "$CURRENT_DATETIME - 1 week" +"%Y-%m-%d 00:00:00")
WEEK2=$(date -d "$CURRENT_DATETIME - 2 week" +"%Y-%m-%d 00:00:00")
WEEK3=$(date -d "$CURRENT_DATETIME - 3 week" +"%Y-%m-%d 00:00:00")
WEEK4=$(date -d "$CURRENT_DATETIME - 4 week" +"%Y-%m-%d 00:00:00")
WEEK5=$(date -d "$CURRENT_DATETIME - 5 week" +"%Y-%m-%d 00:00:00")
WEEK6=$(date -d "$CURRENT_DATETIME - 6 week" +"%Y-%m-%d 00:00:00")
tb --semver ${VERSION} pipe copy run backfill_releases_log --param start_backfill_timestamp="$WEEK1" --param end_backfill_timestamp="$BACKFILL_VALUE" --yes --wait
tb --semver ${VERSION} pipe copy run backfill_releases_log --param start_backfill_timestamp="$WEEK2" --param end_backfill_timestamp="$WEEK1" --yes --wait
tb --semver ${VERSION} pipe copy run backfill_releases_log --param start_backfill_timestamp="$WEEK3" --param end_backfill_timestamp="$WEEK2" --yes --wait
tb --semver ${VERSION} pipe copy run backfill_releases_log --param start_backfill_timestamp="$WEEK4" --param end_backfill_timestamp="$WEEK3" --yes --wait
tb --semver ${VERSION} pipe copy run backfill_releases_log --param start_backfill_timestamp="$WEEK5" --param end_backfill_timestamp="$WEEK4" --yes --wait
tb --semver ${VERSION} pipe copy run backfill_releases_log --param start_backfill_timestamp="$WEEK6" --param end_backfill_timestamp="$WEEK5" --yes --wait

echo "preview count:"
tb --semver ${VERSION} sql "select count() from releases_log"

echo "live count:"
tb sql "select count() from releases_log"