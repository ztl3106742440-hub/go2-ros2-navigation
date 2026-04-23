# GitHub 上传说明

当前本地仓库路径：

```bash
cd /home/ztl/Go2_2DNav
```

如果 `gh auth status` 显示 token 失效，先重新登录：

```bash
gh auth login -h github.com
```

创建公开仓库并推送：

```bash
cd /home/ztl/Go2_2DNav
gh repo create ztl3106742440-hub/Go2_2DNav --public --source=. --remote=origin --push
```

如果 GitHub 上已经手动创建了同名仓库，则执行：

```bash
cd /home/ztl/Go2_2DNav
git remote add origin https://github.com/ztl3106742440-hub/Go2_2DNav.git
git push -u origin main
```
