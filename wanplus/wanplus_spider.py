import time
import xlwt
from lxml import etree
from selenium import webdriver

browser = webdriver.Chrome()

browser.get("https://www.wanplus.com/lol/playerstats")

html = browser.page_source

tree = etree.HTML(html)

book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet("KDA", cell_overwrite_ok=True)
y = 0
header_list = tree.xpath("//table[@id='DataTables_Table_0']/thead/tr/th/text()")

header_list = [option.strip() for option in header_list if option.strip() != ""]


def save_data():
    global y
    if y == 0:
        for index, write_data in enumerate(header_list):
            if write_data:
                sheet.write(0, index, write_data)

    html = browser.page_source
    tree = etree.HTML(html)
    tr_list = tree.xpath("//table[@id='DataTables_Table_0']/tbody/tr")
    for tr in tr_list:
        y += 1
        player_data = tr.xpath(".//text()")
        if player_data:
            for x, write_data in enumerate(player_data):
                sheet.write(y, x, write_data)


# 获取所有页码数
page_num = tree.xpath('//*[@id="DataTables_Table_0_paginate"]/span//text()')[-1]
if int(page_num) >= 1:
    for i in range(1, int(page_num) + 1):
        save_data()
        next_page = browser.find_element_by_xpath('//*[@id="DataTables_Table_0_next"]')

        next_page.click()
        time.sleep(0.5)


book.save("KDA_data.xls")

browser.close()
