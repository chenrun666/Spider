"""
# version.1
爬取抖音由于滑动过快而出现的文件打开过多
解决方案：使用队列
将链接放置到队列中，让worker从队列中那到链接访问下载。放置循环过快打开的文件过

# version.2
爬取抖音视频重复问题
解决方案：获取到url进行md5值解密，放入redis中，每次访问到redis中查询是否下载过了。
为什么放到redis不妨到内存中（代码中）。
防止之后获取到url而再次下载(连接不一致但是可能视频一直，牛逼，发现?rc=后面的字符串一直则视频一直。所以根据这个字符串去重)
"""

import requests

from celery import Celery

app = Celery("tasks",
             broker="redis://127.0.0.1:6379/0",
             backend="redis://127.0.0.1:6379/0",
             )


@app.task
def download(url, path, video_num):
    content = requests.get(url=url, stream=True)
    with open(f"{path}/{video_num}.mp4", "ab") as f:
        f.write(content.content)
        f.flush()
