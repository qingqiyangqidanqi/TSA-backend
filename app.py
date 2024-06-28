from flask import Flask, request
from flask.views import MethodView
from extension import db, cors
from db_init import Users
import os

# 获取当前文件所在的目录路径
current_dir = os.path.dirname(os.path.realpath(__file__))
# 构建数据库文件的完整路径
db_file_path = os.path.join(current_dir, "users.sqlite")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_path}'  # 配置SQLAlchemy数据库URI为当前目录下的 "book.sqlite" 文件
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁止sqlalchemy进行追踪
db.init_app(app)
cors.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    result={'code': 200, 'message': 'hello world!'}
    return result


@app.cli.command()  # 自定义指令
def create():
    '''
    终端输入flask create即可初始化数据库
    :return:
    '''
    db.drop_all()  # 把旧的数据表全部删除
    db.create_all()  # 创建一个新的数据表
    Users.init_db()  # 初始化数据


class userApi(MethodView):
    def get(self, id):
        '''
        获取图书信息
        :param book_id:
        :return:
        '''
        # 如果没有指定ID，返回所有用户内容
        if not id:
            users: [Users] = Users.query.all()  # 类型注释，表示books是一个列表，列表中的元素都是Book元素
            results = [
                {
                    'id': user.id,
                    'nickName': user.nickName,
                    'openId': user.openId,
                    'email': user.email,
                    'type': user.type,
                    'avatar': user.avatar,
                    'lacalDateTime': user.lacalDateTime,
                } for user in users
            ]  # 列表推导式
            return {
                'code': 200,
                'message': '数据查询成功',
                'results': results
            }
        # 指定了ID，返回单用户
        else:
            user: Users = Users.query.get(id)
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
                }
            }

    def post(self):
        '''
        新增图书
        :return:
        '''
        form = request.json
        book = Book()
        book.book_number = form.get('book_number')
        book.book_name = form.get('book_name')
        book.book_type = form.get('book_type')
        book.book_prize = form.get('book_prize')
        book.author = form.get('author')
        book.book_publisher = form.get('book_publisher')
        db.session.add(book)
        db.session.commit()
        return {
            'status': 200,
            'message': '数据添加成功',
        }

    def delete(self, book_id):
        '''
        删除单本书
        :param book_id:
        :return:
        '''
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据删除成功',
        }

    def put(self, book_id):
        '''
        数据库更新
        :param book_id:
        :return:
        '''
        book: Book = Book.query.get(book_id)
        book.book_number = request.json.get('book_number')
        book.book_name = request.json.get('book_name')
        book.book_type = request.json.get('book_type')
        book.book_prize = request.json.get('book_prize')
        book.author = request.json.get('author')
        book.book_publisher = request.json.get('book_publisher')
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功',
        }

class agentsApi(MethodView):
    def get(self):
        return "This is a answer for agents.",200 if 1 is not None else 404

user_view = userApi.as_view('user_api')
agents_view = agentsApi.as_view('agents_api')
app.add_url_rule('/users/', defaults={'id': None}, view_func=user_view, methods=['GET'])
app.add_url_rule('/agents/', view_func=agents_view, methods=['GET'])
# app.add_url_rule('/books', view_func=book_view, methods=['POST'])
# app.add_url_rule('/books/<int:book_id>', view_func=book_view, methods=['GET','PUT','DELETE'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
