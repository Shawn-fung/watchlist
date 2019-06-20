from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys


app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控


@app.route('/')
def index():
    #user = User.query.first()  #从数据库读取用户信息
    movies = Movie.query.all()  #从数据库  电影记录
    return render_template('index.html',movies=movies)


'''
自动被调用
使用 app.errorhandler() 装饰器注册一个错误处理函数，它的作用和视图函数类似，当 404 错误发生时，这个函数会被触发，返回值会作为响应主体返回给客户端：
'''
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数

    return render_template('404.html'), 404  # 返回模板和状态码


'''
对于多个模板内都需要使用的变量，我们可以使用 app.context_processor 装饰器注册一个模板上下文处理函数，如下所示：
'''
#自定义模板上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}
'''
这个函数返回的变量（以字典键值对的形式）将会自动统一注入到所有模板的上下文环境中，因此可以直接在模板中使用。
现在我们可以删除 404 错误处理函数和主页视图函数中的 user 变量定义，并删除在 render_template() 函数里传入的关键字参数
'''


# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


import click

#自定义flask命令  向数据库添加数据
@app.cli.command()
def forge():
    #函数名就是命令名
    db.drop_all()
    db.create_all()
    name = 'Feng'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
        {'title':'flask web 开发','year':'2019'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')  #完成后显示消息
