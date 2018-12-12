import time

from lxml import etree

from selenium import webdriver


# 拖去整个页面的视屏信息
def complete_page_info(page_url):
    # 实例化一个浏览器对象
    browser = webdriver.PhantomJS()
    # 访问url
    browser.get(page_url)
    # 获取加载更多的btn
    listLoadMore = browser.find_element_by_id("listLoadMore")

    while listLoadMore.text == "加载更多":
        listLoadMore.click()
        time.sleep(0.5)

    page_source = browser.page_source
    tree = etree.HTML(page_source)

    return tree


if __name__ == '__main__':
    url = "https://www.pearvideo.com/category_2"
    complete_page_info(url)
