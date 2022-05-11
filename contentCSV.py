import csv
import requests
import pymysql as psql
import time

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

with open('content.csv', 'r', encoding='utf-8-sig') as f:
    readCSV = csv.reader(f)

    contentSaveList = []
    for rCSV in readCSV:
        html = requests.get(rCSV[0])
        soup = BeautifulSoup(html.text, 'html.parser')
        contentSave = soup.select('div.jw-info-box')  # 크롤링할 위치 정함

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

print(contentSaveList)


with open('content1.csv', 'w', encoding='utf-8-sig') as ff:
    z= csv.writer(ff)
    z.writerows(contentSaveList)
