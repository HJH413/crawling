import pymysql as psql
import time
import db
from selenium import webdriver
from bs4 import BeautifulSoup

# ver6에서 url 목록저장
# 1. mysql db 접속해서 테이블 생성 및 테이블 존재여부 확인 후 db연결 종료
# 2. 자동스크롤을 해서 페이지 전체를 로딩하고 크롤링을 통해서 URL 전체 주소 및 주소의 제목을 가져옴


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
        CREATE TABLE contentLink(
            contentLinkNumber int AUTO_INCREMENT,
            contentLink varchar(1000),
            contentTitle varchar(250),
            contentLinkImportDay date,
            PRIMARY KEY(contentTitle),
            UNIQUE INDEX(contentLinkNumber) 
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

options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 실행 화면 안 보이게 처리
# options.add_argument('--disable-gpu')  # 브라우저의 화면 렌더링 사용 안함

driver = webdriver.Chrome("./webdriver/chromedriver", options=options)  # 드라이버 불러오고 옵션값 세팅
driver.maximize_window()  # 화면크기 최대로

url = 'https://www.justwatch.com/kr?providers=atp,dnp,nfx'  # URL
driver.get(url)  # URL 적용

prev_height = driver.execute_script("return document.body.scrollHeight")  # 스크롤링 시작

# 웹페이지 맨 아래까지 무한 스크롤
while True:
    # 스크롤을 화면 가장 아래로 내린다
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # 페이지 로딩 대기
    time.sleep(2)

    # 현재 문서 높이를 가져와서 저장
    curr_height = driver.execute_script("return document.body.scrollHeight")

    urlList = []  # URL 리스트 생성

    if curr_height == prev_height:
        time.sleep(3)  # 3초대기
        html = driver.page_source  # 페이지 소스 가져오기
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')  # parser 하기
        urlMainTag = soup.select('div.title-list-grid > div')  # 크롤링할 위치 정함
        try:
            for urlTag in urlMainTag:
                urlLink = urlTag.select_one('a.title-list-grid__item--link').attrs['href']  # 링크 추출
                urlSetLink1 = 'https://www.justwatch.com{}'.format(urlLink)  # 정상적인 링크로 생성
                urlSetLink2 = 'https://www.justwatch.com{}'.format(urlLink)
                urlTitle = urlTag.select_one('img.picture-comp__img').attrs['alt']  # 링크에 해당하는 제목 추출
                print(urlSetLink1)
                print(urlTitle)
                urlList.append([urlSetLink1, urlTitle, urlSetLink2])
        except Exception as e:
            print(e)
        print(len(urlList))
        for content in urlList:
            data = (content[0], content[1], content[2])
            print(data)
            # cursor 얻어오기
            cursor = conn.cursor()
            #  sql 문장만들기
            sql = """
                        INSERT INTO contentLink (contentLink , contentTitle, contentLinkImportDay)
                        VALUE (%s, %s, now())
                        ON DUPLICATE KEY UPDATE contentLink = %s, contentLinkImportDay = now()
                    """
            # sql 실행(전송)
            cursor.execute(sql, data)
            # cursor 닫기
            cursor.close()
            # 연결 닫기
        conn.close()  # DB 연결 종료
        break
    else:
        prev_height = driver.execute_script("return document.body.scrollHeight")
