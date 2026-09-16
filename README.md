<!-- 小co改动 2026-09-16：按用户要求整理仓库定位、功能、克隆运行说明和合作入口。 -->
# Go2 ROS2 Navigation · 建图、导航与机器人实验

Unitree Go2 + ROS 2 Humble：SLAM Toolbox、Nav2 实机基线，以及三维建图定位、视觉跟随、移动操作和三维规划实验索引。

## 功能与完成边界

| 内容 | 当前提供 |
| --- | --- |
| 二维建图与导航 | `src/` 和 `scripts/` 中已有实机教学基线源码与配置 |
| 雷达与机器人接口 | 点云转 LaserScan、里程计/TF、速度桥接、模型与消息 |
| 秋季实验 1～5 | [实验索引](experiments/README.md)、功能边界与验证摘要 |
| 新实验完整源码 | 目前保存在私有研发备份；公开分发权限和个人差异待逐项核对 |

本仓库的原名是 `Go2_2DNav`。二维实机基线和新增仿真实验索引分别说明，避免把实验索引误认为完整源码已经发布。

## 快速开始：现有二维实机基线

环境：Ubuntu 22.04、ROS 2 Humble；实机运行需要 Go2 EDU、SDK 通信和正确网卡。先完成下方克隆命令，再执行：

```bash
./scripts/setup_all.sh
# 或在依赖已经安装时仅编译
./scripts/build.sh
./scripts/check_local_paths.sh
```

查看网卡并将 `enp3s0` 替换为实际连接机器狗的接口：

```bash
ip -br link
GO2_NET_IFACE=enp3s0 ./scripts/run_mapping.sh
# 关闭建图后，再运行导航；不要同时起两套链路
GO2_NET_IFACE=enp3s0 ./scripts/run_navigation.sh
```

导航时先在 RViz 使用 **2D Pose Estimate** 初始化位置，再用 **2D Goal Pose** 指定目标。可传入自有地图：

```bash
GO2_NET_IFACE=enp3s0 ./scripts/run_navigation.sh /absolute/path/to/map.yaml
```

更详细的原基线说明保存在 [历史运行说明](docs/legacy/README-before-2026-09-16.md)。启动硬件前按环境与急停要求检查；本项目是教学与研发基线。

## 贡献与验证

展示内容为 Go2 接口适配、导航配置、环境兼容调试和实验复现；第三方算法来源见 [THIRD_PARTY.md](THIRD_PARTY.md)。本次仅做仓库整理和离线检查，未重新执行实机导航。

完整三维规划的 137 项单元测试通过记录来自本地实验五；它不等于本仓库当前二维基线或私有全部系统的测试结论。

## 获取与更新

安装 Git 后执行：

```bash
git clone https://github.com/ztl3106742440-hub/go2-ros2-navigation.git
cd go2-ros2-navigation
# 在没有本地未提交改动时获取更新
git pull --ff-only
```

保留自己的修改：先 `git switch -c my-experiment`，再 `git add <修改的文件>`、`git commit -m "说明修改目的"`。没有本仓库写权限时先 Fork，再向自己的仓库推送分支。

## 交流与合作

有 **Go2 机器狗二次开发、ROS 2 集成、导航与感知实验、机器人教学或项目合作** 需求，欢迎通过 [GitHub Issues](https://github.com/ztl3106742440-hub/go2-ros2-navigation/issues) 联系，说明需求目标、硬件、系统版本和期望交付内容。

涉及项目私有资料时，请先在公开 Issue 留下不敏感的需求概要，约定联系渠道后再交流。项目维护者：[TIlor](https://github.com/ztl3106742440-hub)。
