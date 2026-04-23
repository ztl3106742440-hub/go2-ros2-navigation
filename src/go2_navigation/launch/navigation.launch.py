"""Launch the chapter-12 Go2 Nav2 baseline stack."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    map_yaml = LaunchConfiguration("map")
    use_rviz = LaunchConfiguration("use_rviz")

    nav_share = Path(get_package_share_directory("go2_navigation"))
    sensors_share = Path(get_package_share_directory("go2_sensors"))
    driver_share = Path(get_package_share_directory("go2_driver_py"))

    nav2_params = str(nav_share / "config" / "nav2_params.yaml")
    twist_mux_params = str(nav_share / "config" / "twist_mux.yaml")
    scan_params = str(sensors_share / "config" / "pointcloud_to_laserscan_params.yaml")
    driver_launch = str(driver_share / "launch" / "driver.launch.py")

    rviz_config = str(nav_share / "rviz" / "navigation.rviz")

    driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(driver_launch),
        launch_arguments={"use_rviz": "false"}.items(),
    )

    timestamp_fix = Node(
        package="go2_sensors",
        executable="pointcloud_timestamp_fix",
        name="pointcloud_timestamp_fix",
        parameters=[
            {
                "input_topic": "/utlidar/cloud_deskewed",
                "output_topic": "/utlidar/cloud_fixed",
                # /odom 只有 20 Hz,scan 时间戳回退 0.10s,AMCL 查 odom→base 才追得上
                "backdate_sec": 0.10,
            }
        ],
        output="screen",
    )

    pointcloud_to_scan = Node(
        package="pointcloud_to_laserscan",
        executable="pointcloud_to_laserscan_node",
        name="pointcloud_to_laserscan",
        parameters=[scan_params],
        remappings=[
            ("cloud_in", "/utlidar/cloud_fixed"),
            ("scan", "/scan"),
        ],
        output="screen",
    )

    twist_mux = Node(
        package="twist_mux",
        executable="twist_mux",
        name="twist_mux",
        parameters=[twist_mux_params],
        remappings=[("cmd_vel_out", "/cmd_vel")],
        output="screen",
    )

    map_server = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        parameters=[nav2_params, {"yaml_filename": map_yaml}],
        output="screen",
    )

    amcl = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        parameters=[nav2_params],
        output="screen",
    )

    localization_lifecycle = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_localization",
        parameters=[
            {
                "use_sim_time": False,
                "autostart": True,
                "node_names": ["map_server", "amcl"],
            }
        ],
        output="screen",
    )

    planner_server = Node(
        package="nav2_planner",
        executable="planner_server",
        name="planner_server",
        parameters=[nav2_params],
        output="screen",
    )

    controller_server = Node(
        package="nav2_controller",
        executable="controller_server",
        name="controller_server",
        parameters=[nav2_params],
        remappings=[("cmd_vel", "/cmd_vel_nav")],
        output="screen",
    )

    behavior_server = Node(
        package="nav2_behaviors",
        executable="behavior_server",
        name="behavior_server",
        parameters=[nav2_params],
        remappings=[("cmd_vel", "/cmd_vel_behavior")],
        output="screen",
    )

    bt_navigator = Node(
        package="nav2_bt_navigator",
        executable="bt_navigator",
        name="bt_navigator",
        parameters=[nav2_params],
        output="screen",
    )

    navigation_lifecycle = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_navigation",
        parameters=[
            {
                "use_sim_time": False,
                "autostart": True,
                "node_names": [
                    "planner_server",
                    "controller_server",
                    "behavior_server",
                    "bt_navigator",
                ],
            }
        ],
        output="screen",
    )

    delayed_navigation = TimerAction(
        period=3.0,
        actions=[
            planner_server,
            controller_server,
            behavior_server,
            bt_navigator,
            navigation_lifecycle,
        ],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config],
        condition=IfCondition(use_rviz),
        output="screen",
    )

    return LaunchDescription(
        [
            # DeclareLaunchArgument 必须在使用 LaunchConfiguration 的 action 之前被 visit，
            # 否则 IfCondition(LaunchConfiguration("use_rviz")) 拿不到默认值，rviz 会被静默跳过
            DeclareLaunchArgument(
                "map",
                default_value=str(nav_share / "maps" / "my_map.yaml"),
                description="Path to the chapter-11 saved map yaml file.",
            ),
            DeclareLaunchArgument(
                "use_rviz",
                default_value="true",
                description="Whether to launch Nav2 RViz.",
            ),
            # 把 rviz 放到节点列表最前，避免被后续崩溃的节点拖累
            rviz,
            driver,
            timestamp_fix,
            pointcloud_to_scan,
            twist_mux,
            map_server,
            amcl,
            localization_lifecycle,
            delayed_navigation,
        ]
    )
