"""
http://industry.nbd.com.cn/
标题，摘要，来源，作者，浏览量，转载量，评论数，点赞数
"""
import requests
import time
import pymysql

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree

headers = {
    "User-Agent": ": Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML,"
                  " like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "connection": "close"
}

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options)


class Connect(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, database="industry",
                                    user="root", password="123456")
        self.cos = self.conn.cursor()

    def __enter__(self):
        return self.cos

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        self.cos.close()


def more_info(url):
    browser.get(url)
    more = browser.find_element_by_xpath("//div[@class='g-columnnews']/a")
    n = 0
    while n < 1:
        more.click()
        time.sleep(5)
        n += 1

    html = browser.page_source

    browser.close()

    return html


def get_page(html):
    tree = etree.HTML(html)

    title = tree.xpath("//ul/li/div/div/a[1]/text()")
    abstrct = tree.xpath("//ul/li/div/div/div/a/text()")
    source = tree.xpath("//ul/li/div/div/p/span[1]/text()")
    browse = tree.xpath("//ul/li/div/div/p/span[3]/text()")

    # 详细内容url
    page_url = tree.xpath("//ul/li/div/div/a[1]/@href")

    # 全局的dic，因为后边的函数要在里面添加作者
    global dic
    dic = {k: [v1, v2, v3] for k, v1, v2, v3 in zip(title, abstrct, source, browse)}

    return page_url, title


def get_author(page_url, title):
    """
    获取作者
    :param page_url:  详细信息的url
    :param title: 文章的标题，对应字典的key
    :return:
    """
    html = requests.get(url=page_url, headers=headers).text
    tree = etree.HTML(html)

    author = tree.xpath("//div[@class='g-article']/div[@class='g-articl-text']/p[1]/text()")

    # 可能没有获取到作者报错
    # 先处理异常
    try:
        dic[title].append(author[0].strip().split("\xa0\xa0\xa0\xa0"))
    except Exception as e:
        print(e)
        print(title)
        get_author(page_url, title)


def save_mysql():
    print(dic)

    for k, v in dic.items():
        title = k
        abstrct, source, browser = ["".join(i) for i in v if isinstance(i, str)]
        author = ",".join(v[-1])

        sql = "insert into article (title, abstrct, source, browse, author) values {}".format(
            (title, abstrct, source, browser, author)
        )


        # print(sql)

        with Connect() as db:
            db.execute(sql)


# '九连板！ 是谁在追涨风范股份？': ['要闻', '每日经济新闻 ', '8531  阅读 ', ['每经记者 胥帅', '每经编辑 魏官红']]

def run(url_start):
    html = more_info(url_start)
    next_url, title = get_page(html)

    # 将url和title对应起来（k：url，v：title）
    tmp = {k: v for k, v in zip(next_url, title)}
    for k, v in tmp.items():
        get_author(k, v)

    save_mysql()


if __name__ == '__main__':
    industry_url = "http://industry.nbd.com.cn/"

    run(industry_url)

