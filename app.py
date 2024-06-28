from flask import Flask, request
from flask.views import MethodView
from extension import db, cors
from db_init import Users
import server
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
                    'member': user.member,
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
                    'member': user.member,
                }
            }

    # def post(self):
    #     '''
    #     新增图书
    #     :return:
    #     '''
    #     form = request.json
    #     book = Book()
    #     book.book_number = form.get('book_number')
    #     book.book_name = form.get('book_name')
    #     book.book_type = form.get('book_type')
    #     book.book_prize = form.get('book_prize')
    #     book.author = form.get('author')
    #     book.book_publisher = form.get('book_publisher')
    #     db.session.add(book)
    #     db.session.commit()
    #     return {
    #         'status': 200,
    #         'message': '数据添加成功',
    #     }

    # def delete(self, book_id):
    #     '''
    #     删除单本书
    #     :param book_id:
    #     :return:
    #     '''
    #     book = Book.query.get(book_id)
    #     db.session.delete(book)
    #     db.session.commit()
    #     return {
    #         'status': 'success',
    #         'message': '数据删除成功',
    #     }

    # def put(self, book_id):
    #     '''
    #     数据库更新
    #     :param book_id:
    #     :return:
    #     '''
    #     book: Book = Book.query.get(book_id)
    #     book.book_number = request.json.get('book_number')
    #     book.book_name = request.json.get('book_name')
    #     book.book_type = request.json.get('book_type')
    #     book.book_prize = request.json.get('book_prize')
    #     book.author = request.json.get('author')
    #     book.book_publisher = request.json.get('book_publisher')
    #     db.session.commit()
    #     return {
    #         'status': 'success',
    #         'message': '数据修改成功',
    #     }

class agentsApi(MethodView):
    def get(self):
        # result = server.result()
        sdi = "根据您提供的信息，您的自驱动指数SDI为85%。这意味着您在学业和发展道路上表现出了较高的自我驱动力，能够积极主动地推动自己的学习和发展。请继续保持这种努力和热情，不断探索和学习，为实现自己的目标而努力！"
        evaluation = "'根据您提供的个人自述信息和自驱动指数SDI，我为您评定以下奖项和进行口头鼓舞：', '', '**学生奖项：**', '', '1. **学术成就奖**：基于您在攻读工程管理专业的学习和参与区块链技术研究的深入研究，以及在科研项目和实践活动中展现出的扎实技能和综合能力，您表现出色，值得被认可和奖励。', '  ', '2. **科技创新奖**：由于您对区块链技术在工程管理中的创新应用有着强烈兴趣，并且在实践中不断探索，提出优化建议，这展现出您在科技创新领域具备潜力和能力。', '', '3. **个人成长奖**：您在学习和实践中展现出的成长意味着您正在不断完善自我，不断追求进步和改善，这种积极向上的态度值得鼓励和肯定。', '', '**口头鼓舞：**', '通过您在学术和科研领域的表现，您展现了出色的自我驱动力和坚定的学习意愿，在未来的道路上，您需继续保持热情和努力，不断探索，并将您的热情和知识投入到更广阔的领域中。相信您会成为一个优秀的工程管理专业人才，为社会发展贡献更多的力量。', '', '综合评价拟定奖项为：**学术创新奖**。这个奖项将您在学术和科研方面的努力和潜力充分展现出来，奖励并鼓励您在学术创新领域继续努力，实现更多的突破和成就。', '', '您的自驱力表现优秀，持续努力和专注于目标将带来更多成功和成就。祝您在未来的学业和职业发展道路上一帆风顺！祝您更上一层楼，创造更大的辉煌！'"
        result = {'rate': 0, 'grade': '三等'}
        analysis_and_suggestions = "根据您提供的信息和数据分析结果，我给您一些建议和任务：1. **继续深入研究和创新**：由于您对区块链技术在工程管理中的研究和应用充满热情，建议您继续深入学习和探索这一领域。可以选择更具前沿性和挑战性的课题，尝试将区块链技术与工程管理领域更多方面结合，探索创新的解决方案。2. **参与学术会议和研讨**：老师或同学建议您多参加学术会议和研讨活动，这有助于拓展视野、交流想法，并与同行专家学者进行深入交流。在会议上汲取更多灵感和知识，同时也有机会展示自己的研究成果。3. **发表高水平论文**：为了提升学术影响力和获取更多认可，建议您积极投稿一些顶级学术期刊，将您对区块链技术在工程管理中的研究成果和创新理念分享给更广泛的学术界和社会。这有助于推动领域内的发展和提升个人的学术声誉。4. **继续实践和实习**：您在大型基础设施项目实习中提出优化建议并获得认可，这展现了您的实际操作能力和创新思维。建议您继续参与实践活动，不断积累实战经验，锻炼解决问题的能力，并进一步完善自己的专业技能。5. **目标规划与实施**：您已经表现出对未来发展有明确的规划和目标，建议您继续细化和实施这些目标。制定长期和短期目标，设定明确的里程碑和计划，不断追求进步，努力实现个人职业发展的愿景。希望您能够继续保持对学习和研究的热情，不断努力和探索，将自己的专业能力和兴趣充分发挥，为未来的学业和职业发展打下坚实的基础。祝您学业顺利，未来更上一层楼！"
        # return result,200 if 1 is not None else 404
        return {
            'code': 200,
            'sdi': sdi,
            'evaluation': evaluation,
            'result': result,
            'analysis_and_suggestions': analysis_and_suggestions
        }



user_view = userApi.as_view('user_api')
agents_view = agentsApi.as_view('agents_api')
app.add_url_rule('/users/', defaults={'id': None}, view_func=user_view, methods=['GET'])
app.add_url_rule('/agents/', view_func=agents_view, methods=['GET'])
# app.add_url_rule('/books', view_func=book_view, methods=['POST'])
# app.add_url_rule('/books/<int:book_id>', view_func=book_view, methods=['GET','PUT','DELETE'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
