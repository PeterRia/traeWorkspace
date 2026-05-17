# GitHub 系统学习指南

---

## 目录

1. [GitHub 简介与起源](#1-github-简介与起源)
2. [Git 基础概念](#2-git-基础概念)
3. [GitHub 注册与配置](#3-github-注册与配置)
4. [仓库基础操作](#4-仓库基础操作)
5. [分支管理](#5-分支管理)
6. [协作开发流程](#6-协作开发流程)
7. [Pull Request](#7-pull-request)
8. [Issues 管理](#8-issues-管理)
9. [GitHub Pages](#9-github-pages)
10. [学习资源推荐](#10-学习资源推荐)

---

## 1. GitHub 简介与起源

### 1.1 什么是 GitHub

GitHub 是一个基于 Git 的代码托管平台，提供版本控制和协作功能。

### 1.2 起源故事

- **2008年**：由 Chris Wanstrath、P.J. Hyett、Tom Preston-Werner 和 Scott Chacon 共同创立
- **初衷**：为开源项目提供一个友好的协作平台
- **发展**：
  - 2012年拥有 300 万用户
  - 2018年被微软以 75 亿美元收购
  - 2023年拥有超过 1 亿用户

### 1.3 GitHub 的核心价值

| 功能 | 说明 |
|------|------|
| 代码托管 | 安全存储代码，支持版本回溯 |
| 协作开发 | 多人同时开发同一项目 |
| 版本控制 | 追踪代码变更历史 |
| 社区互动 | Issue、PR、讨论等 |

---

## 2. Git 基础概念

### 2.1 什么是 Git

Git 是一个分布式版本控制系统，由 Linus Torvalds 在 2005 年创建。

### 2.2 核心概念

**仓库 (Repository)**
- 项目的容器，包含所有文件和历史记录

**提交 (Commit)**
- 代码的一次快照
- 每次提交都有唯一的哈希值

**分支 (Branch)**
- 并行开发的独立线路
- 默认分支通常是 `main` 或 `master`

**远程仓库 (Remote)**
- 存储在网络上的仓库副本
- GitHub 上的仓库就是远程仓库

### 2.3 Git 工作流程

```
工作区 → 暂存区 → 本地仓库 → 远程仓库
  ↓        ↓         ↓           ↓
 modify  add      commit      push
```

---

## 3. GitHub 注册与配置

### 3.1 注册账号

1. 访问 [github.com](https://github.com)
2. 填写用户名、邮箱、密码
3. 验证邮箱

### 3.2 安装 Git

**Windows**
- 下载：[git-scm.com/download/win](https://git-scm.com/download/win)
- 安装时保持默认选项

**macOS**
```bash
brew install git
```

**Linux**
```bash
sudo apt install git
```

### 3.3 配置 Git

```bash
# 配置用户名
git config --global user.name "Your Name"

# 配置邮箱（必须与 GitHub 账号一致）
git config --global user.email "your.email@example.com"

# 查看配置
git config --list
```

### 3.4 设置 SSH 密钥（推荐）

**生成 SSH 密钥**
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

**添加到 GitHub**
1. 复制公钥内容：
   ```bash
   # Windows
   clip < ~/.ssh/id_ed25519.pub
   
   # macOS
   pbcopy < ~/.ssh/id_ed25519.pub
   
   # Linux
   xclip -sel clip < ~/.ssh/id_ed25519.pub
   ```
2. 打开 GitHub → Settings → SSH and GPG keys
3. 点击 "New SSH key" 粘贴并保存

---

## 4. 仓库基础操作

### 4.1 创建仓库

**方式一：网页创建**
1. 点击 GitHub 右上角的 `+` → "New repository"
2. 填写仓库名称
3. 选择公开或私有
4. 可选：添加 README、.gitignore、许可证

**方式二：本地创建后推送**
```bash
# 创建本地仓库
mkdir my-project
cd my-project
git init

# 添加文件
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit"

# 关联远程仓库
git remote add origin https://github.com/your-username/my-project.git

# 推送到远程
git push -u origin main
```

### 4.2 克隆仓库

```bash
# HTTPS 方式
git clone https://github.com/username/repo-name.git

# SSH 方式（推荐）
git clone git@github.com:username/repo-name.git
```

### 4.3 基础操作命令

```bash
# 查看状态
git status

# 添加文件到暂存区
git add filename.txt
git add .  # 添加所有文件

# 提交
git commit -m "commit message"

# 推送到远程
git push origin main

# 从远程拉取
git pull origin main
```

---

## 5. 分支管理

### 5.1 创建分支

```bash
# 创建并切换到新分支
git checkout -b feature-branch

# 或者分开执行
git branch feature-branch
git checkout feature-branch
```

### 5.2 查看分支

```bash
# 查看所有分支
git branch -a

# 查看当前分支
git branch
```

### 5.3 合并分支

```bash
# 切换到主分支
git checkout main

# 合并 feature-branch 到 main
git merge feature-branch
```

### 5.4 删除分支

```bash
# 删除本地分支
git branch -d feature-branch

# 删除远程分支
git push origin --delete feature-branch
```

### 5.5 分支命名规范

| 分支类型 | 命名示例 | 用途 |
|---------|---------|------|
| feature | feature/login | 新功能开发 |
| bugfix | bugfix/login-error | 修复 Bug |
| hotfix | hotfix/critical-issue | 紧急修复 |
| release | release/v1.0 | 发布版本 |

---

## 6. 协作开发流程

### 6.1 Fork 仓库

1. 访问目标仓库页面
2. 点击右上角 "Fork" 按钮
3. 等待复制完成

### 6.2 克隆 Fork 的仓库

```bash
git clone git@github.com:your-username/forked-repo.git
```

### 6.3 添加上游仓库

```bash
git remote add upstream https://github.com/original-owner/original-repo.git
```

### 6.4 同步上游更新

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

---

## 7. Pull Request

### 7.1 创建 Pull Request

1. 在自己的分支上完成开发
2. 推送到自己的 GitHub 仓库
3. 访问原始仓库页面
4. 点击 "Compare & pull request"
5. 填写标题和描述
6. 点击 "Create pull request"

### 7.2 PR 审查流程

1. 团队成员审查代码
2. 提出修改意见
3. 在分支上进行修改
4. 自动更新 PR
5. 审查通过后合并

### 7.3 合并方式

| 方式 | 特点 | 适用场景 |
|------|------|---------|
| Merge | 保留完整历史 | 公共项目 |
| Squash | 合并为一个提交 | 清理历史 |
| Rebase | 线性历史 | 个人项目 |

---

## 8. Issues 管理

### 8.1 创建 Issue

1. 访问仓库的 Issues 页面
2. 点击 "New issue"
3. 选择模板（如果有）
4. 填写标题和描述
5. 点击 "Submit new issue"

### 8.2 Issue 标签

| 标签类型 | 示例 |
|---------|------|
| bug | 代码错误 |
| feature | 功能需求 |
| enhancement | 改进建议 |
| documentation | 文档问题 |
| help wanted | 需要帮助 |

### 8.3 Issue 状态

- **Open**：待处理
- **Closed**：已解决
- **Locked**：锁定讨论

---

## 9. GitHub Pages

### 9.1 什么是 GitHub Pages

免费的静态网站托管服务，支持：
- 个人主页
- 项目文档
- 博客

### 9.2 创建 GitHub Pages

**方式一：使用 main 分支的 docs 文件夹**
1. 创建 `docs` 文件夹
2. 添加 HTML 文件或使用 Jekyll
3. 配置：Settings → Pages → Source

**方式二：使用 gh-pages 分支**
```bash
git checkout -b gh-pages
# 添加静态文件
git push origin gh-pages
```

### 9.3 访问地址

```
https://username.github.io/repo-name/
```

---

## 10. 学习资源推荐

### 10.1 官方资源

- [GitHub 官方文档](https://docs.github.com/)
- [GitHub Learning Lab](https://lab.github.com/)
- [Git 官方文档](https://git-scm.com/docs)

### 10.2 学习网站

- [Learn Git Branching](https://learngitbranching.js.org/) - 交互式学习
- [Git Immersion](https://gitimmersion.com/) - 实践教程
- [Pro Git 中文版](https://git-scm.com/book/zh/v2)

### 10.3 视频教程

- YouTube: GitHub Guides 系列
- B 站：Git 和 GitHub 教程

---

## 练习清单

- [ ] 注册 GitHub 账号
- [ ] 配置 Git 和 SSH 密钥
- [ ] 创建第一个仓库
- [ ] 克隆一个仓库
- [ ] 创建并切换分支
- [ ] 提交并推送代码
- [ ] Fork 一个仓库并提交 PR
- [ ] 创建一个 Issue
- [ ] 部署 GitHub Pages

---

## 常用命令速查

```bash
# 配置
git config --global user.name "Name"
git config --global user.email "email"

# 仓库操作
git init              # 初始化仓库
git clone <url>       # 克隆仓库
git remote add <name> <url>  # 添加远程仓库

# 文件操作
git add <file>        # 添加文件
git commit -m "msg"   # 提交
git status            # 查看状态
git log               # 查看日志

# 分支操作
git branch            # 查看分支
git checkout -b <name> # 创建并切换分支
git merge <branch>    # 合并分支

# 远程操作
git push <remote> <branch>  # 推送
git pull <remote> <branch>  # 拉取
git fetch <remote>          # 获取远程更新
```

---

*祝你学习愉快！🚀*
