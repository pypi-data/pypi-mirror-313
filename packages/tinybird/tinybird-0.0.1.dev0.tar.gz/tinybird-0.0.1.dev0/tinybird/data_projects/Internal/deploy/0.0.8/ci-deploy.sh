#!/bin/bash
set -e

source .tinyenv
tb release create --semver ${VERSION}
# If I do --populate the copy_with_backfill mismatches, there are more rows in v0_0_8.pipe_stats_rt than in v0_0_7.pipe_stats_rt
# The reason is the populate runs over the v0_0_8 User model, so v0_0_8.pipe_stats_rt is populated with all the rows from spans as opposed to v0_0_7.pipe_stats_rt which only has the last partition which are 6 hours of data
tb --semver ${VERSION} deploy --fixtures --fork-downstream --is-internal
tb release preview --semver ${VERSION}
./scripts/copy_with_backfill.sh pipe_stats_rt "select *, map() as parameters from live.pipe_stats_rt" start_datetime
tb release promote --semver ${VERSION}
tb release ls