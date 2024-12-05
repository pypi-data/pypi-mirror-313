#!/bin/bash

tb datasource rm usage_metrics_storage --yes
tb deploy --fixtures --wait

