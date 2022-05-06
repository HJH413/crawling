import pymysql as psql
import time
import db
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime

# -------------------------------1. 웹 페이지 접근

# 옵션 생성
options = webdriver.ChromeOptions()

options.add_argument('--headless')  # 실행 화면 안 보이게 처리
options.add_argument('--disable-gpu')  # 브라우저의 화면 렌더링 사용 안함

# 웹드라이버 객체 생성
driver = webdriver.Chrome('./webdriver/chromedriver', options=options)
driver.implicitly_wait(3)

url_list = []
# 페이지 접근
driver.get('https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/apple-tv-plus')
time.sleep(3)
html = driver.page_source
# print(html)
soup = BeautifulSoup(html, 'html.parser')
url_link = soup.select('div.title-list-grid > div')
try:
    for url in url_link:
        url_url = url.select_one('a.title-list-grid__item--link[href]')
        urlaa = url_url.attrs['href']
        urlreal = 'https://www.justwatch.com{}'.format(urlaa)
        url_list.append([urlreal])
except Exception as e:
    print(e)
print(url_list)
print(len(url_list))


