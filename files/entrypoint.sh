#!/bin/sh
set -e

# check if there was a command passed
# required by Jenkins Docker plugin: https://github.com/docker-library/official-images#consistency

# this if will check if the first argument is a flag
# but only works if all arguments require a hyphenated flag
# -v; -SL; -f arg; etc will work, but not arg1 arg2
if [ "$#" -eq 0 ] || [ "${1#-}" != "$1" ]; then
    set -- python /job_launch.py "$@"
fi

# else default to run whatever the user wanted like "bash" or "sh"
exec "$@"