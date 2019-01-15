import time
import requests

path = "/Users/chenrun/Public/抖音/"


def response(flow):
    target_urls = [
                   "http://v1-dy.ixigua.com/",
                   "http://v3-dy.ixigua.com/",
                   "http://v6-dy.ixigua.com/",
                   "http://v9-dy.ixigua.com/",
                   ]

    for url in target_urls:
        # 筛选出下载的视频链接
        if flow.request.url.startswith(url):
            # 设置视频名字
            filename = path + str(time.time()) + ".mp4"

            res = requests.get(flow.request.url, stream=True)

            with open(filename, "ab") as f:
                f.write(res.content)
                f.flush()
                print(filename + "下载完成")

