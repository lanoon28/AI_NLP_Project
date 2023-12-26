import pymysql
from GB_config import predict_sentiment, PN_Ana, split_sentences
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

def process_and_update_data():
    # .env 파일 로드
    load_dotenv()

    host = os.getenv("HOST")
    user = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE")

    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # 현재 날짜 및 시간을 얻기
    today = datetime.now()

    # 어제의 날짜 계산
    yesterday = today - timedelta(days=1)

    # 어제의 날짜를 00:00:00으로 설정
    yesterday_midnight = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)

    cur = conn.cursor()
    query = "SELECT idx, news_doc FROM news_data WHERE news_date <= %s"
    cur.execute(query, (yesterday_midnight,))
    results = cur.fetchall()

    sentences = []
    idx_num = []

    for i in range(len(results)):
        # results[i]가 튜플인 경우에 문자열로 변환
        text_to_process = str(results[i][1]) if isinstance(results[i][1], tuple) else results[i][1]
        # split_sentences 함수 호출
        a = split_sentences(text_to_process)
        sentences.append(a)
        idx_num.append(results[i][0])

    GB = PN_Ana(sentences)

    for j in range(len(GB)):
        # 파라미터화된 쿼리를 사용하여 값 삽입
        if type(GB[j]) != 'string':
            flo_est_value = float(GB[j])
            rou_flo_est_value = round(flo_est_value, 2)
        query = "UPDATE news_data SET estimate = %s WHERE idx = %s"
        cur.execute(query, (rou_flo_est_value, idx_num[j]))
        conn.commit()

    cur.close()
    conn.close()
    print('종료되었습니다.')

# Call the function
process_and_update_data()
