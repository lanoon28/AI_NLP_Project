import pymysql
from dotenv import load_dotenv
import os
import pandas as pd

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
# print(results)

conn.commit()
cur.close()
conn.close()

# df = pd.DataFrame(results)
# df = df.rename(columns={0: 'idx', 1: 'news_id', 2: 'news_doc', 3: 'estimate', 4: 'enter_id', 5: 'url'})
# print(df[:][1])
# print(type(results))
# li_result = list(results[:])
print(results[0])