import re
import requests

from lxml import etree
from selenium import webdriver
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

    def crawl_daili66(self, page_count=5):
        """
        获取代理66
        :param page_count: 获取的页码
        :return: 代理
        """
        # 这个网站每次都要验证cookie，每次都要更换cookie值有点麻烦，换成selenium获取页面数据

        # 实例化浏览器对象
        browser = webdriver.PhantomJS()
        start_url = "http://www.66ip.cn/{}.html"
        urls = [start_url.format(pageNum) for pageNum in range(1, page_count + 1)]
        for url in urls:
            # html = requests.get(url=url, headers=headers1)
            browser.get(url)
            html = browser.page_source

            # text = html.content.decode("gb2312")
            text = html
            pattern = re.compile(r"<td>(?P<ip>[\d.]+)</td><td>(?P<port>\d+)</td>")
            results = re.finditer(pattern, text)
            for result in results:
                ip = result.group("ip")
                port = result.group("port")
                yield ":".join([ip, port])

    def crawl_proxy360(self, page_count=5):
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

    def crawl_goubanjia(self, page_count=5):
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
