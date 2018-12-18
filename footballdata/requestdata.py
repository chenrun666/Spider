import re

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import xlwt

base_url = "http://zq.win007.com"


chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options)


def save_excel(team_list):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("sheet1", cell_overwrite_ok=True)
    for x, value in enumerate(team_list):
        # 判断列表长度，清除插入多余数据
        if len(value) < 27:
            value.insert(2, "")
        for y, write_info in enumerate(value):
            sheet.write(x, y, write_info)

    book.save(r"./footdata.xls")


def get_team_url(index_url):
    """

    :param index_url:
    :return: 当前页面的比赛数据，和详细信息的url列表
    """
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser = webdriver.Chrome()
    browser.get(index_url)
    html = browser.page_source

    tree = etree.HTML(html)
    team_trs = tree.xpath('//div[@id="tableId"]/table/tbody/tr')

    back_data = []
    team_data = []
    for index, tr in enumerate(team_trs):
        team_info = tr.xpath(".//text()")
        back_data.append(team_info)

        team_url = tr.xpath("./td[2]/a/@href")
        if team_url:
            team_url = team_url[0]
        team_data.append(team_url)

    return back_data, team_data


def save_team_info(name, result):
    """
    :param name: 球队的名字
    :param result: 接受比赛数据的列表
    :return: 保存excel
    """
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("sheet", cell_overwrite_ok=True)
    for x, value in enumerate(result):
        for y, data in enumerate(value):
            sheet.write(x, y, data)
    book.save(f"{name}.xls")


def team_detail_info(team_url):
    """
    获取比赛的详细信息
    :param team_url:
    :return:
    """
    # browser = webdriver.Chrome()
    browser.get(team_url)
    html = browser.page_source

    tree = etree.HTML(html)
    team_name = tree.xpath('//*[@id="mainTitle"]/table/tbody/tr[1]/td[3]/span[1]/strong/text()')[0]

    team_data = tree.xpath('//div[@id="Tech_schedule"]/table/tbody/tr')
    result = []
    for tr in team_data:
        res_one = [i for i in tr.xpath(".//text()") if i != " "]
        result.append(res_one)

    return team_name, result


def run():
    index_url = "http://zq.win007.com/cn/League/60.html"
    # 返回比赛结果列表，和team_url
    game_info, team_info = get_team_url(index_url)
    # 保存到excel
    save_excel(game_info)
    # 访问详情页面信息
    for url in team_info:
        if isinstance(url, str):
            url = base_url + url
            team_name, result = team_detail_info(url)
            save_team_info(team_name, result)


if __name__ == '__main__':
    run()
