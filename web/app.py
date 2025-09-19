# Web应用主文件
# 这里后面会写Flask应用

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "论文查重系统 - Web界面"

if __name__ == '__main__':
    app.run(debug=True)
