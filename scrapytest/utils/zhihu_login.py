# -*- coding: utf-8 -*-
__author__ = 'bobby'

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print ("cookie未能加载")

agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
header = {
    "HOST":"www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': agent,
    'Cookie':'d_c0="AADCzcnW3QuPTpCMMZBINIrCjFd0ywsrXJk=|1496645925"; _zap=7deaee6f-334b-494e-9a77-fb68a62d037d; q_c1=cbfa1b9b32d942de82f457088b98f648|1507959356000|1496633759000; _xsrf=373d479547fe8ce971204a06ec10663d; infinity_uid="2|1:0|10:1518355097|12:infinity_uid|24:OTQ2MTMwNTMzODEwNDU0NTI4|c32bebcb1c9531309f35e069278cae2c47f1b1bf1a40c82f2d08b535f458d6b1"; __utma=155987696.775738611.1518355099.1518355099.1518355099.1; __utmz=155987696.1518355099.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.|1=userId=946130533810454528=1; aliyungf_tc=AQAAABMoIyEPLgEA0QCk3Dko28AoiHQ3; _xsrf=373d479547fe8ce971204a06ec10663d; q_c1=cbfa1b9b32d942de82f457088b98f648|1518434927000|1496633759000; l_cap_id="ZThkZjE4YTgxMmRkNGQ3ZGI3MjhjYzllZmZhY2YyMGM=|1518435276|91e5fd48b3026e7818efc6b4a5cdc68398d2feb4"; r_cap_id="NzQzMWIwZmUyMTZjNGMzYmI0NjIzZjdmZjNjNDI3MWU=|1518435276|a02cd8347cdfaf36c22b6671911b6714ff223fbb"; cap_id="NzI1NjlkNTc0YWJlNDYwOGIzN2I2MDYxOWRiZTBkN2I=|1518435276|1e7f51737e9921e22e7fdb9bd51da12627a21fef"; capsion_ticket="2|1:0|10:1518436749|14:capsion_ticket|44:YzVmMzdmNjQxODA3NGUxNWFhMjU3YmM1ZDczNWVlYzc=|64c2dba2f4c376d2ebe2089f685084c2fee74221ceac9bf1a1c934f366507bad"; z_c0="2|1:0|10:1518436774|4:z_c0|92:Mi4xSXpJRkFnQUFBQUFBQU1MTnlkYmRDeVlBQUFCZ0FsVk5wczl1V3dCaGpSOUVnUE5aQTBLZXlfRkdSZ2gtXzB6WDJn|555873a01b49e54e6ab204c50b0572b97c26e3fb390186d7709843c0498d9f3b"'
}

def is_login():
    #通过个人中心页面返回状态码来判断是否为登录状态
    inbox_url = "https://www.zhihu.com/question/56250357/answer/148534773"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True

def get_xsrf():
    #获取xsrf code
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print ("ok")

def get_captcha():
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg","wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = input("输入验证码\n>")
    return captcha

def zhihu_login(account, password):
    #知乎登录
    # if re.match("^1\d{10}",account):
    #     print ("手机号码登录")
    #     post_url = "https://www.zhihu.com/login/phone_num"
    #     post_data = {
    #         "_xsrf": get_xsrf(),
    #         "phone_num": account,
    #         "password": password,
    #         "captcha":get_captcha()
    #     }
    # else:
    #     if "@" in account:
    #         #判断用户名是否为邮箱
    #         print("邮箱方式登录")
    #         post_url = "https://www.zhihu.com/login/email"
    #         post_data = {
    #             "_xsrf": get_xsrf(),
    #             "email": account,
    #             "password": password
    #         }

    response_text = session.post("https://www.zhihu.com/signup?next=%2F", headers=header)
    print(response_text.text)
    session.cookies.save()
    pass

zhihu_login("18782902568", "admin123")
# get_index()
#is_login()

# get_captcha()