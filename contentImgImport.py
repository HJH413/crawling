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
# URL 이미지 저장 리스트 생성
contentImgLinkList = []

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
        CREATE TABLE contentImgLink(
            contentTitle varchar(250),
            contentImgLinkNumber int AUTO_INCREMENT,
            contentPosterImgLink varchar(2000),
            contentMainImgLink varchar(2000),
            contentImgLinkImportDay date,
            PRIMARY KEY(contentImgLinkNumber),
            FOREIGN KEY (contentTitle) REFERENCES contentLink(contentTitle)
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
        CREATE TABLE world.content(
            contentTitle varchar(250),
            contentNumber int AUTO_INCREMENT,
			contentReleaseDate varchar(250),
            contentInfo varchar(2000),
            contentAge varchar(250),
            contentRunningTime varchar(250),
            contentGenre varchar(2000),
            contentOTTList varchar(2000),
			PRIMARY KEY(contentNumber),
            FOREIGN KEY (contentTitle) REFERENCES contentLink(contentTitle)
    )
    """
    # sql 실행 명령(테이블 생성)
    cursor.execute(sql)  # cusor 객체의 execute() 메서드를 사용하여 CRUD 문장을 데이터베이스 서버로 보냄
    # 실행 결과 확정 선언
    conn.commit()  # CRUD가 완료되었으면, commit()메서드를 사용하여 데이터를 commit
    # DB연결 해제
    conn.close()
except Exception as e:
    print("{} 테이블 생성되어 있음".format(e))

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
imgInsert = 0
for URL in contentURL:
    # 페이지 접근
    driver.get(URL)
    time.sleep(3)
    htmlImg = driver.page_source
    soupImg = BeautifulSoup(htmlImg, 'html.parser')
    contentImgTitle = soupImg.select_one('div.jw-info-box div.title-block h1')  # 제목 저장
    contentImgTitleReplace = contentImgTitle.text.strip()
    contentPosterImgLink = soupImg.select_one('div.title-poster img.picture-comp__img').attrs['src']

    try:
        contentMainImgLink = \
            soupImg.select_one('a.horizontal-title-list__item div.swiper-slide img.picture-comp__img').attrs['src']
    except Exception as e:
        try:
            print(e, '{} 슬라이드 없는 페이지'.format(URL))
            contentMainImgLink = soupImg.select_one('div.backdrop-trailer img.picture-comp__img').attrs['src']
        except Exception as e:
            try:
                contentMainImgLink = soupImg.select_one('div.backdrop-carousel img.picture-comp__img').attrs['src']
                print(e)
            except Exception as e:
                contentMainImgLink = 'none main img'
                print(e)

    print('제목',contentImgTitleReplace)
    print('메인이미지',contentMainImgLink)
    print('포스터이미지',contentPosterImgLink)
    contentImgLinkList.append([contentImgTitleReplace, contentPosterImgLink, contentMainImgLink])
    imgInsert += 1
    print(imgInsert)


for contentImg in contentImgLinkList:
    data = (contentImg[0], contentImg[2], contentImg[1])
    print(data)
    # cursor 얻어오기
    cursor = conn.cursor()
    #  sql 문장만들기
    sql = """
                INSERT INTO contentImgLink (contentTitle , contentMainImgLink, contentPosterImgLink, contentImgLinkImportDay)
                VALUE (%s, %s, %s, now())
                ON DUPLICATE KEY UPDATE contentImgLinkImportDay = now()
            """
    # sql 실행(전송)
    cursor.execute(sql, data)
    # cursor 닫기
    cursor.close()
conn.close()  # DB 연결 종료
