# 从Flask框架导入Flask类
from flask import Flask

# 创建Flask应用实例
# __name__ 是当前模块的名称，Flask用它来确定资源路径
app = Flask(__name__)

# 使用@app.route装饰器定义路由
# '/' 表示根URL路径
@app.route('/')
def hello_world():
    """
    处理根URL请求的视图函数
    
    当用户访问网站根目录时，会调用此函数
    返回简单的文本响应 'Hello, Flask!'
    """
    return 'Hello, Flask!'

# 确保这个脚本直接运行时才启动服务器
# 如果是被导入的模块，则不启动
if __name__ == '__main__':
    # 启动Flask开发服务器
    # debug=True 开启调试模式，提供以下功能：
    # 1. 代码修改后自动重载
    # 2. 出错时显示详细的错误页面
    # 3. 输出详细的日志信息
    app.run(debug=True)