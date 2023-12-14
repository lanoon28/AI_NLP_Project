import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re
import mysql.connector
import pymysql

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
        #수정 필요
        self.tests = []
        
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
        # 수정 필요
        test = 0
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
                
                
                test += 1
                
                self.tests.append(test)
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
        config = {'user': 'admin_ytk',
                'password': 'tN8VnV1aBuDNvcnPWKgU',
                'host': 'database-ytk.ctkg5u6wqxe6.us-east-2.rds.amazonaws.com',
                'database': 'NLP_G3',
                'raise_on_warnings': True}
        
        cnn = pymysql.connect(host='database-ytk.ctkg5u6wqxe6.us-east-2.rds.amazonaws.com', 
                              user='admin_ytk', password='tN8VnV1aBuDNvcnPWKgU',db='NLP_G3')
        querys_data = []
        
        cur = cnn.cursor()
        
        # 수정 필요 data 첫번째 idx 값 생성방식 고민 및 기업 id
        #테이블에 맞춰 항목 추가 예정 
        for i in range(5):
            data = (self.tests[i], self.titles[i], self.articles[i], self.dates[i], 'ER01', self.article_urls[i])
            querys_data.append(data)
        
        query = 'INSERT INTO news_data VALUES (%s, %s, %s, %s, %s, %s)'
        #query = "INSERT INTO test (name, City) VALUES (%s, %s)"
        
        for i in querys_data:
            cur.execute(query, i)
        
        cnn.commit()
        cur.close()
        cnn.close()

# test = newsScrap('롯데백화점')
# test.createNewsLinks()
# print(test.article_urls)
# print(len(test.article_urls))
# test.newsDataScrap()
# print(test.titles)
# print(len(test.titles))
# print(len(test.url_full))
