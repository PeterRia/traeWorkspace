# 从Flask框架导入Flask类、redirect函数和url_for函数
# redirect函数用于重定向到其他URL
# url_for函数用于根据视图函数名生成URL
from flask import Flask, redirect, url_for

# 创建Flask应用实例
app = Flask(__name__)

# 重定向示例：Flask可以轻松实现URL重定向

# 定义首页路由
@app.route('/')
def index():
    """
    首页视图函数
    
    返回简单的首页内容
    """
    return '首页'

# 定义旧页面路由，演示重定向
@app.route('/old-page')
def old_page():
    """
    旧页面视图函数
    
    当用户访问 /old-page 时，会自动重定向到 /new-page
    redirect() 函数返回一个重定向响应
    """
    # 重定向到新页面
    return redirect('/new-page')

# 定义新页面路由
@app.route('/new-page')
def new_page():
    """
    新页面视图函数
    
    显示新页面的内容
    """
    return '新页面'

# 定义回家路由，演示使用url_for生成URL
@app.route('/go-home')
def go_home():
    """
    回家路由视图函数
    
    使用url_for函数根据视图函数名生成URL
    url_for('index') 会生成 '/' 的URL
    这种方式比硬编码URL更灵活，因为URL变化时只需要修改路由定义
    """
    # 使用url_for生成首页URL并重定向
    return redirect(url_for('index'))

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)