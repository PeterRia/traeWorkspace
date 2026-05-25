# 从Flask框架导入Flask类
from flask import Flask

# 创建Flask应用实例
app = Flask(__name__)

# 路由示例：Flask使用@app.route装饰器将URL映射到Python函数

# 定义根路由 '/' 
# 当用户访问网站根目录时，调用index函数
@app.route('/')
def index():
    """
    首页视图函数
    
    处理根URL '/' 的GET请求
    返回网站的首页内容
    """
    return '首页'

# 定义 '/about' 路由
# 当用户访问 /about 路径时，调用about函数
@app.route('/about')
def about():
    """
    关于页面视图函数
    
    处理 '/about' URL的GET请求
    返回关于我们页面的内容
    """
    return '关于我们'

# 定义 '/contact' 路由
# 当用户访问 /contact 路径时，调用contact函数
@app.route('/contact')
def contact():
    """
    联系页面视图函数
    
    处理 '/contact' URL的GET请求
    返回联系我们页面的内容
    """
    return '联系我们'

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)