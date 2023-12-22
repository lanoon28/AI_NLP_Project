import pymysql
# import newScrap
from GB_config import predict_sentiment, PN_Ana, split_sentences
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from dotenv import load_dotenv
import os
import time

# .env 파일 로드
load_dotenv()

host=os.getenv("HOST")
user=os.getenv("USER_NAME")
password=os.getenv("PASSWORD")
database=os.getenv("DATABASE")

conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur = conn.cursor()
cur.execute("SELECT idx, news_doc FROM news_data")
results = cur.fetchall()


sentences = []
idx_num = []
# print(len(results))
# print(results)
for i in range(len(results)):
    # results[i]가 튜플인 경우에 문자열로 변환
    text_to_process = str(results[i][1]) if isinstance(results[i][1], tuple) else results[i][1]
    # split_sentences 함수 호출
    a = split_sentences(text_to_process)
    # print(f'{i+1}번째 문장. {a}')
    # for j in a:
    #     print(j)
    sentences.append(a)
    idx_num.append(results[i][0])

# a = 1
# for b in sentences:
#     print()
#     print(f'{a}번째 기사')
#     a = a + 1
#     for c in b:
#         print()
#         print(c)

# print(f'sentence:{sentences[:5]}')
# test = list(sentences[1])
# for j in range(len(test)):
#     print(test[j])
GB = PN_Ana(sentences)
# print(GB)
# print(len(GB))

for j in range(len(GB)):
    # 파라미터화된 쿼리를 사용하여 값 삽입
    if type(GB[j]) != 'string':
        flo_est_value = float(GB[j])
        rou_flo_est_value = round(flo_est_value,2)
    query = "UPDATE news_data SET estimate = %s WHERE idx = %s"
    cur.execute(query, (rou_flo_est_value, idx_num[j]))
    conn.commit()

cur.close()
conn.close()
print('종료되었습니다.')
# print(GB)