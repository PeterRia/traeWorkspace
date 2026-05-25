# 学习项目集合

这是一个综合性的学习项目仓库，使用 [uv](https://docs.astral.sh/uv/) 管理 Python 依赖与项目运行。

## 📁 项目结构

```
├── Flask_Learning/           # Flask Web 框架学习
│   ├── 01-hello-world/       # 基础入门示例
│   ├── 02-routing/           # 路由基础
│   ├── 03-http-methods/      # HTTP 方法
│   ├── 04-templates/         # 模板渲染
│   ├── 05-static-files/      # 静态文件管理
│   ├── 06-url-parameters/    # URL 参数
│   ├── 07-query-parameters/  # 查询参数
│   ├── 08-forms/             # 表单处理
│   ├── 09-redirects/         # 重定向
│   ├── 10-sessions/          # Session 会话
│   ├── 11-sqlite-basic/      # SQLite 数据库
│   ├── FLASK_LEARNING_ROADMAP.md  # 学习路线图
│   └── FLASK_LEARNING_PPT.md      # PPT 文稿
├── Vibe_Coding_Learning/     # Vibe Coding 系统化学习
├── github-learning/          # GitHub 学习指南
├── pyproject.toml            # uv 项目配置
└── README.md                 # 项目总览
```

## 🚀 学习模块

### 1. Flask 学习模块

从基础到进阶的完整 Flask 学习路径，包含 **11 个独立示例**：

| 序号 | 模块 | 知识点 |
|:---:|------|--------|
| 01 | hello-world | Flask 应用结构、路由装饰器、开发服务器 |
| 02 | routing | 多路由定义、路由命名规范 |
| 03 | http-methods | GET/POST 方法、请求类型判断 |
| 04 | templates | Jinja2 模板引擎、变量传递、模板语法 |
| 05 | static-files | 静态资源管理、CSS/JavaScript/图片 |
| 06 | url-parameters | 动态路由、参数类型转换器 |
| 07 | query-parameters | URL 查询参数、默认值设置 |
| 08 | forms | 表单数据处理、POST 请求 |
| 09 | redirects | 页面重定向、url_for 反向生成 |
| 10 | sessions | Session 会话管理、secret_key 配置 |
| 11 | sqlite-basic | SQLite 数据库连接、增删改查 |

**学习资源：**
- 📋 学习路线图：`Flask_Learning/FLASK_LEARNING_ROADMAP.md`
- 📊 PPT 文稿：`Flask_Learning/FLASK_LEARNING_PPT.md`
- 🌐 Flask 官方文档：https://flask.palletsprojects.com/

### 2. GitHub 学习模块

GitHub 使用指南，包含版本控制基础和协作开发知识。

**学习资源：**
- 📖 学习指南：`github-learning/GITHUB_LEARNING_GUIDE.md`

### 3. Vibe Coding 学习模块

基于 Easy-Vibe 官方教程的系统化 Vibe Coding 学习路径，覆盖从零基础到高级开发。

**学习资源：**
- � 学习总览：`Vibe_Coding_Learning/README.md`

---

## �️ 环境要求

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装 uv

```powershell
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## � 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/PeterRia/traeWorkspace.git
cd traeWorkspace

# 2. uv 自动创建虚拟环境并安装依赖
uv sync

# 3. 运行 Flask 示例（以 hello-world 为例）
uv run python Flask_Learning/01-hello-world/app.py
```

然后访问 http://localhost:5000

## 🔧 常用 uv 命令

| 命令 | 说明 |
|------|------|
| `uv sync` | 同步依赖，创建虚拟环境 |
| `uv run python <脚本>` | 在虚拟环境中运行 Python 脚本 |
| `uv add <包名>` | 添加新依赖 |
| `uv remove <包名>` | 移除依赖 |
| `uv lock --upgrade` | 升级所有依赖到最新版 |

## 📚 学习建议

1. **顺序学习**：按照数字顺序逐步掌握每个知识点
2. **动手实践**：修改代码，观察输出变化
3. **扩展练习**：尝试组合多个知识点完成小项目
4. **查阅文档**：遇到问题优先查看官方文档

## 📝 注意事项

- 代码保持简洁，专注于核心知识点
- 每个示例独立运行，互不依赖
- 使用 `uv run python` 替代直接 `python` 以确保在虚拟环境中运行
- 运行其他示例只需替换路径：`uv run python Flask_Learning/<目录名>/app.py`

---

**Happy Coding!**