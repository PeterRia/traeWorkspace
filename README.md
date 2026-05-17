# Flask 学习项目

这是一个 Flask 入门学习项目，包含多个独立的知识点示例。

## 项目结构

```
├── 01-hello-world/          # 第一个 Flask 应用
├── 02-routing/              # 路由基础
├── 03-http-methods/         # HTTP 方法
├── 04-templates/            # 模板渲染
├── 05-static-files/         # 静态文件
├── 06-url-parameters/       # URL 参数
├── 07-query-parameters/     # 查询参数
├── 08-forms/                # 表单处理
├── 09-redirects/            # 重定向
├── 10-sessions/             # Session 会话
├── 11-sqlite-basic/         # SQLite 数据库
├── FLASK_LEARNING_ROADMAP.md # 学习路线图
├── FLASK_LEARNING_PPT.md    # PPT 文稿
├── requirements.txt         # 依赖列表
└── README.md               # 项目说明
```

## 环境要求

- Python 3.10+
- Flask

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行示例

每个文件夹都是独立的示例，进入对应目录运行：

```bash
cd 01-hello-world
python app.py
```

然后访问 http://localhost:5000

## 学习顺序

按照数字顺序学习即可：

1. **01-hello-world** - 基础入门
2. **02-routing** - 路由基础
3. **03-http-methods** - HTTP 方法
4. **04-templates** - 模板渲染
5. **05-static-files** - 静态文件
6. **06-url-parameters** - URL 参数
7. **07-query-parameters** - 查询参数
8. **08-forms** - 表单处理
9. **09-redirects** - 重定向
10. **10-sessions** - Session 会话
11. **11-sqlite-basic** - SQLite 数据库

## 学习资源

- 学习路线图：`FLASK_LEARNING_ROADMAP.md`
- PPT 文稿：`FLASK_LEARNING_PPT.md`
- Flask 官方文档：https://flask.palletsprojects.com/

## 注意事项

- 代码保持简洁，不包含 try-except 等复杂结构
- 每个示例独立运行，互不依赖
- 建议按顺序学习，逐步深入