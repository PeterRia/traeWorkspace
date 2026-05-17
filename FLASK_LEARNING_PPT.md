# Flask 入门学习 PPT

---

## 幻灯片 1：封面

# Flask 入门学习

## Python Web 开发框架

---

## 幻灯片 2：什么是 Flask？

### Flask 简介
- 轻量级 Python Web 框架
- 简洁、灵活、易于学习
- 遵循 WSGI 标准

### Flask 的特点
- 微框架：只提供核心功能
- 可扩展：通过插件扩展功能
- 易学易用：适合初学者

---

## 幻灯片 3：环境准备

### 安装步骤

```bash
# 安装 Python 3.10+
# 安装 Flask
pip install flask
```

### 验证安装

```bash
python -c "import flask; print(flask.__version__)"
```

---

## 幻灯片 4：第一个 Flask 应用

### 最小应用示例

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

if __name__ == '__main__':
    app.run(debug=True)
```

### 运行方式

```bash
python app.py
```

访问：http://localhost:5000

---

## 幻灯片 5：路由基础

### 什么是路由？
- URL 到 Python 函数的映射
- 使用 `@app.route()` 装饰器

### 多路由示例

```python
@app.route('/')
def index():
    return '首页'

@app.route('/about')
def about():
    return '关于我们'

@app.route('/contact')
def contact():
    return '联系我们'
```

---

## 幻灯片 6：HTTP 方法

### 常见 HTTP 方法
- GET：获取数据（默认）
- POST：提交数据

### 指定方法

```python
@app.route('/post-data', methods=['POST'])
def post_data():
    return '这是 POST 请求'

@app.route('/both', methods=['GET', 'POST'])
def both_methods():
    if request.method == 'GET':
        return 'GET 请求'
    else:
        return 'POST 请求'
```

---

## 幻灯片 7：模板渲染

### Jinja2 模板引擎

```python
from flask import render_template

@app.route('/')
def index():
    name = 'Flask'
    items = ['苹果', '香蕉', '橙子']
    return render_template('index.html', name=name, items=items)
```

### 模板文件 templates/index.html

```html
<h1>Hello, {{ name }}!</h1>
<ul>
    {% for item in items %}
    <li>{{ item }}</li>
    {% endfor %}
</ul>
```

---

## 幻灯片 8：静态文件

### 静态文件目录结构

```
app.py
templates/
    index.html
static/
    style.css
    script.js
```

### 在模板中引用

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<script src="{{ url_for('static', filename='script.js') }}"></script>
```

---

## 幻灯片 9：URL 参数

### 动态路由

```python
@app.route('/user/<username>')
def user_profile(username):
    return f'欢迎, {username}!'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'文章 ID: {post_id}'
```

### 参数类型
- `string`：字符串（默认）
- `int`：整数
- `float`：浮点数

---

## 幻灯片 10：查询参数

### 获取 URL 查询参数

```python
from flask import request

@app.route('/search')
def search():
    keyword = request.args.get('q')
    page = request.args.get('page', default=1, type=int)
    return f'搜索: {keyword}, 页码: {page}'
```

### 访问示例

```
http://localhost:5000/search?q=python&page=2
```

---

## 幻灯片 11：表单处理

### 接收表单数据

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return f'用户: {username}'
    return render_template('login.html')
```

### HTML 表单

```html
<form method="POST">
    <input type="text" name="username">
    <input type="password" name="password">
    <button type="submit">登录</button>
</form>
```

---

## 幻灯片 12：重定向

### 页面跳转

```python
from flask import redirect, url_for

@app.route('/old-page')
def old_page():
    return redirect('/new-page')

@app.route('/go-home')
def go_home():
    return redirect(url_for('index'))
```

### url_for 优势
- 自动生成 URL
- 修改路由时无需修改链接

---

## 幻灯片 13：Session 会话

### 配置和使用

```python
app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/login', methods=['POST'])
def login():
    session['username'] = request.form['username']
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return f'欢迎, {session["username"]}'
```

### 注意事项
- 需要设置 secret_key
- 会话数据存储在客户端 Cookie 中

---

## 幻灯片 14：数据库操作

### SQLite 示例

```python
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return str(posts)
```

---

## 幻灯片 15：学习总结

### 已学知识点
1. Flask 基础结构
2. 路由和视图函数
3. HTTP 方法
4. 模板和静态文件
5. 请求参数处理
6. 表单和会话
7. 数据库操作

### 学习建议
- 多动手实践
- 阅读官方文档
- 尝试小项目

---

## 幻灯片 16：练习时间

### 动手练习

1. 创建一个 Flask 应用
2. 添加首页和关于页面
3. 创建一个简单的表单
4. 使用模板渲染页面

### 扩展挑战
- 添加用户登录功能
- 连接数据库存储数据

---

## 幻灯片 17：资源推荐

### 学习资源
- Flask 官方文档：https://flask.palletsprojects.com/
- Flask 中文文档：https://dormousehole.readthedocs.io/
- GitHub 示例项目

### 下一步
- Flask-SQLAlchemy（ORM）
- Flask-WTF（表单验证）
- Flask-RESTful（API）

---

## 幻灯片 18：结束

# 谢谢观看！

## Happy Coding!

---