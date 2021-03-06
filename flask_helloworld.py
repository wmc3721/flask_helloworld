#!usr/bin/env python
# -*- coding:utf-8 _*-
from flask import Flask, render_template, request, redirect, url_for, make_response, abort, json
from werkzeug.routing import BaseConverter
from os import path
from werkzeug.utils import secure_filename
from flask_script import Manager
from flask_json import json_response, FlaskJSON, JsonTestResponse, as_json_p, as_json

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
flaskJson = FlaskJSON(app)
app.url_map.converters['regex'] = RegexConverter


# manager = Manager(app)  # 用manager包装Flask


@app.route('/')
def index():
    # abort(404)
    # request.cookies[''] 读cookie
    response = make_response(render_template('index.html', title='Flask Hello World'))
    response.set_cookie('username', '')
    return response


@app.route('/services')
def services():
    print(request.headers)
    return 'Service'


@app.route('/about')
def about():
    return 'About'


# int float path 路由转换器
@app.route('/user/int=<int:user_id>')
def user(user_id):
    return 'User %s' % user_id


@app.route('/download/client/<regex(".*"):info>')
def regex(info):
    return 'info = %s' % info


@app.route('/download/client/<regex(".+\.tar$"):filename>')
def regex2(filename):
    return 'filename = %s' % filename


# 多个url指向同一个view
@app.route('/projects/')
@app.route('/our-works/')
def projects():
    return 'The project page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # html请求发送时填入的值会自动包装成字典发送到服务端
        # debug=True时会有一个track跟踪页，没有debug=True直接404
        username = request.form['username']
        password = request.form['password']
    else:
        username = request.args['username']
    return render_template('login.html', method=request.method)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath, 'static/uploads')
        f.save(path.join(upload_path, secure_filename(f.filename)))
        # 当上传成功，让url变成GET方法，相当于Post back
        return redirect(url_for('upload'))  # 在flask服务端使用url_for不需要带‘.’
    return render_template('upload.html')


@app.route('/dologin', methods=['POST'])
def dologin():
    print(request.json)
    return json.dumps({"msg": 'post成功'})


@app.route('/news', methods=['GET'])
@as_json_p()
def news():
    # print request.json
    # return json.dumps({"msg": 'post成功'})
    data = ({"msg": 'post成功'})
    return json_response(_data=data, headers_={'X-STATUS': 'ok'})


@app.route('/register', methods=['POST'])
@as_json_p()
def register():
    print(request.json)
    # return json.dumps({"msg": 'post成功'})
    print(request.json.get(u'username'))
    username = request.json.get(u'username')
    passsword = request.json.get(u'password')
    email = request.json.get(u'email')
    res = ({"msg": '用户'})
    import random
    random_num = random.randint(0, 9)
    print("random_num = " + str(random_num))
    if random_num < 5:
        trueOrFalse = True
        msg = "用户注册成功"
    else:
        trueOrFalse = False
        msg = "用户注册失败"
    data = {
        "email": email,
        "id": 6,
        "login_time": None,
        "username": username
    }
    res = {
        "data": data,
        "msg": msg,
        "status": trueOrFalse
    }
    return json_response(_data=res, headers_={'X-STATUS': 'ok'})





@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# # 不需要F5自动刷新
# @manager.command
# def dev():
#     from livereload import Server
#     live_server = Server(app.wsgi_app)
#     live_server.watch('**/*.*')
#     live_server.serve(open_url=True)


if __name__ == '__main__':
    app.run(debug=True)  # 不需要重启服务
    # manager.run()  # 在用ext时要用这个启动
