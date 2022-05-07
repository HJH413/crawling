import pymysql as psql
import time
import db
from selenium import webdriver
from bs4 import BeautifulSoup

# ver9 CRUD

# 드라이버 세팅
conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
                    charset='utf8',
                    autocommit=True)
# 테이블 생성
try:
    # cusor : 커서 생성
    cursor = conn.cursor()
    # sql문 작성(테이블 생성 sql문 작성)
    sql = """ 
        CREATE TABLE content(
            contentNumber int AUTO_INCREMENT,
            contentTitle varchar(250),
            contentYear varchar(100),
            contentImportDate date,
            PRIMARY KEY(contentNumber),
            UNIQUE INDEX(contentTitle) 
    );
    """
    # sql 실행 명령(테이블 생성)
    cursor.execute(sql)  # cusor 객체의 execute() 메서드를 사용하여 CRUD 문장을 데이터베이스 서버로 보냄
    # 실행 결과 확정 선언
    conn.commit()  # CRUD가 완료되었으면, commit()메서드를 사용하여 데이터를 commit
    # DB연결 해제
    conn.close()
except Exception as e:
    print("{} 테이블 생성되어 있음".format(e))

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
            contentSaveList.append([contentTitle.text.strip(), contentYear2])
    except Exception as e:
        print(e)
# 드라이버 세팅
conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
                    charset='utf8',
                    autocommit=True)
for content in contentSaveList:
    data = (content[0], content[1])
    listData = list(data)
    print(listData)
    cursor = conn.cursor()
    #  sql 문장만들기
    sql = """
                    INSERT INTO content (contentTitle , contentYear, contentImportDate)
                    VALUE (%s, %s, now())
                    ON DUPLICATE KEY UPDATE contentImportDate = now()
                """
    # sql 실행(전송)
    cursor.execute(sql, listData)
    # cursor 닫기
    cursor.close()
    # 연결 닫기
conn.close()  # DB 연결 종료


