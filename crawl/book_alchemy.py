from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker


from crawl.crawl_book import crawl_info, Crawl_wuxia, URL

engine = create_engine('mysql+pymysql://root:asd.zxc123@localhost/books')
Base = declarative_base()

class Books(Base):
    __tablename__ = 'djgapp_books'
    id = Column(Integer, primary_key=True)
    book_name = Column(Text)
    author = Column(Text)
    brief = Column(Text)

    def __init__(self, book_name, author, brief):
        self.book_name = book_name
        self.author = author
        self.brief = brief

    def __repr__(self):
        return "<books('%s', '%s', '%s')>" % (self.book_name, self.author, self.brief,)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_book(url):
    info = crawl_info(url=url, text=False, tags='div', class_='book')
    name = info[0]
    brief = info[1]

    try:
        ed_book = Books(book_name=name[0], author=name[1], brief=brief)
    except IndexError:
        ed_book = Books(book_name=1, author=1, brief=1)

    session.add(ed_book)
    session.commit()
    session.close()


def add_books():
    crawl_wuxia = Crawl_wuxia(url=URL)
    url_list = crawl_wuxia.complex_url()
    for url in url_list:
        try:
            add_book(url=url)
        except Exception as e:
            continue

if __name__ == '__main__':
    add_books()