from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import datetime, time



class TwitCrawler():

    def __init__(self,keyword,input_since,input_until,count):
        self.crawURL = 'https://twitter.com/search-advanced'
        self.FILE_PATH = 'c:\\data\\twit.txt'
        self.keyword = str(keyword)
        self.input_since = str(input_since)
        self.input_until = str(input_until)
        self.count = int(count)

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
        #print(soup)
        #print(len(soup))
        self.tweet_tag = soup.find_all('div', class_="js-tweet-text-container")
        browser.quit()

    def write_twit_data(self):
        file = open(self.get_save_path(), 'w', encoding='utf-8')
        self.get_twit_data()
        for i in self.tweet_tag:
            tweet_text = i.get_text(strip=True)
            print(tweet_text)
            file.write(tweet_text)
        file.close()

twit = TwitCrawler('강령술사','2017/6/29','2017/7/2',10)
twit.write_twit_data()
