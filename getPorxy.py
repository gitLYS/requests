import requests
from lxml import etree
import os
import random
from bs4 import BeautifulSoup
from get_headers import GetHeaders

class GetProxy():
    def getproxy(self):
        urls=['http://www.xicidaili.com/nn/',
              'http://www.xicidaili.com/nt/',
              'http://www.xicidaili.com/wn/',
              'http://www.xicidaili.com/wt/']

        header=GetHeaders().getHeaders()
        proxies=[]

        for url in urls:
            print(url)

            s = requests.get(url,headers=header)
            html=etree.HTML(s.text)
            ips=html.xpath('//*[@class="country"][1]/following-sibling::td[1]/text()')
            ports=html.xpath('//*[@class="country"][1]/following-sibling::td[2]/text()')

            for i in range(0,int(len(ips)/2)):
                proxies.append(ips[i]+':'+ports[i])
            # with open('/home/lys/project/requests project/代理ip.txt','a') as f:
            #     for i in proxies:
            #         f.writelines(i+'\n')

        print('ok!')


        #测试
        proxies_useful=[]
        for proxy in proxies:
            proxy_http={
                        'http':"http://"+proxy,
                        'https':"http://"+proxy,
                    }
            title=''
            try:
                s=requests.get('http://music.163.com/',headers=header,proxies=proxy_http,timeout=2)
                title=BeautifulSoup(s.text,'lxml').h1.text
                if title.strip()=='网易云音乐':
                    print('correct:'+proxy)
                    proxies_useful.append(proxy)
            except Exception as e:
                print('error:'+proxy)
                continue

        print('Test Done!!')


        # #return an enable proxy
        # with open('/home/lys/project/requests project/代理ip.txt','r') as f:
        #     proxies=f.readlines()
        proxy_list=[]
        for proxy in proxies_useful:
            proxy_http={
                        'http':"http://"+proxy,
                        'https':"http://"+proxy,
                    }
            proxy_list.append(proxy_http)

        return proxy_list


    # def getPorxyFromTxt(self):
    #     header=GetHeaders().getHeaders()
    #
    #     with open('/home/lys/project/requests project/代理ip.txt','r') as f:
    #         proxies=f.readlines()
    #
    #     proxie_list=[]
    #     # proxy=random.choice(proxies).strip()
    #     for proxy in proxies:
    #         proxy_http={
    #                     'http':"http://"+proxy,
    #                     'https':"http://"+proxy,
    #                 }
    #         proxie_list.append(proxy_http)
    #     return proxie_list




# GetIp().get_proxy()
