import pymysql
from GB_config import predict_sentiment, PN_Ana, split_sentences
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import os

def esti_config():
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
    yesterday_time = today - timedelta(days=1)
    yesterday = datetime.date(yesterday_time)

    cur = conn.cursor()
    query = "SELECT idx, news_doc FROM news_data WHERE news_date = %s"
    cur.execute(query, (yesterday,))
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
    print('긍정부정 평가가 종료되었습니다.')

def avg_comp_esti():
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
    cur = conn.cursor()
    query = "SELECT enter_id FROM enterprise_data"
    cur.execute(query)
    comp_idx = cur.fetchall()
    # print(comp_idx[0][0])
    
    for i in range(len(comp_idx)):
        comp_id = comp_idx[i][0]
        # print(comp_id)
        # query_name = "SELECT enter_id FROM enterprise_data WHERE enter_name = %s"
        # cur.execute(query_name, (comp_id[0],))
        # comp_num = cur.fetchall()
        # print(comp_num)
        query_num = "SELECT AVG(estimate) FROM news_data WHERE enter_id = %s"
        cur.execute(query_num, (comp_id,))
        avg_esti_com = cur.fetchall()
        print(f'({comp_id})의 긍정부정 평균 : {avg_esti_com[0][0]}')
        query_yest = "UPDATE enterprise_data SET yeste_esti = avg_esti WHERE enter_id = %s"
        cur.execute(query_yest, (comp_id,))
        query_avg = "UPDATE enterprise_data SET avg_esti = %s WHERE enter_id = %s"
        cur.execute(query_avg,(avg_esti_com, comp_id,))
        conn.commit()
    
    cur.close()
    conn.close()
    print('평균 평가 등록이 완료되었습니다.')

# Call the function
# esti_config()
# avg_comp_esti()
