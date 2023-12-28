import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import pymysql
import os
from dotenv import load_dotenv
from konlpy.tag import Okt
import re

class newsScrap :
    
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
    
    def __init__(self, company):
        self.company = company
        self.titles = []
        self.dates = []
        self.articles = []
        self.article_urls = []
        self.press_companies = []
        self.url_full = []
        
    def createNewsLinks(self):
        start_point = 1
        while True :
            #pd => 4=1일 , 2= 1달
            url = 'https://search.naver.com/search.naver?where=news&query='+ str(self.company) + '&sm=tab_opt&sort=1&photo=0&field=0&pd=4&start=' + str(start_point)
            web = requests.get(url).content
            source = BeautifulSoup(web, 'html.parser')
            
            for urls in source.find_all('a', {'class' : "info"}):
                if urls["href"].startswith("https://n.news.naver.com"):
                    self.article_urls.append(urls["href"])
                    # print(urls["href"])
            is_last_page = source.find('a',{'class':'btn_next'}).get('aria-disabled')
            if is_last_page == "true":
                # print("last page")
                break
            else:
                time.sleep(1)
                start_point += 10
                
                    
    def newsDataScrap(self):
        for url in self.article_urls:
            try:
                web_news = requests.get(url, headers=self.headers).content
                source_news = BeautifulSoup(web_news, 'html.parser')

                title = source_news.find('h2', {'class' : 'media_end_head_headline'}).get_text()

                date = source_news.find('span', {'class' : 'media_end_head_info_datestamp_time'}).get_text()

                article = source_news.find('div', {'id' : 'newsct_article'}).get_text()
                article = article.replace("\n", "")
                article = article.replace("// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}", "")
                article = article.replace("동영상 뉴스       ", "")
                article = article.replace("동영상 뉴스", "")
                article = article.strip()

                press_company = source_news.find('em', {'class':'media_end_linked_more_point'}).get_text()
                
                self.titles.append(title)
                self.dates.append(date)
                self.articles.append(article)
                self.press_companies.append(press_company)
                self.url_full.append(url)
            except:
                pass
            
            
            
    def saveExcel(self):
        article_df = pd.DataFrame({'Title':self.titles, 
                                   'Date':self.dates, 
                                   'Article':self.articles, 
                                   'URL':self.url_full, 
                                   'PressCompany':self.press_companies})
        article_df.to_excel('{}_{}.xlsx'.format(self.company, datetime.now().strftime('%y%m%d_%H%M')), index=False)
        
        
    def dbUpdater(self):
        load_dotenv()

        host=os.getenv("HOST")
        user=os.getenv("USER_NAME")
        password=os.getenv("PASSWORD")
        database=os.getenv("DATABASE")

        cnn = pymysql.connect(host=host, user=user, password=password, database=database)
        
        querys_data = []
        
        cur = cnn.cursor()
        
        selectQuery = 'SELECT enter_id FROM enterprise_data WHERE enter_name = %s'
        
        cur.execute(selectQuery, self.company)
        
        e_id = cur.fetchone()
#         print(self.company)
#         print(type(self.company))
        
        #테이블에 맞춰 항목 추가 예정 
        for i in range(len(self.titles)):
            data = (self.titles[i], self.articles[i], e_id[0], self.url_full[i], self.dates[i])
            querys_data.append(data)
        
        query = 'INSERT INTO news_data(news_id, news_doc, enter_id, url, news_date) VALUES (%s, %s, %s, %s, %s)'
        #query = "INSERT INTO test (name, City) VALUES (%s, %s)"
        
        # for i in querys_data:
        #     cur.execute(query, i)
        
        cur.executemany(query, querys_data)

        cnn.commit()
        cur.close()
        cnn.close()

    def keyWord(self):
        keyword_article = ''.join(self.articles)

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

        sorted_word_dic = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)

        for word, count in sorted_word_dic[:50]:
            print("{0}({1})".format(word, count), end=" ")

    def auto(self):
        self.createNewsLinks()
        self.newsDataScrap()
        self.dbUpdater()

# test = newsScrap('롯데백화점')
# test.createNewsLinks()
# print(test.article_urls)
# print(len(test.article_urls))
# test.newsDataScrap()
# print(test.titles)
# print(len(test.titles))
# print(len(test.url_full))