from flask import Flask,render_template,request,url_for,flash,redirect
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
app.config['SECRET_KEY'] = '12312asdfsdfsadf'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)



@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录




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
#数据模型类
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份




'''
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,IntegerField
from wtforms.validators import DataRequired,Length
#表单类
class HelloForm(FlaskForm):
    movie = StringField('book',validators=[DataRequired(),Length(1,10)])
    year = IntegerField('year',validators=[DataRequired()])
    submit = SubmitField()
    

<form  class="inline-form" method="POST">
{{ form.csrf_token() }}
{{ form.movie.label }}{{ form.movie }}<br>
{{ form.year.label }}{{ form.year }}<br>
<div class="btn">{{ form.submit }}<br></div>
{% for message in get_flashed_messages() %}
        <div class="alert">{{ message }}</div>
{% endfor %}

</form>


'''
'''form = HelloForm()
    if form.validate_on_submit():
        new_movie = form.movie.data
        new_year = form.year.data
        movie = Movie.query.filter_by(title=new_movie).first()
        if movie:
            flash('movie was looked')
        else:
            try:
                new_list = Movie(title=new_movie,year=new_year)
                db.session.add(new_list)
                db.session.commit()
            except Exception as e:
                print(e)
                flash('error111111111111111111')
                db.session.rollback()

    '''



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
