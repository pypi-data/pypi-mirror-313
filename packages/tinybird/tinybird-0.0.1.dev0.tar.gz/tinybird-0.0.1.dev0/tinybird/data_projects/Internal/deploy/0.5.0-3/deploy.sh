#!/bin/bash
set -e

source .tinyenv

CURRENT_COMMIT=$(git rev-parse HEAD)

echo "** Manually update the Data Source"
tb push datasources/external_datasource_connector_ops_log.datasource --force --yes

echo "** Force update yepcode_to_internal Materialized View:"
tb push pipes/yepcode_to_internal.pipe --force

if [[ "$TB_HOST" == *"wadus"* ]]; then
    tb datasource append external_datasource_connector_ops_log datasources/fixtures/external_datasource_connector_ops_log.ndjson
fi

echo "** Current job: $CI_JOB_NAME"

if [[ "$CI_JOB_NAME" != *"01_internal_wadus_deploy_ci"* ]]; then
    echo "** Update HEAD $CURRENT_COMMIT"
    echo 'y' | tb init --override-commit "$CURRENT_COMMIT"
fi

tb release create --semver ${VERSION}
tb release preview --semver ${VERSION}
tb release promote --semver ${VERSION}
tb release ls
