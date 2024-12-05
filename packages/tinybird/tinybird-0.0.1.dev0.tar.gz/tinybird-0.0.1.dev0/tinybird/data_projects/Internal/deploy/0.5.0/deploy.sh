#!/bin/bash
set -e

source .tinyenv

if [[ "$TB_HOST" == *"wadus"* ]]; then
    tb datasource append external_datasource_connector_ops_log datasources/fixtures/external_datasource_connector_ops_log.ndjson
fi

tb --semver ${VERSION} deploy
tb --semver ${VERSION} push backfill/external_datasource_connector_ops_log_view.pipe
tb release ls
