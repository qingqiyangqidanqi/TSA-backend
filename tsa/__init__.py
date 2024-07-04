import sys
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),
                                                              os.getenv('DATABASE_FILE', './tas-backend.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')  # 等同于 app.secret_key = 'dev'

# 实例化
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # login_manager.login_view 的值设为我们程序的登录视图端点（函数名）
cors = CORS(app)


@login_manager.user_loader
def load_user(user_id):
    """创建用户加载回调函数，接受用户 ID 作为参数"""
    from tsa.models import Users
    user = Users.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


@app.context_processor
def inject_user():  # 函数名可以随意修改
    """对于多个模板内都需要使用的变量，我们可以使用 app.context_processor 装饰器注册一个模板上下文处理函数"""
    from tsa.models import Users
    user = Users.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


from tsa import views, errors, commands
