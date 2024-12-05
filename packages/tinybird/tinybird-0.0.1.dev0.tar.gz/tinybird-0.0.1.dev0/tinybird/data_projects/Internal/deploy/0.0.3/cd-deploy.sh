#!/bin/bash
source .tinyenv

./scripts/copy_with_backfill.sh pipe_stats_rt "select *, 0 as result_rows from main.pipe_stats_rt" start_datetime
