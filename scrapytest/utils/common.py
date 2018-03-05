#coding:utf-8
__author__ = 'cccccc'
__date__ = '2018/2/10 16:09'
import hashlib
def get_md5(url):
    if isinstance(url,str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == "__main__":
    print(get_md5("http://baidu.com".encode("utf-8")))
