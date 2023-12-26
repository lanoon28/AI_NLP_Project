import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import pymysql
import os
from dotenv import load_dotenv

class newsScrap:
    
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
        
        e_id = cur.fetchall()
#         print(self.company)
#         print(type(self.company))
        
        #테이블에 맞춰 항목 추가 예정 
        for i in range(len(self.titles)):
            data = (self.titles[i], self.articles[i], e_id[0][0], self.url_full[i])
            querys_data.append(data)
        
        query = 'INSERT INTO news_data(news_id, news_doc, enter_id, url) VALUES (%s, %s, %s, %s)'
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
