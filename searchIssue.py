import re
import pymysql
import os
from dotenv import load_dotenv
from konlpy.tag import Okt


class searchIssue :
    
    def __init__(self):
        load_dotenv()
        self.host=os.getenv("HOST")
        self.user=os.getenv("USER_NAME")
        self.password=os.getenv("PASSWORD")
        self.database=os.getenv("DATABASE")
    
    def hotEnter(self):
        
        articles = []
        
        cnn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = cnn.cursor()

        searchMaxQuery = 'SELECT * FROM enterprise_data WHERE devi_yes_avg = (SELECT MAX(devi_yes_avg) FROM enterprise_data)'

        cur.execute(searchMaxQuery)
        
        company = list(cur.fetchall()[0])
        
        hotEId = company[0]
        #print(hotEId)
        
        findArticlesQuery = 'SELECT news_doc FROM news_data WHERE enter_id = %s'
        cur.execute(findArticlesQuery,hotEId)
        
        findArticles = cur.fetchall()
        
        for i in range(len(findArticles)):
            articles.append(findArticles[i][0])
        
        key = self.keyWord(articles)
        
        company.append(key)
        
        cur.close()
        cnn.close()
        
        return company[1:]
    
    
    
    def coldEnter(self):
        
        articles = []
        
        cnn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cur = cnn.cursor()

        searchMaxQuery = 'SELECT * FROM enterprise_data WHERE devi_yes_avg = (SELECT MIN(devi_yes_avg) FROM enterprise_data)'

        cur.execute(searchMaxQuery)
        
        company = list(cur.fetchall()[0])
        
        coldEId = company[0]
        #print(hotEId)
        
        findArticlesQuery = 'SELECT news_doc FROM news_data WHERE enter_id = %s'
        cur.execute(findArticlesQuery,coldEId)
        
        findArticles = cur.fetchall()
        
        for i in range(len(findArticles)):
            articles.append(findArticles[i][0])
        
        key = self.keyWord(articles)
        
        company.append(key)
        
        cur.close()
        cnn.close()
        
        return company[1:]
        
        
        
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