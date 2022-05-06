import pymysql as psql
import time
import db
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime


# 15초 주기로 크롤링 시작
# -------------------------------1. 웹 페이지 접근
# 웹드라이버 객체 생성
driver = webdriver.Chrome('./webdriver/chromedriver')
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
        CREATE TABLE norang2(
            norang_number int AUTO_INCREMENT,
            norang_name varchar(300),
            norang_tel varchar(300),
            norang_address varchar(300),
            norang_time date,
            PRIMARY KEY(norang_number),
            UNIQUE INDEX(norang_name) 
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

while True:
    now = datetime.now()
    print(now)

    norang_list = []

    for i in range(1, 3):
        # 페이지 접근
        driver.get('http://www.norangtongdak.co.kr/store/store.html?p=%d' % i)
        time.sleep(3)
        html = driver.page_source
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        store_list = soup.select('#new_wrap > div')
        i = 0
        for store in store_list:
            i += 1
            store_name = store.select_one('p.txt1')
            store_tel = store.select_one('li.txt2')
            store_address = store.select_one('li.txt3')
            norang_list.append([store_name.text, store_tel.text, store_address.text])
            # print("{int}. 매장명 : {0} // 매장 전화 번호: {1} // 매장 주소 : {2}".format(store_name.text, store_tel.text, store_address.text, int=i))
    print(norang_list)

    conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
                        charset='utf8',
                        autocommit=True)
    for norang in norang_list:
        data = (norang[0], norang[1], norang[2])
        print(data)
        # cursor 얻어오기
        cursor = conn.cursor()
        #  sql 문장만들기
        sql = """
                    INSERT INTO world.norang2 (norang_name, norang_tel, norang_address, norang_time)
                    VALUE (%s, %s, %s, now())
                    ON DUPLICATE KEY UPDATE norang_time = now()
                """.format()
        # sql 실행(전송)
        cursor.execute(sql, data)
        # cursor 닫기
        cursor.close()
        # 연결 닫기
    conn.close()  # DB 연결 종료
    print("-------------------------------")
    time.sleep(15)


