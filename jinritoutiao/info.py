import requests
import time
import pymysql

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree



# chrome_options = Options()
# chrome_options.add_argument("--headless")
# browser = webdriver.Chrome(chrome_options=chrome_options)

browser = webdriver.Chrome()


url = "https://www.toutiao.com/ch/stock_channel/"

browser.get(url)
for i in range(2):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)


html = browser.page_source



print(html)










if __name__ == '__main__':
    url = "https://www.toutiao.com/ch/stock_channel/"



