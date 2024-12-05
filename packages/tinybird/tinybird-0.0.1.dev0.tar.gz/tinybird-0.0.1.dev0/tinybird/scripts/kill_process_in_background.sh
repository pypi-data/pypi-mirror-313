#!/bin/bash

# This script is used to spawn a new process in the background that will kill
# the process given as 1st parameter after the 2nd parameter timeout in seconds.
# The script itself returns immediately, but the background process created will
# make sure that the process to be killed is eventually either dead or killed by
# this utility.

set -u

kill_pid_after_timeout() {
    pid=$1
    timeout=$2

    echo "Waiting in the background $timeout seconds to kill all processes for parent PID $pid"

    while [[ $SECONDS -lt $timeout ]]; do
        # echo "Checking if PID is dead after $SECONDS seconds"
        if ! ps -p "$pid"; then
            echo "Process with parent PID $pid finished on its own :)"
            exit 0
        fi
        sleep 10
    done

    echo "Process with parent PID $pid still exists after $SECONDS seconds, killing it along with all its children"
    kill -SIGKILL -"$pid"
}

pid=$1
timeout=$2

kill_pid_after_timeout "$pid" "$timeout" &
