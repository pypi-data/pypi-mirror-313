#!/bin/bash
set -e

source .tinyenv

if [[ "$TB_HOST" == *"wadus"* ]]; then
    tb datasource append external_datasource_connector_ops_log datasources/fixtures/external_datasource_connector_ops_log.ndjson
fi

tb --semver ${VERSION} deploy
tb release ls
