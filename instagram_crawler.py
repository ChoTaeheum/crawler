import urllib.request
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

class InstaCrawler:
    def __init__(self):
        self.binary = 'c:\data/chromedriver.exe'
        self.driver = None
        self.soup = None
        self.id = input('아이디를 입력하세요  ')
        self.pwd = input('패스워드를 입력하세요  ')
        self.keyword = input('검색어를 입력하세요  ')
        self.FILE_PATH = 'c:\\data\\{}_insta\\'.format(self.keyword)
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


instacrwaler = InstaCrawler()
