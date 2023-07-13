from flask import Flask, request, render_template, url_for

from scripts import graph

app = Flask(__name__)


# 默认页面
@app.route("/")
def index():
    return render_template("index.html")


# 处理POST请求
@app.route("/", methods=["POST"])
def process():
    # 获取输入文本
    text = request.form["text"]

    if text == '':
        # text = 'Great food but the service was dreadful !'
        text = 'The tech guy then said the service center does not do 1 - to - 1 exchange and I have to direct my concern to the " sales " team , which is the retail shop which I bought my netbook from .'
    graph.generate_fig(text)

    img1 = url_for("static", filename='depgcn.png')
    img2 = url_for("static", filename='consgcn.png')
    img3 = url_for("static", filename='depconsgcn.png')
    # img3 = url_for("static", filename='depconsgcn.png')

    # 返回渲染后的页面
    return render_template("index.html", img1_url=img1, img2_url=img2, img3_url=img3)


if __name__ == "__main__":
    app.run()
