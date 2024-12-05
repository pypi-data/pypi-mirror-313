#!/bin/bash
set -euxo pipefail

source .tinyenv

query="select id, name, database, database_server, plan, created_at, origin, '' as organization_id, null as deleted_at from workspaces_all"

tb --semver $VERSION datasource copy workspaces_all_rt --sql "$query" --wait

echo "preview count:"
tb --semver ${VERSION} sql "select count() from workspaces_all_rt"