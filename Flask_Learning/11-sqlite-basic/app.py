# 从Flask框架导入Flask类
from flask import Flask

# 导入SQLite数据库模块
# SQLite是一个轻量级的嵌入式数据库，不需要单独的服务器进程
import sqlite3

# 创建Flask应用实例
app = Flask(__name__)

# 数据库连接辅助函数
def get_db_connection():
    """
    获取数据库连接
    
    创建到SQLite数据库的连接，并设置row_factory为sqlite3.Row
    这样查询结果可以通过列名访问，而不是索引
    """
    # 连接到SQLite数据库文件（如果不存在会自动创建）
    conn = sqlite3.connect('database.db')
    
    # 设置row_factory，使查询结果可以通过列名访问
    # 例如：post["title"] 而不是 post[1]
    conn.row_factory = sqlite3.Row
    
    return conn

# 数据库初始化函数
def init_db():
    """
    初始化数据库
    
    创建posts表（如果不存在）
    表结构：
    - id: 文章ID，主键，自动递增
    - title: 文章标题，文本类型，不能为空
    - content: 文章内容，文本类型，不能为空
    """
    # 获取数据库连接
    conn = get_db_connection()
    
    # 执行SQL语句创建表
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    
    # 提交事务，保存更改
    conn.commit()
    
    # 关闭连接
    conn.close()

# 首页路由，显示所有文章
@app.route('/')
def index():
    """
    首页视图函数
    
    从数据库中查询所有文章并显示
    使用HTML格式化输出
    """
    # 获取数据库连接
    conn = get_db_connection()
    
    # 执行SQL查询，获取所有文章
    # fetchall() 返回所有查询结果
    posts = conn.execute('SELECT * FROM posts').fetchall()
    
    # 关闭连接
    conn.close()
    
    # 构建HTML响应
    result = ''
    for post in posts:
        # 通过列名访问查询结果
        result += f'<h2>{post["title"]}</h2><p>{post["content"]}</p>'
    
    return result

# 添加文章路由
@app.route('/add/<title>/<content>')
def add_post(title, content):
    """
    添加文章视图函数
    
    从URL参数获取文章标题和内容，插入到数据库中
    例如：/add/Flask教程/Flask是一个轻量级的Web框架
    """
    # 获取数据库连接
    conn = get_db_connection()
    
    # 执行SQL插入语句
    # 使用参数化查询（?占位符）防止SQL注入攻击
    conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
    
    # 提交事务，保存更改
    conn.commit()
    
    # 关闭连接
    conn.close()
    
    return f'文章 "{title}" 添加成功!'

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 初始化数据库（创建表）
    init_db()
    
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)