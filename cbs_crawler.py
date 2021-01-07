import urllib.request  # 웹브라우저에서 html 문서를 얻어오기위해 통신하는 모듈
from  bs4 import BeautifulSoup  # html 문서 검색 모듈
import os
import re

def get_save_path():
    save_path = input("Enter the file name and file location :" )
    save_path = save_path.replace("\\", "/")
    if not os.path.isdir(os.path.split(save_path)[0]):
        os.mkdir(os.path.split(save_path)[0])
    return save_path


def fetch_list_url():
    params = []
    for i in range(1, 2):
        for j in range(15):
            list_url = "http://www.cbs.co.kr/radio/pgm/board.asp?page=" + str(i) + "&pn=list&skey=&sval=&bgrp=2&bcd=00350012&pcd=board&pgm=111&mcd=BOARD2"
            # request_header = urllib.parse.urlencode({"page": j})
            # print (request_header) # 결과 page=1, page=2 ..
            # request_header = request_header.encode("utf-8")
            # print (request_header) # b'page=29'
            url = urllib.request.Request(list_url)
            # print (url) # <urllib.request.Request object at 0x00000000021FA2E8>
            res = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(res, "html.parser")
            soup2 = soup.find_all("a", class_="bd_link")[j]["href"]
            # print(soup2)
            soup3 = re.search("[0-9,',']{11}", soup2).group().split(',')
            # 숫자 사이에 콤마로 구분되어 있는 문자를 찾아라!
            # print(soup3)
            params.append(soup3)
            # print(params)


    return params

def fetch_list_url2():
    params2 = fetch_list_url()
    f = open(get_save_path(), 'w', encoding ="utf-8")
    for i in params2:
        detail_url = "http://www.cbs.co.kr/radio/pgm/board.asp?pn=read&skey=&sval=&anum={}&vnum={}&bgrp=2&page=1&bcd=00350012&pcd=board&pgm=111&mcd=BOARD2".format(i[1], i[0])
        # request_header = urllib.parse.urlencode({"RCEPT_NO": str(i) })
        # request_header = request_header.encode("utf-8")
        print(detail_url)
        url = urllib.request.Request(detail_url)
        res = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(res, "html.parser")
        # print(soup)
        title = soup.find("td", class_="bd_menu_content").get_text()
        content = soup.find("td", class_='bd_article').get_text()
        # print(title, '\n', content)

        f.write("==" * 30 + "\n")
        f.write(title + "\n")
        f.write(content + "\n")
        f.write("==" * 30 + "\n")
    f.close()
fetch_list_url2()
