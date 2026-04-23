#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

rg -n \
  '(/home/ztl|go2_tutorial_ws|unitree_go2_ws|unitree_ros2|/absolute/path|xacro/home)' \
  --glob '!**/README.md' \
  src maps || true
