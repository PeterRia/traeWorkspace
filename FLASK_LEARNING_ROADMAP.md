# Flask 学习路线图

---

## 第一阶段：基础入门

### 1.1 环境准备
- 安装 Python
- 安装 Flask：`pip install flask`
- 了解虚拟环境（可选）

### 1.2 第一个 Flask 应用
- 创建 Flask 实例
- 定义路由和视图函数
- 运行开发服务器

**参考示例：** `01-hello-world/`

### 1.3 路由基础
- `@app.route()` 装饰器
- 定义多个路由
- 路由命名规范

**参考示例：** `02-routing/`

### 1.4 HTTP 方法
- GET 和 POST 方法
- `methods` 参数
- 判断请求类型

**参考示例：** `03-http-methods/`

---

## 第二阶段：模板与静态文件

### 2.1 Jinja2 模板引擎
- `render_template()` 函数
- 变量传递 `{{ variable }}`
- 模板语法（循环、条件）

**参考示例：** `04-templates/`

### 2.2 静态文件管理
- static 文件夹
- `url_for()` 引用静态资源
- CSS、JavaScript、图片

**参考示例：** `05-static-files/`

---

## 第三阶段：请求与响应

### 3.1 URL 参数
- 动态路由参数 `<param>`
- 参数类型转换器
- 多参数路由

**参考示例：** `06-url-parameters/`

### 3.2 查询参数
- `request.args` 获取查询参数
- 默认值设置
- 类型转换

**参考示例：** `07-query-parameters/`

### 3.3 表单处理
- `request.form` 获取表单数据
- POST 方法接收表单
- HTML 表单结构

**参考示例：** `08-forms/`

### 3.4 重定向
- `redirect()` 函数
- `url_for()` 反向生成 URL

**参考示例：** `09-redirects/`

---

## 第四阶段：会话管理

### 4.1 Session 会话
- `session` 对象
- `app.secret_key` 配置
- 会话数据的增删改查

**参考示例：** `10-sessions/`

---

## 第五阶段：数据库基础

### 5.1 SQLite 操作
- sqlite3 模块
- 创建连接和表
- INSERT、SELECT 查询

**参考示例：** `11-sqlite-basic/`

---

## 学习建议

### 学习顺序
1. 先运行每个示例，观察输出结果
2. 修改代码，理解每一行的作用
3. 尝试扩展功能，巩固知识点

### 练习建议
- 每个知识点完成后，自己动手写一个类似的小例子
- 尝试组合多个知识点完成一个小项目
- 记录遇到的问题和解决方案

### 资源推荐
- Flask 官方文档：https://flask.palletsprojects.com/
- Jinja2 模板文档：https://jinja.palletsprojects.com/

---

## 下一步学习方向

完成基础学习后，可以继续学习：
1. Flask-SQLAlchemy（ORM）
2. Flask-WTF（表单验证）
3. Flask-Login（用户认证）
4. Flask-RESTful（REST API）
5. 部署到服务器