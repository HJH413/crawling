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

try:
    # 2단계 : connect : mysql 접속
    conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
                        charset='utf8',
                        autocommit=True)
    # 3단계 : cusor : 커서 생성
    cursor = conn.cursor()
    # 4단계 : sql문 작성(테이블 생성 sql문 작성)
    sql = """ 
        CREATE TABLE url_test(
            url_number int AUTO_INCREMENT,
            url_site varchar(1000),
            url_title varchar(250),
            url_Date date,
            PRIMARY KEY(url_number),
            UNIQUE INDEX(url_title) 
    );
    """
    # 5단계 : sql 실행 명령(테이블 생성)
    cursor.execute(sql)  # cusor 객체의 execute() 메서드를 사용하여 CRUD 문장을 데이터베이스 서버로 보냄
    # 6단계 : 실행 결과 확정 선언
    conn.commit()  # CRUD가 완료되었으면, commit()메서드를 사용하여 데이터를 commit
    # 7단계 : DB연결 해제
    conn.close()
except Exception as e:
    print("{} /////////DB존재함".format(e))

url_list = []

# (2안-for문을 사용하여 여러 개를 사용할 경우)
# URL_links = dom.select(".list-type a")
# for i in range(10):
#     print(URL_links[i]['href'])
#
# 페이지 접근
driver.get('https://www.justwatch.com/kr?providers=atp,dnp,flb,nfx')
time.sleep(3)
html = driver.page_source
# print(html)
soup = BeautifulSoup(html, 'html.parser')
url_link = soup.select('div.title-list-grid > div')
try:
    for url in url_link:
        #url_title = url.select_one('span.text-ellipsis')
        url_url = url.select_one('a.title-list-grid__item--link[href]')
        urlaa = url_url.attrs['href']
        urlreal = 'https://www.justwatch.com{}'.format(urlaa)
        #time_test_nation_date2 = url.select_one('div.clock-body > div')
        #print(urlreal)
        # print(url_url.text)
        url_list.append([urlreal])
except Exception as e:
    print(e)
print(url_list)
print(len(url_list))
# conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
#                     charset='utf8',
#                     autocommit=True)
# for time_nation_list in url_list:
#     data = (time_nation_list[0], time_nation_list[1], time_nation_list[2])
#     print(data)
#     # cursor 얻어오기
#     cursor = conn.cursor()
#     #  sql 문장만들기
#     sql = """
#                 INSERT INTO time_test (time_test_nation, time_test_nation_date)
#                 VALUE (%s, %s)
#                 ON DUPLICATE KEY UPDATE time_test_nation_date = %s
#             """
#     # sql 실행(전송)
#     cursor.execute(sql, data)
#     # cursor 닫기
#     cursor.close()
#     # 연결 닫기
# conn.close()  # DB 연결 종료

