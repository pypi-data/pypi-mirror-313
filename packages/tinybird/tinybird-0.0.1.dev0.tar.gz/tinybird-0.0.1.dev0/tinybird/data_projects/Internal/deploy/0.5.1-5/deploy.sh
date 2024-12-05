#!/bin/bash
set -e

source .tinyenv

echo "** Force update Materialized Views:"
tb push pipes/yepcode_to_internal.pipe --force
tb push pipes/connector_ops_log_view.pipe --force

tb --semver ${VERSION} deploy
tb release ls
