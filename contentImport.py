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
    print('-' * 50)
    # cursor 닫기
    cursor.close()
    # 연결 닫기
    conn.close()  # DB 연결 종료
    print(len(contentURL))
except Exception as e:
    print(e)

# 드라이버 세팅
conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
                    charset='utf8',
                    autocommit=True)

driver = webdriver.Chrome("./webdriver/chromedriver")  # 드라이버 불러오고 옵션값 세팅
driver.maximize_window()  # 화면크기 최대로
driver.implicitly_wait(3)

# 페이지 이동기
contentInsert = 0
for URL in contentURL:
    # 페이지 접근
    driver.get(URL)
    time.sleep(3)
    contentInsert += 1
    try:
        elem_pw = driver.find_element_by_class_name('jw-title-clip-poster-play-button')
        elem_pw.click()  # 클릭명령
    except Exception as e:
        print('유튜브 영상 없음', e)
    html = driver.page_source
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    contentSave = soup.select('div.jw-info-box')  # 크롤링할 위치 정함
    print(contentInsert)
    try:
        for content in contentSave:
            contentTitle = content.select_one('div.title-block h1')  # 제목 저장
            contentTitleReplace = contentTitle.text.strip()
            try:
                contentYoutube = soup.select_one('#youtube-player-1').attrs['src']  # 유튜브 영상 링크
            except Exception as e:
                contentYoutube = 'YouTube No'
                print('{} --- 유튜브 동영상 링크가 없음 error : {}'.format(contentTitleReplace, e))
            contentReleaseDate = content.select_one('div.title-block span.text-muted')
            contentReleaseDateReplace = contentReleaseDate.text.replace("(", "").replace(")", "").replace(" ", "")
            contentInfo = content.select_one('p.text-wrap-pre-line')
            contentAge = content.select_one('.title-info>div:nth-child(5)>div:nth-child(2)')
            contentRunningTime = content.select_one('.title-info>div:nth-child(4)>div:nth-child(2)')
            contentGenre = content.select_one('.title-info>div:nth-child(3)>div:nth-child(2)')
            contentGenreReplace = contentGenre.text.replace(" ", "")
            contentOTTList = []
            for contentOTT in soup.select(
                    'div.price-comparison__grid__row--stream .price-comparison__grid__row__holder img'):
                ct = contentOTT['alt']
                contentOTTList.append(ct)
            print("진행 중 인 영상 {}".format(contentTitleReplace))
            contentSaveList.append(
                [contentTitleReplace, contentYoutube, contentReleaseDateReplace, contentInfo.text, contentAge.text,
                 contentRunningTime.text, contentGenreReplace, contentOTTList])

    except Exception as e:
        print(e)

data = pd.DataFrame(contentSaveList)
data.to_csv('content.csv', encoding='euc-kr')



for contentList in contentSaveList:
    data = (
    contentList[0], contentList[1], contentList[2], contentList[3], contentList[4], contentList[5], contentList[6],
    contentList[7])
    print(data)
    # cursor 얻어오기
    cursor = conn.cursor()
    #  sql 문장만들기
    sql = """
                INSERT INTO content (contentTitle, contentYoutube, contentReleaseDate, contentInfo, contentAge, contentRunningTime, contentGenre, contentOTTList, contentImportDay)
                VALUE (%s, %s, %s, %s, %s, %s, %s, %s, now());
            """
    # sql 실행(전송)
    cursor.execute(sql, data)
    # cursor 닫기
    cursor.close()

conn.close()  # DB 연결 종료
