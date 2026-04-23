#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
set +u
source /opt/ros/humble/setup.bash
set -u

cd "${ROOT}"
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
colcon build --symlink-install --allow-overriding unitree_api unitree_go

echo
echo "Build finished. Source the workspace with:"
echo "  source ${ROOT}/scripts/env.sh"
