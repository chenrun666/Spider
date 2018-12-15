import re
import requests
from lxml import etree
from pyquery import PyQuery as pq

from proxy_poll.settings import *

headers = {
    "User-Agent": USER_AGENT
}

url = "http://www.swei360.com/?page=1"


def get_page(url):
    html = requests.get(url, headers=headers)

    if html.status_code == 200:
        tree = etree.HTML(html.content.decode("gb2312"))
        info = tree.xpath('//*[@id="list"]/table/tbody')[0]
        for num in range(1, 11):
            info_list = info.xpath(f"./tr[{num}]//text()")
            ip, port, _, category, _, _, _, _ = [ip for ip in info_list if ip.strip() != '']
            print(ip, port, category)
    else:
        print("请求失败")


def goubanjia(url):
    html = requests.get(url, headers=headers)

    if html.status_code == 200:
        doc = pq(html.text)
        trs = doc("tbody").items()
        for tr in trs:
            tds = tr("td.ip").items()
            category = tr("td").eq(2).text()
            for td in tds:
                td.find("p").remove()
                print(td.text().replace("\n", "").replace(" ", ""))





headers1 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Cookie": "yd_cookie=70e5c339-7e77-4681687dcc5a696de1663dcb5f30079cee96; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1544782139; _ydclearance=a1594a933497122226c2346b-d879-448f-b3d0-1ed12d85c4d6-1544799914; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1544792716",
    "Host": "www.66ip.cn",
    "Pragma": "no-cache",
    "Referer": "http://www.66ip.cn/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",

}

def daili66(url):
    html = requests.get(url=url, headers=headers1)

    if html.status_code == 200:
        print("请求成功")
        text = html.content.decode("gb2312")
        pattern = re.compile(r"<td>(?P<ip>[\d.]+)</td><td>(?P<port>\d+)</td>")
        results = re.finditer(pattern, text)
        for result in results:
            ip = result.group("ip")
            port = result.group("port")
            yield ":".join([ip, port])
    else:
        print("缺少cookie")



if __name__ == '__main__':
    import redis

    db = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    # db.zadd("proxies", {"128.09.90.111": 80})
    # 按照索引取值，并且前包后包
    # a = db.zrevrange("proxies", 0, 2)
    # 按照分数取值
    # a = db.zrangebyscore("proxies", 91, 100)
    # db.zadd("proxies", {"103.194.233.45:18186": 9})
    db.zincrby("proxies", -1, "103.194.233.45:18186")

