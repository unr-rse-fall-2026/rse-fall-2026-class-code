#!/usr/bin/env bash

# This file must be sourced so its exports affect the current terminal.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "Run this with: source ${BASH_SOURCE[0]} TEAM_NUMBER" >&2
  exit 1
fi

if [[ $# -ne 1 || ! "$1" =~ ^[0-9]+$ ]]; then
  echo "Usage: source ${BASH_SOURCE[0]} TEAM_NUMBER" >&2
  return 2
fi

export ROS_DOMAIN_ID="$1"
export GZ_PARTITION="rse_lab_$1"

# ros2cli daemons are domain-specific. Stop an old one before changing domains.
ros2 daemon stop >/dev/null 2>&1 || true

echo "ROS_DOMAIN_ID=${ROS_DOMAIN_ID}"
echo "GZ_PARTITION=${GZ_PARTITION}"
