#!/usr/bin/env bash
# Deploy a dashboard source (e.g. dashboards/tablet2.yaml) to Home Assistant.
# Copies the dashboards folder + deploy_dashboard.py to the HA host and runs it
# there (the Mac can't reach the HA websocket directly; the SSH add-on can).
# Usage: scripts/deploy_dashboard.sh dashboards/tablet2.yaml
set -euo pipefail
HA_HOST="${HA_HOST:-root@192.168.4.4}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:?usage: $0 dashboards/<name>.yaml}"

ssh "$HA_HOST" 'mkdir -p /tmp/dashdeploy/dashboards'
scp -q "$REPO"/dashboards/* "$HA_HOST":/tmp/dashdeploy/dashboards/
scp -q "$REPO/scripts/deploy_dashboard.py" "$HA_HOST":/tmp/dashdeploy/
ssh "$HA_HOST" "PYTHONPATH=/tmp/pylib python3 /tmp/dashdeploy/deploy_dashboard.py /tmp/dashdeploy/$SRC"
