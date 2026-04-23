"""Launch SLAM Toolbox with chapter-11-specific parameters."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    pkg_share = get_package_share_directory("go2_slam")
    params_file = os.path.join(pkg_share, "config", "slam_toolbox_params.yaml")
    rviz_file = os.path.join(pkg_share, "config", "slam.rviz")

    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
    )
    use_rviz = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
    )

    slam_toolbox_node = Node(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        parameters=[params_file, {"use_sim_time": LaunchConfiguration("use_sim_time")}],
        output="screen",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_file] if os.path.exists(rviz_file) else [],
        condition=IfCondition(LaunchConfiguration("use_rviz")),
        output="screen",
    )

    return LaunchDescription(
        [
            use_sim_time,
            use_rviz,
            slam_toolbox_node,
            rviz_node,
        ]
    )
