from tsa import app, db, inject_user
from tsa.models import Users, Results


@app.route('/')
def hello_tsa():  # put application's code here
    """Return a hello."""
    result = {'code': 200, 'message': 'Teacher-Student-Agents!'}
    return result


@app.route('/users/<int:id>', methods=['GET', 'POST'])
def users(id):
    '''
    获取用户信息
    :param id
    :return 该用户的信息
    '''
    # 如果没有指定ID，返回所有用户内容
    if not id:
        return '请输入该用户的id'
    else:
        user = Users.query.get_or_404(id, '数据库里没有这个用户！')
        return {
            'code': 200,
            'message': '数据查询成功',
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


@app.route('/agents/', methods=['GET','POST'])
def agents():
    # result = Results.query.get_or_404(0, '没查到这个信息！')
    # print(result)
    # return {
    #     'code': 200,
    #     'email': result.email,
    #     'input': result.input,
    #     'result': result.result,
    # }
    return 1