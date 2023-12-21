# app.py

from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from newsScrap import newsScrap

app = Flask(__name__)

@app.route('/api/crawl', methods=['GET'])
def crawl():
    # 웹 크롤링할 사이트의 URL
    url2 = 'https://google.com'
    
    # requests를 사용하여 웹 페이지 가져오기
    response2 = requests.get(url2)
    
    # BeautifulSoup을 사용하여 HTML 파싱
    soup3 = BeautifulSoup(response2.text, 'html.parser')
    
    # 웹 페이지에서 필요한 정보 추출
    # 예를 들어, 웹 페이지의 제목을 추출하는 경우:
    title7 = soup3.title.text

    test = newsScrap('한전')
    test.createNewsLinks()
    test.newsDataScrap()
    test.dbUpdater()
    
    # 추출한 정보를 JSON 형태로 반환
    return jsonify({'title': title7})

if __name__ == '__main__':
    app.run(debug=True)
