from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import pymysql
from flask import jsonify
from esti_config import esti_config, avg_comp_esti
from newsScrap import newsScrap
from konlpy.tag import Okt
from datetime import date, datetime, timedelta
# .env 파일 로드
load_dotenv()

host = os.getenv("HOST")
user = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

app = Flask(__name__)

@app.route('/news/scrap/esti', methods=['GET'])
def esti_eve():
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    comp_names = []
    cur = conn.cursor()
    query = "SELECT enter_name FROM enterprise_data"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    for i in range(len(result)):
        comp_names.append(result[i])
        print(comp_names[i])
    for j in comp_names:
        today_Scrap = newsScrap(j)
        today_Scrap.auto()

    esti_config()
    avg_comp_esti()
    return jsonify(0)

@app.route('/news/scrap/news/comp/<comp_name>', methods=['GET'])
def news_comp(comp_name):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cur = conn.cursor()
    query1 = 'SELECT enter_id FROM enterprise_data WHERE enter_name = %s'
    cur.execute(query1, (comp_name,))
    # 현재 날짜 및 시간을 얻기
    today = datetime.now()
    # 어제의 날짜 계산
    yesterday_time = today - timedelta(days=1)
    yesterday = datetime.date(yesterday_time)
    comp_id = cur.fetchall()
    query2 = "SELECT news_id, news_doc, url FROM news_data WHERE enter_id = %s AND news_date=%s"
    cur.execute(query2, (comp_id[0], yesterday,))
    news_list = cur.fetchall()
    return jsonify(news_list[:5])

@app.route('/news/scrap/esti/comp/<comp_name>', methods=['GET'])
def comp_esti(comp_name):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cur = conn.cursor()
    query = "SELECT avg_esti,devi_yes_avg FROM enterprise_data WHERE enter_name = %s"
    cur.execute(query, (comp_name,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(result[0])

@app.route('/news/scrap/esti/indus/<indus_name>', methods=['GET'])
def indus_esti(indus_name):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cur = conn.cursor()
    query = "SELECT AVG(avg_esti),AVG(devi_yes_avg) FROM enterprise_data WHERE enter_type = %s"
    cur.execute(query, (indus_name,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    esti_result = result[0]
    return jsonify(esti_result)

#급상승 기업
@app.route('/news/hot', methods=['GET'])
def indus_esti(indus_name):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    articles = []
    cur = conn.cursor()
    searchMaxQuery = 'SELECT * FROM enterprise_data WHERE devi_yes_avg = (SELECT MAX(devi_yes_avg) FROM enterprise_data)'
    cur.execute(searchMaxQuery)
    company = list(cur.fetchall()[0])
    hotEId = company[0]  
    findArticlesQuery = 'SELECT news_doc FROM news_data WHERE enter_id = %s'
    cur.execute(findArticlesQuery,hotEId)
    findArticles = cur.fetchall()
        
    for i in range(len(findArticles)):
        articles.append(findArticles[i][0])
        
    key = keyWord(articles)  
    company.append(key)
    cur.close()
    conn.close()

    return jsonify(company[1:])

# 급하락 기업
@app.route('/news/cold', methods=['GET'])
def indus_esti(indus_name):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    articles = []
    cur = conn.cursor()
    searchMaxQuery = 'SELECT * FROM enterprise_data WHERE devi_yes_avg = (SELECT MIN(devi_yes_avg) FROM enterprise_data)'
    cur.execute(searchMaxQuery)
    company = list(cur.fetchall()[0])
    coldEId = company[0]
    findArticlesQuery = 'SELECT news_doc FROM news_data WHERE enter_id = %s'
    cur.execute(findArticlesQuery,coldEId)
    findArticles = cur.fetchall()
        
    for i in range(len(findArticles)):
        articles.append(findArticles[i][0])
        
    key = keyWord(articles)
    company.append(key)
    cur.close()
    conn.close()

    return jsonify(company[1:])

# 급상승,하락 내부에 사용
def keyWord(self,art):
        keyword_article = ''.join(art)

        tokenizer = Okt()
        raw_pos_tagged = tokenizer.pos(keyword_article, norm=True, stem=True)
        del_list = ['하다', '있다', '되다', '이다', '돼다', '않다', '그렇다', '아니다', '이렇다', '그렇다', '어떻다']

        word_cleaned = []
        for word in raw_pos_tagged:
            if not word[1] in ["Josa", "Eomi", "Punctuation", "Foreign"]: # Foreign == ”, “ 와 같이 제외되어야할 항목들
                if (len(word[0]) != 1) and (word[0] not in del_list): # 한 글자로 이뤄진 단어들을 제외 & 원치 않는 단어들을 제외
            # 숫자나 이메일 형식의 단어 제외
                    if not re.match(r'^[0-9]*$', word[0]) and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', word[0]):
                        word_cleaned.append(word[0])

        word_dic = {}

        for word in word_cleaned:
            if word not in word_dic:
                word_dic[word] = 1 # changed from "0" to "1"
            else:
                word_dic[word] += 1

        sorted_word_dic = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)[:5]

        return sorted_word_dic


if __name__ == '__main__':
    app.run(debug=True)