import json
import requests
import pymysql

from xueqiu import settings
from xueqiu import get_information

get_information.read_excel()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/71.0.3578.98 Safari/537.36",
    "cookie_save": settings.cookie
}

# A股列表
A_li = []
# 港股列表
G_li = []
# 美股列表
M_li = []


class Connection(object):
    def __init__(self):
        self.conn = pymysql.connect(**settings.mysql_info)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


def save_mysql():
    with Connection() as db:
        for item in A_li:
            company = item[0]
            title = item[1]
            category = item[2]

            sql = f"insert into info (title, nick, category) values ('{company}', '{title}', '{category}')"
            db.execute(sql)


def compare(title):
    """
    判断文章title是否有关键字
    :param title:
    :return:
    """

    for code, info in get_information.A_dic.items():
        li = []
        if not info["nick"]:
            if info["title"] in title or code in title:
                li.append(info["title"])
                li.append(title)
                li.append("A股")
        else:
            if info["title"] in title or info["nick"] in title or code in title:
                li.append(info["title"])
                li.append(title)
                li.append("A股")
        if li:
            A_li.append(li)


def get_html(url):
    """
    沪深的文章
    :param url:
    :return:
    """
    html = requests.get(url, headers=headers)

    dic_info = json.loads(html.text)

    li = dic_info["list"]
    for item in li:
        title = json.loads(item["data"])["title"]
        compare(title)

    # 拼接下一个url
    max_id = dic_info["next_max_id"]
    if max_id < settings.max_id:
        return
    next_url = f"https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id={max_id}" \
               f"&count=10&category=105"
    get_html(next_url)


if __name__ == '__main__':
    a_url = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_" \
            "id=-1&count=10&category=105"

    get_html(a_url)

    save_mysql()
