#!/bin/bash

# pushes changes in the MR
tb deploy --populate --wait
# Delete tracker.datasource
tb datasource rm tracker --yes
