import pymysql as psql
import time
import db
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime

# -------------------------------1. 웹 페이지 접근

# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")
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
        CREATE TABLE time_test(
            time_test_number int AUTO_INCREMENT,
            time_test_nation varchar(300),
            time_test_nation_date varchar(300),
            PRIMARY KEY(time_test_number),
            UNIQUE INDEX(time_test_nation) 
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

    time_list = []

    # 페이지 접근
    driver.get('https://vclock.kr/time/')
    time.sleep(3)
    html = driver.page_source
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    nation_list = soup.select('#row-clocks > div')
    try:
        for nation in nation_list:
            time_test_nation = nation.select_one('span.text-ellipsis')
            time_test_nation_date = nation.select_one('div.clock-body > div')
            time_test_nation_date2 = nation.select_one('div.clock-body > div')
            print(time_test_nation.text)
            print(time_test_nation_date.text)
            time_list.append([time_test_nation.text, time_test_nation_date.text, time_test_nation_date2.text])
    except Exception as e:
        print(e)

    conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
                        charset='utf8',
                        autocommit=True)
    for time_nation_list in time_list:
        data = (time_nation_list[0], time_nation_list[1], time_nation_list[2])
        print(data)
        # cursor 얻어오기
        cursor = conn.cursor()
        #  sql 문장만들기
        sql = """
                    INSERT INTO time_test (time_test_nation, time_test_nation_date)
                    VALUE (%s, %s)
                    ON DUPLICATE KEY UPDATE time_test_nation_date = %s
                """
        # sql 실행(전송)
        cursor.execute(sql, data)
        # cursor 닫기
        cursor.close()
        # 연결 닫기
    conn.close()  # DB 연결 종료
    print("-------------------------------")
    time.sleep(5)
