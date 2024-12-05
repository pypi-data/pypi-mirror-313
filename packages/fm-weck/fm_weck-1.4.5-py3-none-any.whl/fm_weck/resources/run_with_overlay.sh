#! /bin/sh

# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

TOOL_DIR=$1
shift

mkdir -p /tmp/overlay
mount -t tmpfs tmpfs /tmp/overlay
mkdir -p /tmp/overlay/upper
mkdir -p /tmp/overlay/work
mkdir -p /home/_cwd

# We mount the weck_cache to /home/weck_cache in the container
cp -r "/home/fm-weck_cache/$TOOL_DIR" /tmp/overlay/

# Assume workdir is /home/cwd
# Assume the user $PWD is mounted to home/cwd
#Mount the overlay
mount -t overlay overlay -o lowerdir=/home/cwd:/tmp/overlay/"$TOOL_DIR",upperdir=/tmp/overlay/upper,workdir=/tmp/overlay/work /home/_cwd

# Change directory and execute the command
cd /home/_cwd || exit 1

"$@" &
PID=$!

# Handle signals and delegate to the process
trap 'kill -TERM $PID' INT TERM

# Wait for the process and handle its termination correctly
wait $PID
trap - TERM INT
wait $PID   # wait for JVM to exit after signal delegation
EXIT_STATUS=$?

# Check if upper directory has data to copy to output
if [ -n "$(ls -A /tmp/overlay/upper)" ]; then
    cp -r /tmp/overlay/upper/* /home/output
fi

# Clean up mounted filesystems
umount /tmp/overlay

exit $EXIT_STATUS
