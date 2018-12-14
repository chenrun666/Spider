import re
import requests

from lxml import etree
from pyquery import PyQuery as pq

from proxy_poll.settings import *

headers = {
    "User-Agent": USER_AGENT
}


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs["__CrawlFunc__"] = []
        for k, v in attrs.items():
            if "crawl_" in k:
                attrs["__CrawlFunc__"].append(k)
                count += 1
        attrs["__CrawlFuncCount__"] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval(f"self.{callback}()"):
            print("成功获取到代理", proxy)
            proxies.append(proxy)

        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 获取的页码
        :return: 代理
        """
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
        start_url = "http://www.66ip.cn/{}.html"
        urls = [start_url.format(pageNum) for pageNum in range(1, page_count + 1)]
        for url in urls:
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

    def crawl_proxy360(self, page_count=4):
        """
        获取360代理
        :return: 代理
        """
        start_url = "http://www.swei360.com/?page={}"
        urls = [start_url.format(pageNum) for pageNum in range(1, page_count + 1)]
        for url in urls:
            html = requests.get(url, headers=headers)

            if html.status_code == 200:
                tree = etree.HTML(html.content.decode("gb2312"))
                info = tree.xpath('//*[@id="list"]/table/tbody')[0]
                for num in range(1, 11):
                    info_list = info.xpath(f"./tr[{num}]//text()")
                    ip, port, _, category, _, _, _, _ = [ip for ip in info_list if ip.strip() != '']
                    yield ":".join([ip, port])
            else:
                print("请求失败")

    def crawl_goubanjia(self, page_count=4):
        """
        获取goubanjia
        :param page_count:
        :return: 代理
        """
        start_url = "http://www.swei360.com/?page={}"
        urls = [start_url.format(pageNum) for pageNum in range(1, page_count + 1)]
        for url in urls:
            html = requests.get(url, headers=headers)

            if html.status_code == 200:
                doc = pq(html.text)
                tds = doc("td.ip").items()
                for td in tds:
                    td.find('p').remove()
                    ip_info = td.text().replace(" ", "").replace("\n", "")
                    yield ip_info
