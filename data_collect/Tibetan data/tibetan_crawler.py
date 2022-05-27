import requests
from bs4 import BeautifulSoup
import urllib
import unicodedata
import html2text
import re
import time


# རྒྱལ་རྩེ་མདའ་དམག
# keyword = 'རྒྱལ་རྩེ་མདའ་དམག'
# res = requests.get(
#     'https://www.yongzin.com/page/search.do?pageNo=1&word=%E0%BD%A6%E0%BE%A4%E0%BD%B4%E0%BC%8B%E0%BD%A7%E0%BE%B2%E0%BD%BA%E0%BD%84%E0%BC%8B%E0%BD%A3%E0%BD%BC%E0%BC%8B%E0%BD%82%E0%BD%A6%E0%BD%A2&pageSize=10&searchId=9f614bdbd0a74a00ac59c36ffa1764ae&referId=&flagWord=%E0%BD%A6%E0%BE%A4%E0%BD%B4%E0%BC%8B%E0%BD%A7%E0%BE%B2%E0%BD%BA%E0%BD%84%E0%BC%8B%E0%BD%A3%E0%BD%BC%E0%BC%8B%E0%BD%82%E0%BD%A6%E0%BD%A2%E0%BC%8D&spellCorrectEnabled=true&order=&filterDataIds=8348EA5BB15AEC1F0A867EFA85EB3B66n%2CD4494D46D408D817BDD7E7C47689B971n%2C46338D7244C66B8B31B36EE33ACFEABCn%2C48C3C2AC748C9FB972D59D60928DE012n%2C0000000052542f2d01525e4f0ac03113%2C40288cbd59004d08015938f94d895ae8%2Cedf06e87d04e47e8a0d99670cda4b1ba%2C40288cbe66c2a82a0166d3764bd521d3%2C40288cc166f0fc5601670758ccaa33b6%2C40288cc166f0fc560167074a58343396%2C')
# soup = BeautifulSoup(res.text, features='lxml')
#
# serp = soup.find_all('div', class_='result')
# href_list = []
# for i in range(4, 14):
#     href = serp[i].find_all('a')[0].get('href')
#     href_list.append(href)
# print(href_list)


def get_url_list(url, is_first_page):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features='lxml')
    serp = soup.find_all('div', class_='result')
    href_list = []
    start = 4 if is_first_page else 1
    for i in range(start, 10):
        href = serp[i].find_all('a')[0].get('href')

        href_list.append(href)
    return href_list


def get_website_name(href_list):
    output_list = []
    for i in href_list:
        flag, stop_idx = 0, 0
        web_name = ''
        for idx, j in enumerate(i):
            if j == '/':
                flag += 1
            if flag == 3:
                stop_idx = idx
                web_name = i[:stop_idx]
                break
        if web_name in ['http://tibet.people.com.cn', 'http://tb.tibet.cn', 'http://www.vtibet.com',
                        'http://tb.chinatibetnews.com', 'http://ti.zangdiyg.com']:
            output_list.append(i)
    return output_list


# print(get_website_name(href_list=href_list))

def get_serp(keyword, page_range=10):
    code = urllib.parse.quote(keyword)
    total_url_list = []
    for i in range(1, page_range + 1):
        url = 'https://www.yongzin.com/page/search.do?pageNo=' + str(
            i) + '&word=' + code + '&pageSize=10&searchId=9f614bdbd0a74a00ac59c36ffa1764ae&referId=&flagWord=%E0%BD%A6%E0%BE%A4%E0%BD%B4%E0%BC%8B%E0%BD%A7%E0%BE%B2%E0%BD%BA%E0%BD%84%E0%BC%8B%E0%BD%A3%E0%BD%BC%E0%BC%8B%E0%BD%82%E0%BD%A6%E0%BD%A2%E0%BC%8D&spellCorrectEnabled=true&order=&filterDataIds=8348EA5BB15AEC1F0A867EFA85EB3B66n%2CD4494D46D408D817BDD7E7C47689B971n%2C46338D7244C66B8B31B36EE33ACFEABCn%2C48C3C2AC748C9FB972D59D60928DE012n%2C0000000052542f2d01525e4f0ac03113%2C40288cbd59004d08015938f94d895ae8%2Cedf06e87d04e47e8a0d99670cda4b1ba%2C40288cbe66c2a82a0166d3764bd521d3%2C40288cc166f0fc5601670758ccaa33b6%2C40288cc166f0fc560167074a58343396%2C'
        first_page = True if i == 1 else False
        url_list = get_url_list(url, first_page)
        # print(url_list)
        whitelist_url = get_website_name(url_list)
        total_url_list.extend(whitelist_url)
        print('crawlering page ' + str(i))
        time.sleep(1)
    return total_url_list


