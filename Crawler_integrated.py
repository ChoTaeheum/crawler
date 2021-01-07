import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver   # 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
from selenium.webdriver.common.keys import Keys
import time    # sleep하기 위한 모듈
import os
import lxml


#######################################################################################
#######################################################################################

def input_order():
    print('본 수집기 이용에는 크롬 드라이버가 필요합니다. {c:\\data\\chromedriver.exe} 경로에 크롬드라이버를 설치해주세요.')
    print('=========' * 9)
    while True:
        print('검색엔진 이미지 수집은 1번,  SNS(Twitter, instagram) 수집은 2번,  뉴스 텍스트 수집은 3번\n'
              '을 입력하세요')
        print('=========' * 9)
        try:
            purpose = int(input(''))
            print('=========')

            if purpose == 1:
                imagecrwaler = ImageCrawler()
                break
            elif purpose == 2:
                type = int(input('트위터(텍스트)는 1번, 인스타그램(이미지)는 2번을 입력하세요  '))
                if type == 1:
                    twitcrawler = TwitCrawler()
                    break
                elif type == 2:
                    instacrwaler = InstaCrawler()
                    break
            elif purpose == 3:
                journalcrawler = JournalCrawler()
                break
            else:
                print('1번 ~ 3번만 사용가능합니다. 다시 입력해주세요')
                print('=========' * 5)

        except:
            print('=========')
            print('잘못 입력하셨습니다. 숫자를 입력해주세요(예, 1)')
            print('=========' * 5)



class ImageCrawler:
    def __init__(self):
        self.keyword = str(input('검색어를 입력하세요 : '))
        self.browser = None
        self.elem = None
        self.soup = None

        self.search_list = {'naver':['https://search.naver.com/search.naver?where=image&amp;sm=stb_nmr&amp;', 'nx_query', '_img', 'c:\\data\\{}_naverImages\\'.format(self.keyword)],
                            'daum':['http://search.daum.net/search?nil_suggest=btn&w=img&DA=SBC&q=', 'q', 'thumb_img', 'c:\\data\\{}_daumImages\\'.format(self.keyword)],
                            'bing':['https://www.bing.com/?scope=images&FORM=Z9LH1', 'sb_form_q', 'mimg', 'c:\\data\\{}_bingImages\\'.format(self.keyword)],
                            'google':['https://www.google.com/imghp?hl=ko', 'lst-ib', 'rg_ic rg_i', 'c:\\data\\{}_googleImages\\'.format(self.keyword)]}
        while True:
            self.searchsite = input('이미지를 검색할 웹브라우저 주소를 입력하세요(naver/daum/bing/google) ')   # 이상한거 입력하면 계속 물어!!
            if self.searchsite in ['naver', 'daum', 'bing', 'google']:
                break
            else:
                print('잘못 입력하셨습니다.')
                continue

        self.cnt = int(input('스크롤을 내릴 횟수를 입력하세요 ')) + 1

        self.Main()


    def Main(self):
        self.get_url()
        self.input_word()

        for i in range(1, self.cnt):
            self.browser.find_element_by_xpath("//body").send_keys(Keys.END)
            # Enter키를 누르면 body를 활성화하겠다.(마우스로 클릭하는 개념), END키 누르기
            time.sleep(3)
        time.sleep(5)
        html = self.browser.page_source  # 크롬 브라우저에서 현재 불러온 소스를 가져온다.
        self.soup = BeautifulSoup(html, "lxml")  # html코드를 검색할 수 있도록 설정
        # 스크롤링 후에 변한 html을 html에 담아준다
        # print(html)

        self.fetch_detail_url()

        self.browser.quit()
        print('=========' * 2)
        print('크롤링이 완료되었습니다.')
        print('=========' * 2)


    def get_url(self):   ###########################url 받아오기###########################
        chrome = 'c:\\data\\chromedriver.exe'
        # 크롬드라이버 경로설정(사전에 설치필요)
        # 팬텀JS를 사용하면 백그라운드로 실행할 수 있다.

        self.browser = webdriver.Chrome(chrome)  # 웹브라우저 인스턴스화
        self.browser.get(self.search_list['{}'.format(self.searchsite)][0])
        # 이미지를 검색할 웹사이트의 주소 입력(이미지만 검색하는 창을 추천한다.)해서 열기

        self.elem = self.browser.find_element_by_id(self.search_list['{}'.format(self.searchsite)][1])  #naver.com같은 경우에는 "nx_query"


    def input_word(self):   ###########################검색어 입력#############################
        self.elem.send_keys(self.keyword)  # 검색어 입력(검색어 입력창과 연결)
        self.elem.submit()            # Enter키


    def fetch_list_url(self):   ############################그림파일 저장##############################
        params = []
        imgList = self.soup.find_all("img", class_=self.search_list['{}'.format(self.searchsite)][2])   # 네이버 이미지 메모리에 해당하는 imgList에 저장
        for img in imgList:
            try:
                params.append(img["src"])
            except:
                params.append(img["data-src"])
        return params

    def fetch_detail_url(self):
        direc_name = self.search_list['{}'.format(self.searchsite)][3]   # 디렉토리 확인해보고 없으면 만들어라!@!@!@!!!!!!
        if not os.path.isdir(direc_name):
            os.mkdir(direc_name)

        params = self.fetch_list_url()
        for idx, img in enumerate(params, 1):
            urllib.request.urlretrieve(img, self.search_list['{}'.format(self.searchsite)][3] + str(idx) + ".jpg")
            # 다운로드 받을 경로 입력


