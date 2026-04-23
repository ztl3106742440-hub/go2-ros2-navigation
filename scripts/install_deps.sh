#!/usr/bin/env bash
set -euo pipefail

if [ "$(id -u)" -eq 0 ]; then
  echo "Do not run this script with sudo; it will call sudo only for apt." >&2
  exit 1
fi

sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-rosdep \
  ros-humble-desktop \
  ros-humble-joint-state-publisher \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-nav2-map-server \
  ros-humble-pointcloud-to-laserscan \
  ros-humble-rmw-cyclonedds-cpp \
  ros-humble-robot-state-publisher \
  ros-humble-rosidl-generator-dds-idl \
  ros-humble-slam-toolbox \
  ros-humble-teleop-twist-keyboard \
  ros-humble-tf2-tools \
  ros-humble-twist-mux \
  ros-humble-xacro

if ! rosdep version >/dev/null 2>&1; then
  echo "rosdep is not available after installation." >&2
  exit 1
fi

if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then
  sudo rosdep init || true
fi

rosdep update
