from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import pymysql
from flask import jsonify
from esti_config import esti_config, avg_comp_esti
from newsScrap import newsScrap
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
        today_Scrap.newsDataScrap()
        today_Scrap.dbUpdater()
        today_Scrap.saveExcel()
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
    query = "SELECT avg_esti,(avg_esti-yeste_esti) FROM enterprise_data WHERE enter_name = %s"
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
    query = "SELECT AVG(avg_esti),(AVG(avg_esti)-AVG(yeste_esti)) FROM enterprise_data WHERE enter_type = %s"
    cur.execute(query, (indus_name,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    esti_result = result[0]
    return jsonify(esti_result)


if __name__ == '__main__':
    app.run(debug=True)