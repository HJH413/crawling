import pymysql as psql
import time
import db
from selenium import webdriver
from bs4 import BeautifulSoup

# ver9 추출연습

# URL 주소 리스트 생성
contentURL = []
# URL 내용 저장 리스트 생성
contentSaveList = []

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

    elem_pw = driver.find_element_by_class_name('jw-title-clip-poster-play-button')
    elem_pw.click() #클릭명령
    time.sleep(3)
    html = driver.page_source
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    contentSave = soup.select('div.jw-info-box')  # 크롤링할 위치 정함


    try:
        for content in contentSave:
            contentTitle = content.select_one('div.title-block h1')  # 제목 저장-
            print(contentTitle.text)
            contentYear1 = content.select_one('div.title-block span.text-muted')
            contentYear2 = contentYear1.text.replace("(", "").replace(")", "").replace(" ", "")
            contentYoutube = soup.select_one('#youtube-player-1').attrs['src']
            print(contentYoutube)
            contentSaveList.append([contentTitle.text.strip(), contentYear2, contentYoutube])
    except Exception as e:
        print(e)


print(contentSaveList)