import os
import re
from datetime import datetime
from multiprocessing.dummy import Pool

import requests
from lxml import etree

from li_video import video_selenium

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}


def send_request(send_url):
    html = requests.get(send_url, headers=headers).text
    tree = etree.HTML(html)

    return tree


def get_video_url(tree):
    """

    :param index_url:
    :return: (title, url)
    """
    # tree = send_request(index_url)

    video_code = tree.xpath('//div[@class="vervideo-bd"]/a/@href')

    # 获取类别
    global category
    category = tree.xpath('//li[@id="select"]/a/text()')[0]

    # 获取title
    title_list = tree.xpath('//div[@class="vervideo-title"]/text()')
    # 通过正则匹配出汉字,作为视频的文件名称
    partten = re.compile("([\u4E00-\u9FA5]+)")
    title_list_after = map(lambda x: re.findall(partten, x), title_list)

    prefix_url = "https://www.pearvideo.com/"
    video_url = [("".join(title), prefix_url + video_code[index]) for index, title in enumerate(title_list_after)]

    # print("获取video成功：", video_url)

    return video_url


def get_video_detail(video_url):
    html = requests.get(video_url, headers=headers).text

    # 视频的播放地址是通过js加载到页面上的。所以xpath是拿不到的
    pattern = re.compile('srcUrl="(.*?)"')
    download_video_url = re.findall(pattern, html)[0]

    print("获取下载url成功：", download_video_url)

    return download_video_url


def get_video_url_tuple(video_list):
    """
    构造视频title 和 视频下载链接地址的元祖。
    :param video_list:
    :return:
    """
    for title, url in video_list:
        download_video_url = get_video_detail(url)
        yield (title, download_video_url)


def download_video(video_info_tuple):
    """
    :param video_info: (title, url)
    :return:
    """
    # 判断文件夹是否存在，以时间作为文件名称
    date = datetime.now().date()
    video_path = f"/Users/chenrun/Public/梨视频/{date}/{category}"
    dir_exists = os.path.exists(video_path)
    if not dir_exists:
        os.makedirs(video_path)

    # 避免了已经下载的文件重复下载。
    filename_bool = os.path.exists(f"{video_path}/{video_info_tuple[0]}.mp4")

    if not filename_bool:
        print(f"{video_info_tuple[0]}开始下载。。。")
        video_data = requests.get(video_info_tuple[1], headers).content
        with open(f"{video_path}/{video_info_tuple[0]}.mp4", "wb") as f:
            f.write(video_data)
            print(f"{video_info_tuple[0]}》》》》》》下载完成")


if __name__ == '__main__':
    """
    category_num: num = 10: 新知； num = 2: 世界； num = 8: 科技; num = 59: 音乐
    """
    num = input("请输入你想下载的类别的数字：")
    get_data = input("是否获取整个页面数据：(yes/no)")

    url = f"https://www.pearvideo.com/category_{num}"
    if get_data.lower() == "no" or get_data.lower() == "n":
        tree = send_request(url)
    elif get_data.lower() == "y" or get_data.lower() == "yes":
        # 获取整个页面数据的url
        tree = video_selenium.complete_page_info(url)
    else:
        raise Exception("请正确填写yes or no")

    video_detail_list = get_video_url(tree)
    # 实例化一个线程池
    pool = Pool(10)
    pool.map(download_video, get_video_url_tuple(video_detail_list))
    pool.close()
    pool.join()
