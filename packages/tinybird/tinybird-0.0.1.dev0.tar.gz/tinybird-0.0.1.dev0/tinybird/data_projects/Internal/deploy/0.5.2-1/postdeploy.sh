#!/bin/bash
set -euxo pipefail

source .tinyenv

tb --semver $VERSION pipe populate datasources_ops_stats_view --node datasources_ops_stats_view_0 --wait

echo "preview count:"
tb --semver ${VERSION} sql "select count() from datasources_ops_stats"