def tibet_people_crawler(link):
    log = open('error_site.log', 'a+', encoding='utf-8')
    res = requests.get(link)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, features='lxml')
    # title = soup.find('div', class_='gq_content').find('h1').text
    news_v1 = soup.find('div', style='WORD-WRAP: break-word;word-break:keep-all;text-align:justify;')
    news_v2 = soup.find('div', style='word-wrap:break-word;')
    if news_v1 != None:
        news = ' '.join(news_v1.text.split())
    elif news_v2 != None:
        news = ' '.join(news_v2.text.split())
    else:
        log.write(link + '\n')
        news = ''
        log.close()
    news = ''.join(news.split())
    news = re.sub('།', '། ', news)
    return news


def tibet_cn_crawler(link):
    res = requests.get(link)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, features='lxml')
    # title = soup.find('td', class_='lan_20').text
    content = soup.find_all('font', style='line-height: 150%;')
    if content != None:
        news = [' '.join(i.text.split()) for i in content]
    else:
        with open('error_site.log', 'a+', encoding='utf-8') as f:
            f.write(link+'\n')
        news = ''
    # print(news)
    processed_news = ' '.join(news)
    text = ''.join(processed_news.split())
    text = re.sub('།', '། ', text)

    # print(processed_news)
    return text


def zangdiyangguang_crawler(link):
    res = requests.get(link)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, features='lxml')
    title = soup.find_all('h1', class_='ti')[-1].text
    text_list = soup.find_all('span', style='fine18px;')
    text = ''.join([re.sub(' ', '', i.text) for i in text_list])
    # text = unicodedata.normalize('NFKC', text)
    text = ''.join(text.split())
    text = re.sub('།', '། ', text)
    return text


# http://www.vtibet.com/tb/xw_1629/xwtp/201711/t20171121_642485.html
def vtibet_crawler(link):
    res = requests.get(link)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, features='lxml')
    title = soup.find_all('h1', class_='n_title')[-1].text
    serp = soup.find_all('font', style='font-size: 18pt')
    text = ''.join(i.text for i in serp)
    text = ''.join(text.split())
    text = re.sub('།', '། ', text)
    return text


keyword = 'དབྱར་གནས་དུས་ཆེན།'

crawler_result = []
for i in get_serp(keyword, 20):
    flag, stop_idx = 0, 0
    web_name = ''
    for idx, j in enumerate(i):
        if j == '/':
            flag += 1
        if flag == 3:
            stop_idx = idx
            web_name = i[:stop_idx]
            break
    if web_name == 'http://tibet.people.com.cn':
        crawler_result.append(tibet_people_crawler(i))
    elif web_name == 'http://www.vtibet.com':
        crawler_result.append(vtibet_crawler(i))
    elif web_name == 'http://ti.zangdiyg.com':
        crawler_result.append(zangdiyangguang_crawler(i))
    elif web_name == 'http://tb.tibet.cn':
        crawler_result.append(tibet_cn_crawler(i))

crawler_result = list(set(crawler_result))
f = open('རདབྱར་གནས་དུས་ཆེན།央勒节.txt', 'w', encoding='utf-8')
for i in crawler_result[1:]:
    f.write(i + '\n')
f.close()
