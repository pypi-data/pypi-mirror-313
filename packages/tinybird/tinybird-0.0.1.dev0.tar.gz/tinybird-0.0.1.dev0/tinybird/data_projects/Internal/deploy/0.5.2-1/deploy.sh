#!/bin/bash
set -e

source .tinyenv

echo "** Force update datasource_ops_log to get new TAGS"
tb push datasources/datasources_ops_log.datasource --force

tb --semver ${VERSION} deploy
tb release ls
