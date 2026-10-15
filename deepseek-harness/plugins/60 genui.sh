#!/bin/sh
set -eu
#dsh plugin --profile web add dsh-genui
PLUGIN="dsh-genui"
PROFILE="${DSH_PROFILE:-web}"
MARKER_DIR="${DSH_HOME:-/root/.dsh}/profiles/${PROFILE}/node_modules/${PLUGIN}"
LOGNAME="60-${PLUGIN}"

# Идемпотентность: если плагин уже стоит — выходим.
if [ -d "$MARKER_DIR" ]; then
  echo "[$LOGNAME] $PLUGIN already installed. Skipping."
  exit 0
fi

echo "[$LOGNAME] Installing $PLUGIN into profile '$PROFILE'..."
dsh plugin --profile "$PROFILE" add "$PLUGIN"

echo "[$LOGNAME] Done."