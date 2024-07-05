import click

from tsa import app, db
from tsa.models import Users, Results


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """
    终端执行 flask initdb 命令就可以创建数据库表
    终端执行 flask initdb --drop 命令可以删除表后重新创建
    """
    if drop:  # 判断是否输入了选项
        db.drop_all()  # 删除数据库
    db.create_all()  # 创建数据库
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()
def forge():
    """Init database for some test data."""
    db.create_all()

    users = [
        {'nickName': 'test', 'openId': '123', 'email': '123@123.com', 'type': 'USER',
         'avatar': 'https://p.qqan.com/up/2020-12/16070652276806379.jpg', 'member': 1, 'password': 'dog'},
        {'nickName': 'test', 'openId': '321', 'email': '321@321.com', 'type': 'USER',
         'avatar': 'https://p.qqan.com/up/2020-12/16070652276806379.jpg', 'member': 2, 'password': 'dog'},
        {'nickName': 'jason', 'openId': '111', 'email': '1030072717@163.com', 'type': 'ADMIN',
         'avatar': 'https://p.qqan.com/up/2020-12/16070652276806379.jpg', 'member': 3, 'password': '23020090092'},
        {'nickName': 'likeke', 'openId': '222', 'email': '2422014722@qq.com', 'type': 'ADMIN',
         'avatar': 'https://p.qqan.com/up/2020-12/16070652276806379.jpg', 'member': 4, 'password': '23020090095'},
    ]
    results = [
        {'email': '123@123.com',
         'input': '我是一名正在攻读工程管理专业的学生，目前就读于山东大学。',
         'result': '根据您提供的信息，您的自驱动指数SDI为85%。这意味着您在学业和发展道路上表现出了较高的自我驱动力，能够积极主动地推动自己的学习和发展。请继续保持这种努力和热情，不断探索和学习，为实现自己的目标而努力！'},
    ]
    for u in users:
        user = Users(nickName=u['nickName'], openId=u['openId'], email=u['email'], type=u['type'],
                     avatar=u['avatar'], member=u['member'])
        user.set_password(password=u['password'])
        db.session.add(user)
    for r in results:
        result = Results(email=r['email'], input=r['input'], result=r['result'])
        db.session.add(result)
    db.session.commit()
    click.echo('Done.')
