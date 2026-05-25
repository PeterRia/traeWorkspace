# 从Flask框架导入Flask类和render_template函数
# render_template函数用于渲染HTML模板
from flask import Flask, render_template

# 创建Flask应用实例
# Flask会自动在templates文件夹中查找模板文件
app = Flask(__name__)

@app.route('/')
def index():
    """
    首页视图函数
    
    演示如何使用Flask模板引擎渲染HTML页面
    将Python变量传递给HTML模板
    """
    # 定义要传递给模板的变量
    name = 'Flask'  # 用户名变量
    items = ['苹果', '香蕉', '橙子']  # 水果列表变量
    
    # 使用render_template渲染HTML模板
    # 第一个参数是模板文件名（相对于templates文件夹）
    # 其余参数是要传递给模板的变量
    # 模板中可以通过 {{ name }} 和 {{ items }} 访问这些变量
    return render_template('index.html', name=name, items=items)

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)