class JournalCrawler:
    def __init__(self):

        self.keyword = str(input('검색어를 입력하세요 '))
        self.browser = None
        self.elem1 = None
        self.elem2 = None
        self.Main()

    def Main(self):
        self.get_url()
        self.input_word()

        self.fetch_list_url2()
        self.browser.quit()
        print('=========' * 2)
        print('크롤링이 완료되었습니다.')
        print('=========' * 2)


    def get_url(self):   ################################url 받아오기################################
        chrome = 'c:\\data\\chromedriver.exe'
        # 크롬드라이버 경로설정(사전에 설치필요)
        # 팬텀JS를 사용하면 백그라운드로 실행할 수 있다.

        self.browser = webdriver.Chrome(chrome)  # 웹브라우저 인스턴스화
        self.browser.get('http://search.joins.com/JoongangNews?Keyword&SortType=New&SearchCategoryType=JoongangNews&PeriodType=All&ScopeType=All&ImageType=All&JplusType=All&BlogType=All&ImageSearchType=Image&TotalCount=0&StartCount=0&IsChosung=False&IssueCategoryType=All&IsDuplicate=True&Page=1&PageSize=10&IsNeedTotalCount=True')
        # 이미지를 검색할 웹사이트의 주소 입력(이미지만 검색하는 창을 추천한다.)

        self.elem1 = self.browser.find_element_by_id('searchKeyword')
        self.elem2 = self.browser.find_element_by_id('btnSearch')

        time.sleep(3)


    def input_word(self):   ################################검색어 입력##################################
        self.elem1.send_keys(self.keyword)  # 검색어 입력(검색어 입력창과 연결)
        self.elem2.click()  # 엔터키 입력인데 왜 안쳐짐?


    def get_save_path(self):   #############################데이터 저장경로 지정################################
        save_path = 'c:\\data\\{}_중앙Texts.txt'.format(self.keyword)
        # save_path = save_path.replace("\\", "/") 필요 없을 것 같은데???

        if not os.path.isdir(os.path.split(save_path)[0]):
            os.mkdir(os.path.split(save_path)[0])  # 지정된 경로에 파일이 없으면 만들어라
        return save_path


    def fetch_list_url(self):   #############################신문사 html 담기##################################
        params = []

        self.browser.find_element_by_xpath("//body")  # 페이지 활성화
        html = self.browser.page_source  # 현재 페이지 소스 담기
        soup = BeautifulSoup(html, "lxml")

        for i in soup.find_all('strong', class_='headline mg'):
            params.append(i('a')[0]['href'])  # find_all은 리스트로 담아준다. 그래서[0]이 필요

        for i in range(9):
            list_url = 'http://search.joins.com' + soup.find_all('a', class_='link_page')[i]['href']

            # 페이지 넘겨주기 위해서 format함수 사용, 치고 들어간 페이지 내에서 찾기

            url = urllib.request.Request(list_url)  # url 요청에 따른 http통신 헤더값을 얻어낸다.
            res = urllib.request.urlopen(url).read().decode("utf-8")
            # 영어가 아닌 한글을 담아내기 위한 문자셋(유니코드)을 사용해서 html문서와 문서 내의 한글을 res변수에 담는다.
            # 즉 loop도는 만큼의 html문서를 한번에 다 담는다.

            # # 참고
            # '''문자set
            #     1. 아스키 코드 : 영문
            #     2. 유니 코드 : 한글, 중국어'''

            soup2 = BeautifulSoup(res, "html.parser")  # res html문서를 BeautifulSoup모듈을 사용해서 검색하도록 설정

            for i in soup2.find_all('strong', class_='headline mg'):
                # print(i('a')[0]['href'])
                params.append(i('a')[0]['href'])
        # print(params)
        return params


    def fetch_list_url2(self):   #######################검색결과 뉴스페이지 접속 후 데이터 긁어오기########################
        params2 = self.fetch_list_url()
        f = open(self.get_save_path(), 'w', encoding='utf-8')  # get_save_path()를 인스턴스화!!

        for i in params2:
            list_url = "{}".format(i)

            url = urllib.request.Request(list_url)
            res = urllib.request.urlopen(url).read().decode('utf-8')

            soup = BeautifulSoup(res, "html.parser")  # res html문서를 BeautifulSoup모듈을 사용해서 검색하도록 설정
            # print(soup('div', id='article_body')[0].get_text(strip=True, separator='\n'))
            article = soup('div', id='article_body')[0].get_text(strip=True, separator='\n')
            # loop돌면서 기사가 계속 바뀐다.
            f.write(article + '\n' * 2 + '='.ljust(50, '=') + '\n')  # 기사 바뀌면서 계속 적어라!

        f.close()


