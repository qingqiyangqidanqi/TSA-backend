from tsa import app, db, inject_user
from tsa.models import Users, Results
from flask import request


@app.route('/')
def hello_tsa():  # put application's code here
    """Return a hello."""
    result = {'code': 200, 'message': 'Teacher-Student-Agents!'}
    return result


@app.route('/users', methods=['POST'])
def users():
    """
    获取用户的账号和密码，然后进行验证登录
    :return 登录失败，返回提示内容；登录成功，则该用户的信息
    """
    content = request.get_json()
    # print(content)  # test
    # 如果没有指定ID，返回所有用户内容
    if not content['email'] or not content['password']:  # 没有输入内容
        return {'code': 200, 'message': '请输入该用户的账号和密码！'}
    else:
        email = content['email']
        password = content['password']
        user = Users.query.filter_by(email=email).first()
        # print(user == None)  # test
        if user is None:
            return {'code': 200, 'message': '该邮箱未注册!'}
        elif not user.validate_password(password):
            return {'code': 200, 'message': '密码错误，请重新输入!'}
        else:  # 成功登录
            return {
                'code': 200,
                'message': '登录成功！！',
                'results': {
                    'id': user.id,
                    'nickName': user.nickName,
                    'openId': user.openId,
                    'email': user.email,
                    'type': user.type,
                    'avatar': user.avatar,
                    'lacalDateTime': user.lacalDateTime,
                    'member': user.member,
                }
            }


@app.route('/agents/', methods=['POST'])
def agents():
    """
    这个用于多agent的内容输入和输出
    :return: agents的输出结果
    """
    content = request.get_json()
    # print(content['input'])  # test
    if content['input'] is None:
        return {'code': 200, 'message': '请和多智能体交流吧~'}
    else:
        result = Results.query.get_or_404(1, '没查到这个信息！')
        return {
            'code': 200,
            'email': result.email,
            'input': result.input,
            'result': result.result,
        }
