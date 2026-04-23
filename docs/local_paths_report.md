# 本地路径检查报告

检查命令：

```bash
./scripts/check_local_paths.sh
```

结论：

- 运行源码中不应出现 `/home/ztl`、`go2_tutorial_ws`、`unitree_go2_ws`、`unitree_ros2` 这类开发机路径。
- README 和本报告里的路径是使用示例，不参与运行。
- `src/go2_navigation/config/nav2_params.yaml` 中的 `/opt/ros/humble/...` 是 ROS Humble 安装目录，属于目标环境依赖，不是开发机本地路径。
- `ros2 launch ... --show-args` 会显示当前 clone/build 目录下的 `install/...` 绝对路径；这是 ROS 包索引运行时生成的，不是源码写死路径。

保留的路径参数：

- `ros2 launch go2_navigation navigation.launch.py map:=/your/absolute/path/my_map.yaml`：允许用户显式传入自己的地图绝对路径。
- 默认地图已随包安装：`src/go2_navigation/maps/my_map.yaml`，clone 后可直接运行默认导航脚本。
