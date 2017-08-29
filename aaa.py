import requests
from lxml import etree

headers={
         "Accept": "*/*",
         "Accept-Encoding": "gzip, deflate, br",
         "Accept-Language": "zh-CN,zh;q=0.8",
         "Connection": "keep-alive",
         "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
         'Host':'www.zhihu.com',
         'Origin':'https://www.zhihu.com',
         'Referer':'https://www.zhihu.com/',
         'X-Requested-With':'XMLHttpRequest',
        }

xrf=requests.get('https://www.zhihu.com/#signin',headers=headers)
xrf=etree.HTML(xrf.text)
xrf=xrf.xpath('/html/body/div[1]/div/div[2]/div[2]/form/input/@value')[0]
headers={
         "Accept": "application/json, text/javascript, */*; q=0.01",
         "Accept-Encoding": "gzip, deflate, br",
         "Accept-Language": "zh-CN,zh;q=0.8",
         "Connection": "keep-alive",
         "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
         'Host':'www.zhihu.com',
         'Origin':'https://www.zhihu.com',
         'Referer':'https://www.zhihu.com/',
         'X-Requested-With':'XMLHttpRequest',
         'X-Xsrftoken':xrf
        }

params={'_xsrf':xrf,'password':'lymiss5201314','captcha_type':'cn','email':'836193873@qq.com'}
r=requests.post('https://www.zhihu.com/login/email',headers=headers,data=params)
print(r.text)

