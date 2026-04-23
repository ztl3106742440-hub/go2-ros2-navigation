#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/env.sh"

MAP="${1:-${ROOT}/src/go2_navigation/maps/my_map.yaml}"

exec ros2 launch go2_navigation navigation.launch.py map:="${MAP}"
