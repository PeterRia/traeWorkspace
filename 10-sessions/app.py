# 从Flask框架导入Flask类、session对象、redirect函数、url_for函数和request对象
# session对象用于在多个请求之间存储用户数据
from flask import Flask, session, redirect, url_for, request

# 创建Flask应用实例
app = Flask(__name__)

# 设置应用的密钥，用于加密会话数据
# 在生产环境中，应该使用一个随机生成的复杂密钥
app.secret_key = 'your-secret-key-here'

# 会话示例：Flask会话允许在多个请求之间存储用户数据

# 定义登录路由，同时支持GET和POST方法
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录页面视图函数
    
    GET请求：显示登录表单
    POST请求：处理登录请求，将用户名存储到会话中
    
    会话数据存储在服务器端，通过安全的cookie与客户端关联
    """
    # 检查请求方法
    if request.method == 'POST':
        # 获取表单中的用户名并存储到会话中
        # session['username'] = ... 会在会话中创建或更新'username'键
        session['username'] = request.form['username']
        
        # 重定向到用户个人资料页面
        return redirect(url_for('profile'))
    
    # 如果是GET请求，显示登录表单
    # 这里直接返回HTML字符串，而不是渲染模板
    return '''
        <form method="POST">
            <input type="text" name="username">
            <button type="submit">登录</button>
        </form>
    '''

# 定义用户个人资料路由
@app.route('/profile')
def profile():
    """
    用户个人资料页面视图函数
    
    从会话中获取用户名并显示欢迎信息
    如果用户未登录（会话中没有'username'），会引发KeyError
    """
    # 从会话中获取用户名
    # session['username'] 会获取会话中存储的用户名
    return f'欢迎回来, {session["username"]}!'

# 定义退出登录路由
@app.route('/logout')
def logout():
    """
    退出登录视图函数
    
    从会话中移除用户名，实现退出登录功能
    session.pop('username', None) 会安全地移除'username'键
    如果键不存在，不会引发错误，而是返回None
    """
    # 从会话中移除用户名
    session.pop('username', None)
    
    return '已退出登录'

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)