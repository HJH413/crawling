import csv

import pymysql as psql
import time
import db
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

filename = 'content.csv'
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)
b = [] # 비어있는 리스트생성
# URL 주소 리스트 생성
contentURL = []
# URL 내용 저장 리스트 생성
contentSaveList = []
# URL 이미지 저장 리스트 생성
contentImgLinkList = []

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
        b.append('0')
    print('-' * 50)
    # cursor 닫기
    cursor.close()
    # 연결 닫기
    conn.close()  # DB 연결 종료
    print(len(contentURL))
    print(len(b))
except Exception as e:
    print(e)

with open('content.csv', 'w', encoding='utf-8-sig') as f:
    writerCSV = csv.writer(f)
    writerCSV.writerows(zip(contentURL, b))
