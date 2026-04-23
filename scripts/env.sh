#!/usr/bin/env bash
set -e

if [ -z "${BASH_VERSION:-}" ]; then
  echo "Please source this file from bash." >&2
  return 1 2>/dev/null || exit 1
fi

GO2_2DNAV_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export GO2_2DNAV_ROOT

_GO2_NOUNSET_WAS_ON=0
case $- in
  *u*) _GO2_NOUNSET_WAS_ON=1; set +u ;;
esac
source /opt/ros/humble/setup.bash

if [ -f "${GO2_2DNAV_ROOT}/install/setup.bash" ]; then
  source "${GO2_2DNAV_ROOT}/install/setup.bash"
fi
if [ "${_GO2_NOUNSET_WAS_ON}" -eq 1 ]; then
  set -u
fi
unset _GO2_NOUNSET_WAS_ON

export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_cyclonedds_cpp}"

# Real robot: set GO2_NET_IFACE to the wired interface connected to Go2, e.g.
# GO2_NET_IFACE=enp3s0 source scripts/env.sh
# Local/simulation checks: default to loopback.
GO2_NET_IFACE="${GO2_NET_IFACE:-lo}"
export GO2_NET_IFACE
export CYCLONEDDS_URI="<CycloneDDS><Domain><General><Interfaces><NetworkInterface name=\"${GO2_NET_IFACE}\" priority=\"default\" multicast=\"default\" /></Interfaces></General></Domain></CycloneDDS>"
