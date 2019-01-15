import requests
from requests.cookies import RequestsCookieJar

url_index = "https://xueqiu.com/#/cn"
url = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=202307&count=15&category=105"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

# 实例cookie管理的类
cookie_jar = RequestsCookieJar()

# 发起请求获取set-cookie(本次请求不需要cookie)
html = requests.get(url_index, headers=headers)
set_cookie = html.headers.get("set-cookie")

# 将获取到的cookie设置到实例好的cookie管理类中
s = {item for item in set_cookie.split("; ")}
for j in s:
    if "=" in j and "domain" not in j:
        k, v = j.split("=")
        cookie_jar.set(k, v, )

# 再次发起请求，携带cookie的管理类
res = requests.get(url, cookies=cookie_jar, headers=headers)
print(res)



