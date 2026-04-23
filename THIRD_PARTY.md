# Third-Party Notes

- `src/unitree_api` and `src/unitree_go` are copied from Unitree ROS2 message packages so this workspace can build without a separate `~/unitree_ros2` checkout.
- The Go2 mesh/URDF assets are included because `go2_driver_py` launches `go2_description` for TF and RViz visualization.
- ROS 2 and Nav2 dependencies are installed from Ubuntu/ROS apt packages by `scripts/install_deps.sh`.
