import requests
from bs4 import BeautifulSoup

url_start = 'http://search.tibet.cn:8080/was5/web/search?page='
url_end = '&channelid=249985&searchword=央勒节&perpage=&token=1.1513150071961.17&templet='
url_list = []
for i in range(1, 8):
    url_list.append(url_start + str(i) + url_end)


def get_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    serp = soup.find_all('a', class_='searchresulttitle')
    title_list = []
    href_list = []
    title_set = []
    for i in serp:
        title_set = set(title_list)
        if i.contents[0] not in title_set:
            title_list.append(i.contents[0])
            href_list.append(i.get('href'))
            title_set = set(title_list)
    return title_set, href_list


title_list = []
href_list = []
for i in url_list:
    title, href = get_url(i)
    title_list.extend(title)
    href_list.extend(href)

import re

# (./W020220319316744186592.jpg)
# [](http://www.news.cn/politics/leaders/2022-03/01/c_1128427391.htm)
pattern = re.compile(r'(!\[.*?jpg\))|(!\[.*?gif\))|(\(\.\/.*?jpg\))|(!\[.*?png\))|(\[.*?htm\))|(\[.*?shtml\))')
import html2text


def get_text(href_list, filepath):
    f = open(filepath, 'w', encoding='utf8')
    for i in href_list:
        res = requests.get(i)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        debug = soup.find_all('div', class_='TRS_Editor')
        if debug != []:
            text = soup.find_all('div', class_='TRS_Editor')[0].contents
            text = ' '.join('%s' % id for id in text)

            content = re.sub(pattern, '', html2text.html2text(text).replace('\n', ''))
            f.write(content + '\n')
    f.close()


print(title_list)
get_text(href_list, 'tibet_cn_yangle.txt')
