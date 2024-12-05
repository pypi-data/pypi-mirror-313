#!/bin/bash
set -euxo pipefail

source .tinyenv

tb --semver $VERSION pipe populate sinks_data_transfer_view --node sinks_ops_log_to_data_transfer --wait

echo "preview count:"
tb --semver ${VERSION} sql "select count() from data_transfer"
