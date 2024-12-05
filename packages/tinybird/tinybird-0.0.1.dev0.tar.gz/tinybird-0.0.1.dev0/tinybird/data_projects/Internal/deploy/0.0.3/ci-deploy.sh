#!/bin/bash

tb datasource rm pipe_stats_rt --yes
tb push datasources/pipe_stats_rt.datasource
# pushes changes in the MR
tb deploy --populate --wait --yes
tb datasource append spans datasources/fixtures/spans.csv
