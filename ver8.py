import pymysql as psql
import time
import db
from selenium import webdriver
from bs4 import BeautifulSoup

# ver8 페이지 자동이동
# URL 주소 리스트 생성
contentURL = []

# 드라이버 세팅
conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
                    charset='utf8',
                    autocommit=True)

try:
    # cursor 얻어오기
    cursor = conn.cursor()
    #  sql 문장만들기
    sql = """
               SELECT contentLink FROM contentLink
               """
    # sql 실행(전송)
    cursor.execute(sql)
    for row in cursor:
        print('-' * 50)
        print('{0}'.format(row[0]))
        contentURL.append(row[0])
    print('-' * 50)
    # cursor 닫기
    cursor.close()
    # 연결 닫기
    conn.close()  # DB 연결 종료
    print(len(contentURL))
except Exception as e:
    print(e)

driver = webdriver.Chrome("./webdriver/chromedriver")  # 드라이버 불러오고 옵션값 세팅
driver.maximize_window()  # 화면크기 최대로
driver.implicitly_wait(3)

# 페이지 이동기
for URL in contentURL:
    # 페이지 접근
    driver.get(URL)
    time.sleep(3)
    html = driver.page_source
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
