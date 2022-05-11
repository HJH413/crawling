import csv

import pymysql as psql
import time
import db
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

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
        CREATE TABLE content(
            contentNumber int AUTO_INCREMENT,
            contentTitle varchar(250),
            contentYoutube varchar(2000),
			contentReleaseDate varchar(250),
            contentInfo varchar(2000),
            contentAge varchar(250),
            contentRunningTime varchar(250),
            contentGenre varchar(2000),
            contentOTTList varchar(2000),
            contentImportDay Date,
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
