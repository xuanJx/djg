import re

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker, relationship, backref

from crawl.crawl_book import crawl_info, Crawl_wuxia, URL

MARK_RULE = r'http://www.wuxia.net.cn/book/(.*).html'

book_engine = create_engine('mysql+pymysql://root:@localhost/books')
Base = declarative_base()


class Books(Base):
    __tablename__ = 'djgapp_books'
    id = Column(Integer, primary_key=True)
    book_name = Column(Text)
    author = Column(Text)
    brief = Column(Text)
    mark = Column(String(2))

    def __init__(self, book_name, author, brief, mark):
        self.book_name = book_name
        self.author = author
        self.brief = brief
        self.mark = mark

    def __repr__(self):
        return "<books('%s', '%s', '%s', '%s')>" % (self.book_name, self.author, self.brief, self.mark)

class Chapter(Base):
    __tablename__ = 'djgapp_chapter'
    id = Column(Integer, primary_key=True)
    chapter_name = Column(Text)
    chapter_content = Column(LONGTEXT)
    book_id = Column(Integer, ForeignKey('djgapp_books.id'))
    #
    # def __init__(self, chapter_name, chapter_content):
    #     self.chapter_name = chapter_name
    #     self.chapter_content = chapter_content

    def __repr__(self):
        return "<chaptes('%s', '%s')>" % (self.chapter_name, self.chapter_content)

Base.metadata.create_all(book_engine)

Book_session = sessionmaker(bind=book_engine)
book_session = Book_session()


def add_book(url, n):
    mark = str(re.findall(MARK_RULE, url)[0])[0]
    info = crawl_info(url=url, tags='div', class_='book')
    name = info[0]
    brief = info[1]
    all_ed = []

    try:
        ed_book = Books(book_name=name[0], author=name[1], brief=brief, mark=mark)
    except IndexError:
        ed_book = Books(book_name=1, author=1, brief=1, mark=1)

    all_ed.append(ed_book)

    chapter_url_list = Crawl_wuxia(url).complex_url()
    for i in chapter_url_list:
        chapter_info = crawl_info(url=i, chapter=True)
        chapter_name = chapter_info[0]
        chapter_content = chapter_info[1]

        try:
            ed_chapter = Chapter(chapter_name=chapter_name, chapter_content=chapter_content, book_id=n)
            all_ed.append(ed_chapter)
        except IndexError or Exception:
            ed_chapter = Chapter(chapter_name=str(1), chapter_content=str(1), book_id=n)
            all_ed.append(ed_chapter)

    book_session.add_all(all_ed)
    book_session.commit()
    book_session.close()


def add_books():
    n = 0
    crawl_wuxia = Crawl_wuxia(url=URL)
    url_list = crawl_wuxia.complex_url()
    for url in url_list:
        n += 1
        try:
            add_book(url=url, n=n)
        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    add_books()