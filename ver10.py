import pymysql as psql
import time
import db
from selenium import webdriver
from bs4 import BeautifulSoup

# ver10 추출연습

# URL 주소 리스트 생성
contentURL = []
# URL 내용 저장 리스트 생성
contentSaveList = []

# 드라이버 세팅
# conn = psql.connect(host=db.hostLocal, port=3306, user=db.userLocal, password=db.passwordLocal, db=db.dbLocal,
#                     charset='utf8',
#                     autocommit=True)
# try:
#     # cursor 얻어오기
#     cursor = conn.cursor()
#     #  sql 문장만들기
#     sql = """
#                SELECT contentLink FROM contentLink
#                """
#     # sql 실행(전송)
#     cursor.execute(sql)
#     for row in cursor:
#         print('-' * 50)
#         print('{0}'.format(row[0]))
#         contentURL.append(row[0])
#     print('-' * 50)
#     # cursor 닫기
#     cursor.close()
#     # 연결 닫기
#     conn.close()  # DB 연결 종료
#     print(len(contentURL))
# except Exception as e:
#     print(e)

driver = webdriver.Chrome("./webdriver/chromedriver")  # 드라이버 불러오고 옵션값 세팅
driver.maximize_window()  # 화면크기 최대로
driver.implicitly_wait(3)
driver.get('https://www.justwatch.com/kr/TV-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8/was-ipeu-2021')

time.sleep(3)
contentImgLinkList = []
htmlImg = driver.page_source
soupImg = BeautifulSoup(htmlImg, 'html.parser')
contentPosterImgLink = soupImg.select_one('div.title-poster img.picture-comp__img').attrs['src']
contentMainImgLink = soupImg.select_one('div.swiper-slide img.picture-comp__img').attrs['src']
contentImgLinkList.append([contentMainImgLink, contentPosterImgLink])
print(contentImgLinkList)

try:
    elem_pw = driver.find_element_by_class_name('jw-title-clip-poster-play-button')
    elem_pw.click()  # 클릭명령
except Exception as e:
    print(e)

time.sleep(3)
htmlContent = driver.page_source
# print(html)
soup = BeautifulSoup(htmlContent, 'html.parser')
contentSave = soup.select('div.jw-info-box')  # 크롤링할 위치 정함

try:
    for content in contentSave:
        contentTitle = content.select_one('div.title-block h1')  # 제목 저장
        contentTitleReplace = contentTitle.text.strip()
        try:
            contentYoutube = soup.select_one('#youtube-player-1').attrs['src']  # 유튜브 영상 링크
            print(contentYoutube)
        except Exception as e:
            contentYoutube = '유튜브 영상 링크 없음'
            print('{} 영상은 링크가 없음 error : {}'.format(contentTitleReplace, e))
        contentYear = content.select_one('div.title-block span.text-muted')
        contentYearReplace = contentYear.text.replace("(", "").replace(")", "").replace(" ", "")
        contentInfo = content.select_one('p.text-wrap-pre-line')
        contentAge = content.select_one('.title-info>div:nth-child(5)>div:nth-child(2)')
        contentReleaseDate = content.select_one('.title-info>div:nth-child(4)>div:nth-child(2)')
        contentGenre = content.select_one('.title-info>div:nth-child(3)>div:nth-child(2)')
        contentGenreReplace = contentGenre.text.replace(" ", "")
        contentOTTList = []
        for contentOTT in soup.select(
                'div.price-comparison__grid__row--stream .price-comparison__grid__row__holder img'):
            ct = contentOTT['alt']
            contentOTTList.append(ct)
        contentSaveList.append([contentTitleReplace, contentYoutube])
except Exception as e:
    print(e)

print(contentSaveList)
