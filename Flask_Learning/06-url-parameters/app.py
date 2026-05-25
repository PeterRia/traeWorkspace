# 从Flask框架导入Flask类
from flask import Flask

# 创建Flask应用实例
app = Flask(__name__)

# URL参数示例：Flask允许在URL中定义动态部分作为参数

# 定义包含字符串参数的路由
# <username> 是URL参数，Flask会将其作为参数传递给视图函数
@app.route('/user/<username>')
def user_profile(username):
    """
    用户个人资料页面视图函数
    
    从URL中获取用户名参数
    例如：/user/john 会调用 user_profile('john')
    """
    return f'欢迎, {username}!'

# 定义包含整数参数的路由
# <int:post_id> 指定参数类型为整数
# Flask会自动进行类型转换，如果转换失败会返回404错误
@app.route('/post/<int:post_id>')
def show_post(post_id):
    """
    文章详情页面视图函数
    
    从URL中获取文章ID参数（整数类型）
    例如：/post/123 会调用 show_post(123)
    """
    return f'文章 ID: {post_id}'

# 定义包含多个参数的路由
# 可以同时使用字符串和整数类型的参数
@app.route('/product/<string:category>/<int:id>')
def product_detail(category, id):
    """
    商品详情页面视图函数
    
    从URL中获取分类名称和商品ID两个参数
    例如：/product/electronics/456 会调用 product_detail('electronics', 456)
    """
    return f'分类: {category}, 商品 ID: {id}'

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)