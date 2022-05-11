import pandas as pd
import db
import csv
import pymysql as psql

df = pd.read_csv('C:/python/content2.csv')
csvRead = open('C:/python/content2.csv', 'r', encoding='utf-8-sig')
csvReader = csv.reader(csvRead)

# 드라이버 세팅
conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
                    charset='utf8',
                    autocommit=True)
cursor = conn.cursor()

print("CSV INSERT")
for row in csvReader:
    contentTitle = (row[0])
    contentYoutube = (row[1])
    contentReleaseDate = (row[2])
    contentInfo = (row[3])
    contentAge = (row[4])
    contentRunningTime = (row[5])
    contentGenre = (row[6])
    contentOTTList = (row[7])
    data = (contentTitle, contentYoutube, contentReleaseDate, contentInfo, contentAge, contentRunningTime, contentGenre, contentOTTList)
    sql =  "INSERT INTO world.content2 (contentTitle, contentYoutube, contentReleaseDate, contentInfo, contentAge, contentRunningTime, contentGenre, contentOTTList, contentImportDay) values(%s,%s,%s,%s,%s,%s,%s,%s,now())"
    cursor.execute(sql, data)
    conn.commit()

conn.close()


