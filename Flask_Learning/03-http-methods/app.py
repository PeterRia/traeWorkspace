# 从Flask框架导入Flask类和request对象
# request对象用于访问HTTP请求的详细信息
from flask import Flask, request

# 创建Flask应用实例
app = Flask(__name__)

# HTTP方法示例：Flask允许为同一个URL定义不同的HTTP方法处理函数

# 定义只处理GET请求的路由
# methods参数指定该路由接受的HTTP方法
@app.route('/get-data', methods=['GET'])
def get_data():
    """
    处理GET请求的视图函数
    
    当用户通过GET方法访问 /get-data 时调用
    GET请求通常用于获取数据，参数通过URL传递
    """
    return '这是 GET 请求'

# 定义只处理POST请求的路由
@app.route('/post-data', methods=['POST'])
def post_data():
    """
    处理POST请求的视图函数
    
    当用户通过POST方法访问 /post-data 时调用
    POST请求通常用于提交数据，参数通过请求体传递
    """
    return '这是 POST 请求'

# 定义同时处理GET和POST请求的路由
@app.route('/both', methods=['GET', 'POST'])
def both_methods():
    """
    处理GET和POST请求的视图函数
    
    根据请求方法返回不同的响应
    使用request.method属性判断当前请求的HTTP方法
    """
    # 检查请求方法类型
    if request.method == 'GET':
        return 'GET 请求'
    else:
        return 'POST 请求'

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)