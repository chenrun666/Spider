import requests

from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    "connection": "closed"
}


def get_page(index_url):
    html = requests.get(index_url, headers=headers).text

    tree = etree.HTML(html)

    resume_url_list = tree.xpath('//div[@id="main"]/div/div/a/@href')
    for resume_url in resume_url_list:
        get_resume(resume_url)


def get_resume(resume_url):
    html = requests.get(resume_url).text

    tree = etree.HTML(html)

    # 获取下载地址
    down_url_list = tree.xpath('//div[@class="down_wrap"]//li/a/@href')
    for down_url in down_url_list:
        filename = down_url.split("/")[-1]
        down_data = requests.get(down_url, headers=headers).content
        with open(f"./简历/{filename}", "wb") as f:
            f.write(down_data)
            print(filename, ">>>下载成功！！！")
            break


def download_resume(index_url):
    get_page(index_url)


if __name__ == '__main__':
    for page_num in range(5, 10):
        if page_num == 1:
            url = "http://sc.chinaz.com/jianli/free.html"
        else:
            url = f"http://sc.chinaz.com/jianli/free_{page_num}.html"

        download_resume(url)
