import openai
import numpy as np
import json

# 配置OpenAI API密钥和代理API基本URL
openai.api_key = 'sk-6JrJl37tHNxUlbrWC90578C39433436389921f8275Bf4aF9'
openai.api_base = 'https://openkey.cloud/v1'  # 设置代理服务的API地址

user_input = '''我是一名正在攻读工程管理专业的学生，目前就读于山东大学。在学业方面，我不仅学习了扎实的工程管理理论知识，还对区块链技术在工程管理中的应用进行了深入的研究，特别是其在公共项目资金管理中的应用。

在校期间，我积极参与各类科研项目和课题研究，曾参与“智慧城市建设中的区块链技术应用研究”项目，负责数据分析和技术方案设计工作。通过这次项目，我对区块链技术在提升数据透明度和安全性方面的优势有了更深的认识。

此外，我还注重社会实践，积极参与各种实践活动。例如，我曾在山东省某大型基础设施项目中担任实习生，负责项目资金管理和进度跟踪。在实习过程中，我结合所学理论知识，提出了多项优化建议，获得了项目主管的高度认可。这段实习经历不仅提升了我的实际操作能力，还让我对工程管理有了更全面的理解。

我对工程管理和区块链技术充满热情，希望通过进一步的研究，探索更多区块链技术在工程管理中的创新应用，提升项目管理的透明度和效率，为社会发展贡献自己的力量。'''

teacher_or_peer_suggestion = '建议多参加学术会议和研讨，可以发一些顶刊'

def agent_1(user_input):
    prompt = f"请根据以下个人自述信息分析并计算出自驱动指数SDI，以百分比的形式给出：\n个人自述信息：{user_input}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": '''你是一个教育咨询顾问,分析自述中的学生或者老师，将其分析和
                决策转化为具体的行动，具体包括信息分析执行,其中信息分析执行：利用大模型分析数据，评
                估激励措施的有效性，生成自驱动指数 SDI(Self drive index)，其中自驱动指
                    数 SDI 以百分比值呈现'''},
            {"role": "user", "content": prompt}
        ]
    )
    sdi = response.choices[0].message["content"].strip()
    return sdi

def agent_2(user_input, sdi):
    prompt = f"""
    请根据以下个人自述信息和自驱动指数SDI进行评分，给与老师或者学生进行自驱力奖项和其他奖项拟定以及口头鼓舞，如果是教师给出教师奖项，两到三个，如果是学生，给出学生奖项，两到三个，并综合评价拟定自驱力奖项和其他奖项：
    个人自述信息：{user_input}
    自驱动指数SDI：{sdi}
    根据以下条件进行评分：
    教师奖项：
    1. 教学创新奖
    2. 学生关怀奖
    3. 学术成就奖
    4. 学科领导奖
    5. 团队合作奖
    6. 社区参与奖
    7. 学生推荐奖
    8. 专业发展奖
    9. 学校贡献奖
    10. 家长合作奖
    11. 学生成功奖
    12. 国际视野奖
    13. 创新课程奖
    14. 学生导师奖
    15. 终身学习奖
    16. 优秀班主任奖
    17. 教育影响力奖
    18. 学生评价奖
    19. 教育研究奖
    20. 教师风尚奖
    学生奖项：
    1. 学术成就奖
    2. 艺术才能奖
    3. 体育竞技奖
    4. 领导力奖
    5. 社区服务奖
    6. 科技创新奖
    7. 公民品德奖
    8. 国际理解奖
    9. 环境意识奖
    10. 个人成长奖
    11. 团队合作奖
    12. 学术研究奖
    13. 创意写作奖
    14. 公共演讲奖
    15. 媒体制作奖
    16. 优秀公民奖
    17. 特殊才能奖
    18. 学术挑战奖
    19. 多元文化奖
    20. 持续努力奖
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个教育评审专家，根据收集到的个人自述信息和sdi，给出教师或者是学生奖项，并进行十次综合打分，限制在0-100分。"},
            {"role": "user", "content": prompt}
        ]
    )
    evaluation = response.choices[0].message["content"].strip().split('\n')
    return evaluation

def agent_3(sdi, scores):
    scores = [int(score.split(':')[1]) for score in scores if ':' in score and '评分' in score]
    scores = sorted(scores)

    ai = [score for score in scores if score <= 50]
    bi = [score for score in scores if 51 <= score <= 80]
    ci = [score for score in scores if score >= 81]

    if len(ai) < 3:
        rate1 = np.mean(ai) if ai else 0
    else:
        rate1 = np.mean(ai[1:-1])

    if len(bi) < 3:
        rate2 = np.mean(bi) if bi else 0
    else:
        rate2 = np.mean(bi[1:-1])

    if len(ci) < 3:
        rate3 = np.mean(ci) if ci else 0
    else:
        rate3 = np.mean(ci[1:-1])

    m1, m2, m3 = 0.3, 0.3, 0.4  # Example weights
    rate = 1 / ((m1 + m2 + m3) * (m1 / rate1 + m2 / rate2 + m3 / rate3)) if (
                rate1 != 0 and rate2 != 0 and rate3 != 0) else 0

    if 0 <= rate < 50:
        grade = "三等"
    elif 51 <= rate < 80:
        grade = "二等"
    elif 81 <= rate <= 100:
        grade = "一等"

    result = {"rate": rate, "grade": grade}
    return result

def agent_4(user_input, sdi, evaluation, result, suggestion):
    prompt = f"""
    请根据以下反馈数据、自驱动指数SDI、评分结果、个人自述信息以及老师或同学的建议，生成个性化的改进建议和任务：
    个人自述信息：{user_input}
    自驱动指数SDI：{sdi}
    评分结果：{evaluation}
    综合评价结果：{result}
    老师或同学的建议：{suggestion}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个教育评审专家，基于数据分析的结果，为教师和学生提供量身定制的改进措施和建议。"},
            {"role": "user", "content": prompt}
        ]
    )
    analysis_and_suggestions = response.choices[0].message["content"].strip()
    return analysis_and_suggestions


if __name__ == '__main__':
    sdi = agent_1(user_input)
    evaluation = agent_2(user_input, sdi)
    result = agent_3(sdi, evaluation)
    analysis_and_suggestions = agent_4(user_input, sdi, evaluation, result, teacher_or_peer_suggestion)

    # 打印所有结果
    print(f"SDI: {sdi}")
    print("************************************************")
    print(f"Evaluation: {evaluation}")
    print("************************************************")
    print(f"Result: {result}")
    print("************************************************")
    print(f"Analysis and Suggestions: {analysis_and_suggestions}")
