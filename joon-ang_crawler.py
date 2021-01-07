import urllib.request            # 웹브라우저에서 html문서를 얻어오기 위한 모듈
from bs4 import BeautifulSoup    # html문서 검색 모듈
import os
from selenium import webdriver   # 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
from selenium.webdriver.common.keys import Keys
import time


filename = input('파일 이름을 입력하세요 ')

keyword = input('검색어를 입력하세요 ')

chrome = 'c:\\data\\chromedriver.exe'
browser = webdriver.Chrome(chrome)  # 웹브라우저 인스턴스화

browser.get('http://search.joins.com/JoongangNews?Keyword&SortType=New&SearchCategoryType=JoongangNews&PeriodType=All&ScopeType=All&ImageType=All&JplusType=All&BlogType=All&ImageSearchType=Image&TotalCount=0&StartCount=0&IsChosung=False&IssueCategoryType=All&IsDuplicate=True&Page=1&PageSize=10&IsNeedTotalCount=True')
# 이미지를 검색할 웹사이트의 주소 입력(이미지만 검색하는 창을 추천한다.)

elem1 = browser.find_element_by_id('searchKeyword')
elem2 = browser.find_element_by_id('btnSearch')

time.sleep(1)

##################################검색어 입력###################################
elem1.send_keys(keyword)  # 검색어 입력(검색어 입력창과 연결)
elem2.click()             # 엔터키 입력인데 왜 안쳐짐?


def get_save_path():
    save_path = 'C:\\data\\중앙일보Text\\{}.txt'.format(filename)
    # save_path = save_path.replace("\\", "/") 필요 없을 것 같은데???

    if not os.path.isdir(os.path.split(save_path)[0]):
        os.mkdir(os.path.split(save_path)[0])           # 지정된 경로에 파일이 없으면 만들어라
    return save_path


##############################각 페이지 주소 가져오기#############################
def fetch_list_url():
    params = []

    # for cnt in range(1, 5):

    browser.find_element_by_xpath("//body")       # 페이지 활성화
    html = browser.page_source                    # 현재 페이지 소스 담기
    soup = BeautifulSoup(html, "lxml")
    for i in soup.find_all('strong', class_='headline mg'):
        params.append(i('a')[0]['href'])          # find_all은 리스트로 담아준다. 그래서[0]이 필요


    for i in range(9):
        list_url = 'http://search.joins.com' + soup.find_all('a', class_='link_page')[i]['href']
        # print(list_url)
        url = urllib.request.Request(list_url)
        res = urllib.request.urlopen(url).read().decode('utf-8')

        soup2 = BeautifulSoup(res, 'html.parser')     # res html문서를 BeautifulSoup모듈을 사용해서 검색하도록 설정

        for i in soup2.find_all('strong', class_='headline mg'):
            params.append(i('a')[0]['href'])
    # print(params)   # 페이지 내의 뉴스 웹주소 다 담긴다.
    browser.quit()
    return params


def fetch_list_url2():
    params2 = fetch_list_url()
    f = open(get_save_path(), 'w', encoding='utf-8')    # get_save_path()를 인스턴스화!!

    for i in params2:
        list_url = "{}".format(i)

        url = urllib.request.Request(list_url)
        res = urllib.request.urlopen(url).read().decode('utf-8')

        soup = BeautifulSoup(res, "html.parser")  # res html문서를 BeautifulSoup모듈을 사용해서 검색하도록 설정
        # print(soup('div', id='article_body')[0].get_text(strip=True, separator='\n'))
        article = soup('div', id='article_body')[0].get_text(strip=True, separator='\n')
        # loop돌면서 기사가 계속 바뀐다.
        f.write(article + '\n'*2 + '='.ljust(50, '=') + '\n')  # 기사 바뀌면서 계속 적어라!

    f.close()

fetch_list_url2()