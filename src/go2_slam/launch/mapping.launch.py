"""Launch the full chapter-11 mapping stack."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description() -> LaunchDescription:
    go2_driver_pkg = get_package_share_directory("go2_driver_py")
    go2_sensors_pkg = get_package_share_directory("go2_sensors")
    go2_slam_pkg = get_package_share_directory("go2_slam")

    # 关掉 driver 自带的 rviz，建图视角交给 slam_toolbox.launch.py 里的 slam.rviz
    go2_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(go2_driver_pkg, "launch", "driver.launch.py")
        ),
        launch_arguments={"use_rviz": "false"}.items(),
    )

    pointcloud_to_scan_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(go2_sensors_pkg, "launch", "pointcloud_to_laserscan.launch.py")
        )
    )

    # 建图场景下 slam_toolbox 的 rviz 固定要开，不再转发外层参数
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(go2_slam_pkg, "launch", "slam_toolbox.launch.py")
        ),
        launch_arguments={"use_rviz": "true"}.items(),
    )

    return LaunchDescription(
        [
            go2_driver_launch,
            pointcloud_to_scan_launch,
            slam_launch,
        ]
    )
