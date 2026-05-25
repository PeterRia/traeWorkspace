# 从Flask框架导入Flask类和request对象
# request对象用于访问HTTP请求的详细信息，包括查询参数
from flask import Flask, request

# 创建Flask应用实例
app = Flask(__name__)

# 查询参数示例：查询参数是URL中?后面的键值对，用于传递额外信息

# 定义搜索路由，演示查询参数的使用
@app.route('/search')
def search():
    """
    搜索页面视图函数
    
    从URL查询参数中获取搜索条件
    例如：/search?q=python&page=2
    - q: 搜索关键词
    - page: 页码（可选，默认为1）
    """
    # 获取查询参数'q'的值
    # request.args 是一个字典，包含所有查询参数
    keyword = request.args.get('q')
    
    # 获取查询参数'page'的值，指定默认值和类型
    # 如果参数不存在，使用默认值1
    # type=int 会自动将字符串转换为整数
    page = request.args.get('page', default=1, type=int)
    
    return f'搜索关键词: {keyword}, 页码: {page}'

# 定义问候路由，演示带默认值的查询参数
@app.route('/greet')
def greet():
    """
    问候页面视图函数
    
    从URL查询参数中获取用户名
    例如：/greet?name=John
    如果name参数不存在，使用默认值'Guest'
    """
    # 获取查询参数'name'，如果不存在则使用默认值'Guest'
    name = request.args.get('name', 'Guest')
    
    return f'Hello, {name}!'

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)