class TwitCrawler():
    def __init__(self):
        self.crawURL = 'https://twitter.com/search-advanced'
        self.keyword = str(input('검색어를 입력하세요~  '))
        self.input_since = str(input('검색을 시작할 날짜를 입력하세요(예, 2001-1-1 | 0 넣지 마세요)  '))
        self.input_until = str(input('검색을 종료할 날짜를 입력하세요(예, 2001-12-31 | 0 넣지 마세요)  '))
        self.count = int(input('스크롤을 몇번 내릴까요?(한번당 15개 게시물 추가)  '))
        self.FILE_PATH = 'c:\\data\\{}_twitTexts.txt'.format(self.keyword)
        self.Main()


    def Main(self):
        self.write_twit_data()


    def get_save_path(self):
        save_path = self.FILE_PATH.replace("\\", "/")        # 굳이 할 필요 없음~
        if not os.path.isdir(os.path.split(save_path)[0]):   # 디렉토리 없으면 만들고~
            os.mkdir(os.path.split(save_path)[0])
        return save_path


    def get_twit_data(self):

        binary = 'c:\\data\\chromedriver.exe'
        browser = webdriver.Chrome(binary)
        browser.get(self.crawURL)
        elem = browser.find_element_by_name("ands")
        since = browser.find_element_by_id("since")
        until = browser.find_element_by_id("until")
        #find_elements_by_class_name("")
        elem.send_keys(self.keyword)
        since.send_keys(self.input_since)
        until.send_keys(self.input_until)

        elem.submit()
        for i in range(1,self.count):
            browser.find_element_by_xpath("//body").send_keys(Keys.END)
            time.sleep(5)

        time.sleep(5)
        html = browser.page_source  # 내가 브라우져로 보고있는 소스를 볼려고하는것이다.
                                    # 그런데 그냥 열면 사용자가 end 버튼틀 눌러서 컨트롤
                                    # 한게 반영 안된것이 열린다.
        soup = BeautifulSoup(html,"lxml")
        self.tweet_tag = soup.find_all('div', class_="js-tweet-text-container")
        browser.quit()

    def write_twit_data(self):
        file = open(self.get_save_path(), 'w', encoding='utf-8')
        self.get_twit_data()
        for i in self.tweet_tag:
            tweet_text = i.get_text(strip=True)
            file.write(tweet_text)
        file.close()



class InstaCrawler:
    def __init__(self):
        self.binary = 'c:\data/chromedriver.exe'
        self.driver = None
        self.soup = None
        self.id = input('아이디를 입력하세요  ')
        self.pwd = input('패스워드를 입력하세요  ')
        self.keyword = input('검색어를 입력하세요  ')
        self.FILE_PATH = 'c:\\data\\{}_instaImages\\'.format(self.keyword)
        self.count = int(input('스크롤을 몇번 내릴까요?(한번당 15개 게시물 추가)  '))
        self.Main()

    def Main(self):
        self.get_url()
        self.get_data()
        self.fetch_detail_url()
        self.driver.quit()
        print('=========' * 2)
        print('크롤링이 완료되었습니다.')
        print('=========' * 2)

    def get_url(self):
        self.driver = webdriver.Chrome(self.binary)
        self.driver.get("https://www.instagram.com/explore/")
        self.driver.find_element_by_name("username").clear()
        self.driver.find_element_by_name("username").send_keys(self.id)
        self.driver.find_element_by_name("password").clear()
        self.driver.find_element_by_name("password").send_keys(self.pwd)
        self.driver.find_element_by_name("password").submit()
        time.sleep(5)
        self.driver.find_element_by_css_selector("div._etslc").click()

    def get_data(self):
        elem = self.driver.find_element_by_css_selector("input._9x5sw._qy55y")
        elem.clear()
        elem.send_keys(self.keyword)
        time.sleep(5)
        elem.send_keys(Keys.ENTER)
        time.sleep(5)
        # 반복할 횟수
        self.driver.find_element_by_css_selector('a._8imhp._glz1g').send_keys(Keys.ENTER)
        for i in range(1, self.count):
            self.driver.find_element_by_xpath("//body").send_keys(Keys.END)
            time.sleep(5)
        time.sleep(5)
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, "lxml")

    def fetch_list_url(self):
        params = []
        imgList = self.soup.find_all("img", class_="_icyx7")
        for im in imgList:
            params.append(im["src"])
        return params

    def fetch_detail_url(self):
        params = self.fetch_list_url()

        direc_name = self.FILE_PATH.replace("\\", "/")    # 디렉토리 확인해보고 없으면 만들어라!@!@!@!!!!!!
        if not os.path.isdir(direc_name):
            os.mkdir(direc_name)

        for idx ,p in enumerate(params, 1):
            # 다운받을 폴더경로 입력
            urllib.request.urlretrieve(p, direc_name + str(idx) + ".jpg")


if __name__ == '__main__':
    while True:
        input_order()

