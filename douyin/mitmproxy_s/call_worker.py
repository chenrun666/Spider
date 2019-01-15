import importlib
import hashlib

download = importlib.import_module("update_script")

path = "/Users/chenrun/Public/抖音"
video_num = 1000

md = hashlib.md5()
urled = []

def response(flow):
    target_urls = [
        "http://v1-dy.ixigua.com/",
        "http://v3-dy.ixigua.com/",
        "http://v6-dy.ixigua.com/",
        "http://v9-dy.ixigua.com/",
    ]

    global video_num
    for url in target_urls:
        if flow.request.url.startswith(url):
            url_str = str(flow.request.url)
            prefix = url_str.split("rc=")[-1]
            md.update(bytes(prefix, encoding="utf-8"))
            secret = md.digest()
            # 判断是否已经下载过
            if secret not in urled:
                # 加入到已下载列表中
                urled.append(secret)
                download.download.delay(flow.request.url, path, video_num)
                video_num += 1

                with open("url_log.log", "a", encoding="utf-8") as f:
                    f.write(str(flow.request.url) + "\n\n")
