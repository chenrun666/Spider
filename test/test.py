import requests

from lxml import etree

url = "http://www.haoduanzi.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}

html = requests.get(url, headers=headers).text

tree = etree.HTML(html)

img_div = tree.xpath('//*[@id="main"]/div')

for item in img_div:
    img_url = item.xpath('./div/img/@src')

    if img_url and img_url[0].split(".")[-1] == "jpg":

        img_data = requests.get(img_url[0], headers=headers).content

        with open(f"./{img_url[0].split('/')[-1]}", "wb") as f:
            f.write(img_data)

            print(f"{img_url[0].split('/')[-1]}保存成功")
