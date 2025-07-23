#!/bin/bash
set -e

# Directory for storing checksums, Render caches this path
CACHE_DIR=./.render-cache
mkdir -p $CACHE_DIR

# File paths
REQS_FILE=requirements.txt
PROCESS_DATA_FILE=process_data.py
REQS_CHECKSUM_FILE=$CACHE_DIR/requirements.sum
PROCESS_DATA_CHECKSUM_FILE=$CACHE_DIR/process_data.sum

# --- Dependency Installation ---
# Calculate the current checksum of requirements.txt
CURRENT_REQS_CHECKSUM=$(sha256sum $REQS_FILE | awk '{ print $1 }')

# Check if the checksum file exists and if the checksum has changed
if [ ! -f "$REQS_CHECKSUM_FILE" ] || [ "$(cat $REQS_CHECKSUM_FILE)" != "$CURRENT_REQS_CHECKSUM" ]; then
    echo "requirements.txt has changed, installing dependencies..."
    pip install -r $REQS_FILE
    # Store the new checksum
    echo -n "$CURRENT_REQS_CHECKSUM" > $REQS_CHECKSUM_FILE
else
    echo "requirements.txt has not changed, skipping installation."
fi

# --- Data Processing ---
# Calculate the current checksum of process_data.py
CURRENT_PROCESS_DATA_CHECKSUM=$(sha256sum $PROCESS_DATA_FILE | awk '{ print $1 }')

# Check if the checksum file exists and if the checksum has changed
if [ ! -f "$PROCESS_DATA_CHECKSUM_FILE" ] || [ "$(cat $PROCESS_DATA_CHECKSUM_FILE)" != "$CURRENT_PROCESS_DATA_CHECKSUM" ]; then
    echo "process_data.py has changed, regenerating database..."
    python $PROCESS_DATA_FILE
    # Store the new checksum
    echo -n "$CURRENT_PROCESS_DATA_CHECKSUM" > $PROCESS_DATA_CHECKSUM_FILE
else
    echo "process_data.py has not changed, skipping database generation."
fi

echo "Build script finished." 