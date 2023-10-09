import os
from flask import Flask, render_template, request
import json
import logging
from zhdate import ZhDate
import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()

app = Flask(__name__)

today_yinli = ZhDate.today()
today_yangli = datetime.datetime.today().strftime('%Y年%m月%d日')

@app.route('/')
def home():
    return render_template('index.html',
                           today_nongli=today_yinli, today_yangli=today_yangli)


@app.route('/result', methods=['POST'])
def result():
    # 获取用户输入
    user_problem = request.form.get('user_problem')
    logger.info(f'用户查询：{user_problem}')

    # 检测用户输入术语是否为空值
    if user_problem is None or user_problem.strip() == "":
        return '无法搜索，请确认输入是否有误'

    # 检测用户输入术语是否在术语集中
    with open('./data/term.csv', 'r', newline='', encoding='utf-8') as term_file:
        term_reader = term_file.read()
        if user_problem not in term_reader:
            return render_template('error.html')


    # 新建 ["宜","忌"] 两个列表存储信息
    user_problem_yi = []
    user_problem_ji = []

    # 根据用户输入对应查询信息
    jsonl_files = os.listdir('./data')
    for jsonl_file in jsonl_files:
        if jsonl_file.endswith('.jsonl'):
            with open(f'./data/{jsonl_file}', 'r', newline='', encoding='utf-8') as file:
                for line in file:
                    json_data = json.loads(line)
                    if user_problem in json_data['result']['yi']:
                        user_problem_yi.append(f'{json_data["result"]["nongli"]}')
                    elif user_problem in json_data['result']['ji']:
                        user_problem_ji.append(f'{json_data["result"]["nongli"]}')

            result_yi = f'{user_problem_yi}'
            result_ji = f'{user_problem_ji}'

            return render_template('result.html',
                                   user_problem=user_problem,
                                   today_nongli=today_yinli, today_yangli=today_yangli,
                                   result_yi=result_yi, result_ji=result_ji)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=9991)