import os
import sys
import click

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager,UserMixin,login_user,

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:
    prifix = 'sqlite:///' # 如果是Windows系统
else:
    prifix = 'sqlite:////' # Mac,Linux

#flask配置：Flask.config字典（写入配置的语句一般会放到扩展类实例化之前）
app.config['SQLALCHEMY_DATABASE_URI'] = prifix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app)

#创建数据库模型类
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True) # 唯一(主键)
    name = db.Column(db.String(20))
    # username = db.Column(db.String(20))  #用户名
    # password_hash = db.Column()

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True) # 唯一(主键)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4)) #年份

#自定义指令
@app.cli.command()
@click.option('--drop',is_flag=True,help='删除之后再创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库')

# 自定义命令forge，把数据写入到数据库
@app.cli.command()
def forge():
    db.create_all()
    name = "李黑皮"
    movies = [
        {'title':'赌圣','year':'2000'},
        {'title':'扫毒','year':'2018'},
        {'title':'囧妈','year':'2020'},
        {'title':'杀破狼','year':'2003'},
        {'title':'捉妖记','year':'2016'},
        {'title':'玻璃盒子','year':'2020'},
        {'title':'调酒师','year':'2020'},
        {'title':'釜山行','year':'2017'},
        {'title':'导火索','year':'2005'},
        {'title':'叶问','year':'2015'},
        {'title':'葫芦娃','year':'1999'}
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('数据导入完成')


# 生成admin账号的函数
# @app.cli.command()
# @click.option('--username',prompt=True,help="用来登录的用户名")
# @click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help="用来登录的密码")
# def admin(username,password):
#     db.create_all()
#     user = User.query.filter()
#     if user is not None:
#         click.echo('更新用户')
#         user.username=username
#         user.set_password(password)
#     else:
#         click.echo('创建用户')
#         user = User(username=username,name='Admin')
#         user.set_password()

# Flask-login初始化操作
# Login_manager = Login_manager(app)  # 实例化扩展类
# @Login_manager.user_loader
# def load_user(user_id):  # 创建用户加载回调函数，接受用户ID作为参数
#     user = User.query.get(int(user_id))
#     return user

# # 设置
# login_manager

#首页
@app.route('/index')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    
    return render_template('index.html',user=user,movies=movies) #render_template渲染html

@app.errorhandler(404) #传入要处理的错误代码
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html',user=user),404

# @app.route('/settings',methods=['POST','GET'])
# @login_required
# def settings():
#     if request.method =='POST':
#         name = request.form['name']

#         if not name or len(name)>20:
#             flash('输入错误')
#             return redirect(url_for('settings'))

#         current_user.name = name
#         db.session.commit()
#         flash('')

# # 用户登录 flask提供的login_user()函数
# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         if not username or not password:
#             flash('输入错误')
#             return redirect(url_for('login'))
#         user = User.query.first()
#         if username == user.username and user.validate_password(password):
#             login_user(user)  # 登录用户
#             flash('登陆成功')
#             return redirect(url_for('index'))  # 登陆成功返回首页
#         flash('用户名或密码错误')
#         return redirect(url_for('login'))
#     return render_template('login.html')

# # 用户登出
# @app.route('/logout')
# def logout():
#     logout_user()
#     flash('退出登录')
#     return redirect(url_for('index'))

