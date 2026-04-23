#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"${ROOT}/scripts/install_deps.sh"
"${ROOT}/scripts/build.sh"

echo
echo "Setup finished. For a real Go2, run:"
echo "  cd ${ROOT}"
echo "  GO2_NET_IFACE=<robot_network_interface> ./scripts/run_navigation.sh"
