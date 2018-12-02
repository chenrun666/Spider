import re
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyquery import PyQuery as pq

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)


def login():
    try:
        browser.get("http://www.taobao.com/")
        click_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-sign > a.h")))
        click_login.click()
        # 扫描二维码等待事件
        time.sleep(8)

    except TimeoutException:
        return login()


def search():
    try:
        # browser.get("http://www.taobao.com/")
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        input.send_keys("美食")
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        return total.text
    except TimeoutException:
        return search()


def next_page(page_num):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        input.clear()
        input.send_keys(page_num)
        submit.click()
        # 判断翻页是否成功
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                     "#mainsrp-pager > div > div > div > ul > li.item.active > span"),
                                                    str(page_num)))
    except TimeoutException:
        return next_page(page_num)


def get_products():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item")))
        html = browser.page_source
        doc = pq(html)
        items = doc("#mainstrp-itemlist .items .item").items()
        print("items--->", items)
        print(list(items))
        for item in items:
            print("item--->", item)
    except TimeoutException:
        return get_products()


def main():
    login()
    total = search()
    total = int(re.compile("(\d+)").search(total).group(1))
    for page_num in range(2, total + 1):
        next_page(page_num)


if __name__ == '__main__':
    main()
