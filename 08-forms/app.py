# 从Flask框架导入Flask类、request对象和render_template函数
# request对象用于访问HTTP请求的详细信息，包括表单数据
from flask import Flask, request, render_template

# 创建Flask应用实例
app = Flask(__name__)

# 表单处理示例：Flask可以处理HTML表单提交的数据

# 定义登录路由，同时支持GET和POST方法
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录页面视图函数
    
    GET请求：显示登录表单
    POST请求：处理表单提交的数据
    
    表单数据通过request.form字典访问
    """
    # 检查请求方法
    if request.method == 'POST':
        # 获取表单中'username'字段的值
        # request.form 是一个字典，包含所有表单字段
        username = request.form['username']
        
        # 获取表单中'password'字段的值
        password = request.form['password']
        
        # 返回包含表单数据的响应
        # 注意：在实际应用中，不应该直接显示密码
        return f'用户名: {username}, 密码: {password}'
    
    # 如果是GET请求，渲染登录表单模板
    return render_template('login.html')

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)