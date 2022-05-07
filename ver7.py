import pymysql as psql
import time
import db
from selenium import webdriver
from bs4 import BeautifulSoup


# ver7 db저장한 url 리스트로 저장
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
    print(contentURL)
except Exception as e:
    print(e)


