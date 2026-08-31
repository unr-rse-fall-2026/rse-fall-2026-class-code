#!/usr/bin/env bash
set -euo pipefail

required_topics=(/clock /cmd_vel /odom /scan)
missing=0

for topic in "${required_topics[@]}"; do
  if ros2 topic list | grep -Fxq "${topic}"; then
    printf 'OK: %s exists\n' "${topic}"
  else
    printf 'MISSING: %s\n' "${topic}" >&2
    missing=1
  fi
done

if [[ "${missing}" -ne 0 ]]; then
  echo "Launch the simulator before running this test." >&2
  exit 1
fi

echo "Waiting for one odometry message..."
timeout 10 ros2 topic echo /odom --once >/dev/null

echo "Waiting for one laser scan..."
timeout 10 ros2 topic echo /scan --once >/dev/null

echo "Publishing a brief forward command..."
timeout 1 ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.15}, angular: {z: 0.0}}" >/dev/null 2>&1 || true
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.0}}" >/dev/null

echo "PASS: bridge topics are present and producing data."
