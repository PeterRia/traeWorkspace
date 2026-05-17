# 从Flask框架导入Flask类和render_template函数
from flask import Flask, render_template

# 创建Flask应用实例
# Flask会自动在static文件夹中查找静态文件（CSS、JavaScript、图片等）
app = Flask(__name__)

@app.route('/')
def index():
    """
    首页视图函数
    
    渲染包含静态文件引用的HTML模板
    静态文件通过url_for('static', filename='...')方式引用
    """
    return render_template('index.html')

# 确保这个脚本直接运行时才启动服务器
if __name__ == '__main__':
    # 启动Flask开发服务器，开启调试模式
    app.run(debug=True)