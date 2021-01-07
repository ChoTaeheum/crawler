import urllib.request            # 웹브라우저에서 html문서를 얻어오기 위한 모듈
from bs4 import BeautifulSoup    # html문서 검색 모듈
import os
from selenium import webdriver   # 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
from selenium.webdriver.common.keys import Keys
import time

filename = input('저장할 파일이름을 입력하세요(예, 인공지능) ')
keyword = input('검색어를 입력하세요 ')

chrome = 'c:\\data\\chromedriver.exe'
browser = webdriver.Chrome(chrome)  # 웹브라우저 인스턴스화

browser.get('http://news.donga.com/search?query=&x=0&y=0')
# 이미지를 검색할 웹사이트의 주소 입력(이미지만 검색하는 창을 추천한다.)  # 1

elem1 = browser.find_element_by_id('query')  # 2
elem2 = browser.find_element_by_class_name('s')      # 3


time.sleep(1)

##################################검색어 입력###################################
elem1.send_keys(keyword)  # 검색어 입력(검색어 입력창과 연결)
time.sleep(1)
elem2.click()
# elem1.submit()
elem3 = browser.find_element_by_class_name('more02')
elem3.click()

def get_save_path():
    save_path = 'C:\\data\\동아일보Text\\{}.txt'.format(filename)    # 4

    if not os.path.isdir(os.path.split(save_path)[0]):
        os.mkdir(os.path.split(save_path)[0])           # 지정된 경로에 파일이 없으면 만들어라
    return save_path


def fetch_list_url():
    params = []

    # for cnt in range(1, 5):

    browser.find_element_by_xpath("//body")       # 페이지 활성화
    html = browser.page_source                    # 현재 페이지 소스 담기 즉 1페이지
    soup = BeautifulSoup(html, "lxml")
    for i in soup.find_all('p', class_='tit'):
        params.append(i('a')[0]['href'])          # find_all은 리스트로 담아준다. 그래서[0]이 필요

    list_url = soup.find_all('div', class_='page')[0]('a')[0]['href']
    # print('\n', list_url)

    for i in range(9):

        list_url = 'http://news.donga.com/search' + soup.find_all('div', class_='page')[0]('a')[i]['href']

        print('\n', list_url)
        url = urllib.request.Request(list_url)
        res = urllib.request.urlopen(url).read().decode('utf-8')

        soup2 = BeautifulSoup(res, 'html.parser')     # res html문서를 BeautifulSoup모듈을 사용해서 검색하도록 설정

        for i in soup2.find_all('p', class_='tit'):
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

        article = soup('div', class_='article_txt')[0].get_text(strip=True, separator='\n')
        # loop돌면서 기사가 계속 바뀐다.
        f.write(article + '\n'*2 + '='.ljust(50, '=') + '\n')  # 기사 바뀌면서 계속 적어라!

    f.close()

fetch_list_url2()