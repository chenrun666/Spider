import re
import requests

from lxml import etree

from doubanLogin.YDMHTTP import code_result

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}


def get_valid_code(login_url):
    """
    获取登陆页面的验证码，以及验证码的id值
    :param login_url:
    :return: 验证码对应的ID == captcha_id
    """
    html = requests.get(login_url, headers=headers).text

    tree = etree.HTML(html)

    # 验证码的图片链接，拿到后面的id值
    valid_url = tree.xpath('//div[@class="item item-captcha"]/img/@src')[0]

    # 下载图片
    valid_code_data = requests.get(valid_url, headers=headers).content
    with open("./验证码/captcha.jpg", "wb") as f:
        f.write(valid_code_data)

    # 共url中匹配出captcha_id
    captcha_id_pattern = re.compile(r'.*?id=(.*?)&.*')
    captcha_id = re.findall(captcha_id_pattern, valid_url)[0]

    return captcha_id


def douban_login(login_url):
    captcha_id = get_valid_code(login_url)
    captcha_solution = code_result("./验证码/captcha.jpg")

    data = {
        "source": "index_nav",
        "form_email": "username",
        "form_password": "password",
        "captcha-solution": captcha_solution,
        "captcha-id": captcha_id
    }

    login_url = "https://www.douban.com/accounts/login"

    # 登陆成功之后的页面
    html = requests.post(login_url, data=data).text

    return html


if __name__ == '__main__':
    url = "https://www.douban.com/"
    douban_login(url)
