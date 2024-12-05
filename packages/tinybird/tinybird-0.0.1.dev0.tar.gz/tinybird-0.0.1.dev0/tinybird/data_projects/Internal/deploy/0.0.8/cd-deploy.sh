#!/bin/bash
source .tinyenv

tb release create --semver ${VERSION}
tb --semver ${VERSION} deploy --fork-downstream --is-internal
tb release preview --semver ${VERSION}
tb release ls
./scripts/copy_with_backfill.sh pipe_stats_rt "select *, map() as parameters from live.pipe_stats_rt" start_datetime
