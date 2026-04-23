# Go2_2DNav

Unitree Go2 第 11/12 章 2D SLAM 建图和 Nav2 实机导航基线代码包。这个仓库只保留 2D 建图/导航相关运行链，已经带上本链路必需的 Go2 描述、驱动适配、速度桥接、传感器预处理、SLAM、Nav2 配置、Unitree ROS2 消息包和示例地图。

## 环境要求

- Ubuntu 22.04
- ROS 2 Humble
- Unitree Go2 EDU/L1 雷达实机，电脑通过网线连接 Go2
- 机器人网口 IPv4 通常设为 `192.168.123.99/24`
- 如果只做编译检查，可以不连接机器人，默认使用 `lo` 回环网卡

## 一键克隆和配置

```bash
git clone https://github.com/ztl3106742440-hub/Go2_2DNav.git
cd Go2_2DNav
./scripts/setup_all.sh
```

如果电脑已经装好 ROS 2 Humble 和相关依赖，也可以只构建：

```bash
cd Go2_2DNav
./scripts/build.sh
```

## 一键运行导航

先确认电脑连接 Go2 的网卡名：

```bash
ip -br link
```

假设网卡名是 `enp3s0`，运行第 12 章 Nav2 基线：

```bash
cd Go2_2DNav
GO2_NET_IFACE=enp3s0 ./scripts/run_navigation.sh
```

默认地图路径是：

```text
Go2_2DNav/src/go2_navigation/maps/my_map.yaml
```

使用自己的地图时，把 `.yaml` 和 `.pgm` 放在同一目录，然后显式传入：

```bash
cd Go2_2DNav
GO2_NET_IFACE=enp3s0 ./scripts/run_navigation.sh /absolute/path/to/my_map.yaml
```

RViz 弹出后必须先点 `2D Pose Estimate` 给 AMCL 初始位姿，粒子云收敛后再点 `2D Goal Pose` 发导航目标。

## 一键运行建图

```bash
cd Go2_2DNav
GO2_NET_IFACE=enp3s0 ./scripts/run_mapping.sh
```

保存地图示例：

```bash
source scripts/env.sh
mkdir -p maps
ros2 run nav2_map_server map_saver_cli -f maps/my_new_map
```

保存后会得到：

```text
maps/my_new_map.yaml
maps/my_new_map.pgm
```

如果要让导航默认使用新地图，复制到：

```bash
cp maps/my_new_map.yaml src/go2_navigation/maps/my_map.yaml
cp maps/my_new_map.pgm src/go2_navigation/maps/my_map.pgm
./scripts/build.sh
```

## 本仓库包含什么

- `src/go2_sensors`：点云时间戳修复、`PointCloud2 -> LaserScan` 启动配置。
- `src/go2_slam`：第 11 章 SLAM Toolbox 建图启动和参数。
- `src/go2_navigation`：第 12 章 Nav2、AMCL、costmap、twist_mux、RViz 配置。
- `src/go2_driver_py`：订阅 Unitree 状态并发布 `/odom`、`odom -> base`、`/joint_states`。
- `src/go2_twist_bridge_py`：把 `/cmd_vel` 转成 Unitree `/api/sport/request`。
- `src/go2_description`：Go2 URDF 和可视化 mesh。
- `src/unitree_api`、`src/unitree_go`：Unitree ROS2 消息定义，避免用户另装 `unitree_ros2` 后才能编译。
- `maps/`：示例地图备份；运行默认使用 `src/go2_navigation/maps/my_map.yaml`。

## 本地路径说明

运行源码中不应依赖老大的本机路径，例如 `/home/ztl/go2_tutorial_ws` 或 `/home/ztl/unitree_ros2`。本仓库已经改成用包路径和脚本自动定位仓库根目录。

需要注意的路径只有这些：

- `/opt/ros/humble/setup.bash`：ROS 2 Humble 的系统安装路径，所有 Humble 环境都应存在。
- `/opt/ros/humble/share/nav2_bt_navigator/...`：Nav2 官方行为树 XML 路径，来自 `ros-humble-nav2-bringup/nav2-bt-navigator`。
- `Go2_2DNav/install/setup.bash`：本仓库 `colcon build` 后生成。
- `Go2_2DNav/src/go2_navigation/maps/my_map.yaml`：默认导航地图。
- `/absolute/path/to/my_map.yaml`：README 中的占位示例，换成用户自己的地图绝对路径。

检查命令：

```bash
./scripts/check_local_paths.sh
```

## 常用排错

- `package 'go2_navigation' not found`：还没构建或没 source，执行 `./scripts/build.sh` 后再跑。
- `Waiting for transform map -> base_footprint`：配置串到默认 Nav2 frame 了；本仓库统一使用 `base`，不要改成 `base_link/base_footprint`。
- RViz 没弹出：检查是否有图形桌面/远程 X11；没有 RViz 就不能完成 `2D Pose Estimate`。
- 收不到 Go2 话题：检查 `GO2_NET_IFACE` 是否是连接 Go2 的真实网卡名，以及电脑 IP 是否在 `192.168.123.x/24`。
- 点云/scan 没数据：确认 Go2 L1 雷达话题 `/utlidar/cloud_deskewed` 存在。

## 安全提醒

第一次运行 Nav2 时，让机器人前方至少空出 2 米，并保证有人可以随时急停或遥控接管。这个包是教学基线，不是无人值守导航系统。
