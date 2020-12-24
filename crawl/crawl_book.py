import re

import requests
from requests import RequestException
from bs4 import BeautifulSoup

BOOK_RULE = r'./book/(.*).html"'

BOOK_NAME_RULE = r'<h1>(.*)</h1>'

AUTHOR_RULE = r'.html">(.*)</a></h2>'

BRIEF_RULE = r'<p>(.*)\W{6}</p>'

CHAPTER_RULE = r'html">(.*)</a></dd>'


URL = 'http://www.wuxia.net.cn/book.html'

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

class Crawl:
    def __init__(self, url):
        self.url = url
        self.session = requests.session()

    def get_soup(self):
        self.response = self.session.get(self.url, headers=HEADERS)
        self.response.encoding = 'UTF-8'
        soup = BeautifulSoup(self.response.text, 'html.parser')
        return soup

    def remove_none(self, list):
        for i in list:
            if not i:
                list.remove(i)
                return self.remove_none(list)
        return list

class Crawl_wuxia(Crawl):
    def get_url(self, soup):
        book_url = []
        for i in soup.find_all('a'):
            book_url.append(re.findall(BOOK_RULE, str(i)))
        return book_url

    def complex_url(self):
        url_list = (self.get_url(self.get_soup()))
        self.remove_none(url_list)
        new_url_list = []
        n = 0

        for i in url_list:
            new_url_list.append('http://www.wuxia.net.cn/book/' + i[0] +'.html')

        return new_url_list

def remove_tags(tags, text):
    return re.sub(tags, '', text)

def crawl_info(url, tags, class_=None, text=False, chapter=False):
    content = ''
    new_crawl = Crawl_wuxia(url)
    book_info = []
    brief = []
    if text:
        for i in new_crawl.get_soup().find_all(tags):
            content += remove_tags('<p></p>', i) + '\r\n'
        return content
    else:
        if not chapter:
            for i in new_crawl.get_soup().find_all(tags, class_=class_):
                book_info.extend(re.findall(BOOK_NAME_RULE, str(i)))
                book_info.extend(re.findall(AUTHOR_RULE, str(i)))
            for i in new_crawl.get_soup().find_all(tags, class_='description'):
                brief.extend(''.join(remove_tags("<h3></h3><p></p>", i.text)))
            return (book_info, ''.join(brief))
        else:
            # for i in new_crawl.get_soup().find_all(tags, )
            ...

def crawl_chapter():
    ...

if __name__ == '__main__':
    print(Crawl_wuxia(url='http://www.wuxia.net.cn/book/bahaifengyun.html').get_soup())
