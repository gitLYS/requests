import requests
from getPorxy import GetProxy
from get_headers import GetHeaders,Urls
from lxml import etree
import re
import json
import os
import time
import random
import settings
from requests.exceptions import RequestException

class LaGou():
    headers=GetHeaders().getHeaders()
    path=settings.path
    urls=Urls.lagouwang_urls

    def getCatUrls(self):
        proxy_list_useful=GetProxy().getproxy()
        proxy_list=[]

        proxy_len=len(proxy_list_useful)
        print(proxy_len)
        #扩展可用代理ip的数量
        proxy_list=proxy_list_useful*10
        print('proxies is ready!')
        for url in self.urls:
            #判断是否是空白页面，默认false
            is_null_page=False
            cat_name=url.split('/')[-2].replace('.','')
            item_urls=[]
            next_page=url
            while True:

                proxy=random.choice(proxy_list)
                try:
                    this_page=next_page
                    response=requests.get(this_page,headers=GetHeaders().getHeaders(),timeout=10,proxies=proxy)
                    html=etree.HTML(response.text)

                    each_jos_urls=html.xpath('//*[@id="s_position_list"]/ul/li/div/div[1]/div/a/@href')
                    next_page=html.xpath('//*[@id="s_position_list"]/div[2]/div/a')[-1].xpath('./@href')[0]
                except RequestException as e:
                    print(e)
                    proxy_list.remove(proxy)
                    if len(proxy_list)<proxy_len:
                        proxy_list_useful=GetProxy().getproxy()
                        proxy_list=list(proxy_list_useful*10)
                        print('proxies is ready!')
                    continue
                except IndexError as e:
                    try:
                        #判断该页面是否是空白页面
                        is_null_page=html.xpath('//*[@id="s_position_list"]/ul/div/div[2]/div/text()')==['暂时没有符合该搜索条件的职位']
                        if is_null_page:
                            break
                    except:
                        pass
                    print(e)
                    proxy_list.remove(proxy)
                    if len(proxy_list)<proxy_len:
                        proxy_list_useful=GetProxy().getproxy()
                        proxy_list=list(proxy_list_useful*3)
                        print('proxies is ready!')
                    continue
                except Exception as e:
                    print(e)
                    continue

                if is_null_page:
                    continue
                for url in each_jos_urls:
                    item_urls.append(url)
                    print(url)
                print(next_page)
                # time.sleep(1)
                if 'www.lagou.com' not in next_page:
                    # with open('/home/lys/project/requests project/item_urls.txt','a') as f:
                    #     for url in item_urls:
                    #         f.writelines(url+'\n')
                    try:
                        os.mkdir(path=self.path+cat_name)
                    except:
                        pass
                    os.chdir(path=self.path+cat_name)
                    LaGou().processItem(item_urls)
                    break


    def processItem(self,urls):
        i=0
        proxy_list_useful=GetProxy().getproxy()
        proxy_len=len(proxy_list_useful)
        proxy_list=proxy_list_useful*10
        print('proxies is ready!')
            #扩展可用代理ip的数量
        while i<len(urls):
            proxy=random.choice(proxy_list)

            try:
                print(urls[i])
                response=requests.get(urls[i],headers=GetHeaders().getHeaders(),proxies=proxy,timeout=5)
                html=etree.HTML(response.text)
                data_dict={}
                #company
                data_dict['company']=html.xpath('/html/body/div[2]/div/div[1]/div/div[1]/text()')[0].strip()

                #job_name
                try:
                    data_dict['job_name']=html.xpath('/html/body/div[2]/div/div[1]/div/span/text()')[0].strip()
                except:
                    data_dict['job_name']=' '

                #salary
                try:
                    data_dict['salary']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[1]/text()')[0].strip()
                except:
                    data_dict['salary']=' '

                #city
                try:
                    data_dict['city']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()')[0].replace('/','').strip()
                except:
                    data_dict['city']=' '

                #experience
                try:
                    data_dict['experience']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()')[0].replace('/','').strip()
                except:
                    data_dict['experience']=' '

                #educetion
                try:
                    data_dict['educetion']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[4]/text()')[0].replace('/','').strip()
                except:
                    data_dict['educetion']=' '

                #job_type
                try:
                    data_dict['job_type']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[5]/text()')[0].replace('/','').strip()
                except:
                    data_dict['job_type']=' '

                #attractive_title
                try:
                    data_dict['attractive_title']=html.xpath('//*[@id="job_detail"]/dd[1]/span/text()')[0].replace('：','').strip()
                except:
                    data_dict['attractive_title']=' '

                #attractive_content
                try:
                    data_dict['attractive_content']=html.xpath('//*[@id="job_detail"]/dd[1]/p/text()')[0].strip()
                except:
                    data_dict['attractive_content']=' '

                #description_title
                try:
                    data_dict['description_title']=html.xpath('//*[@id="job_detail"]/dd[2]/h3/text()')[0].replace('：','').strip()
                except:
                    data_dict['description_title']=' '

                #description_content
                try:
                    data_dict['description_content']=re.sub(r'\\xa\d','',str(html.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')).replace('\', \'','\n').replace('[\'','').replace('\']','')).strip()
                except:
                    data_dict['description_content']=' '

                #city_distinct
                try:
                    data_dict['city_distinct']=str(html.xpath('//*[@id="job_detail"]/dd[3]/div[1]/a/text()')[0:-1]).replace('\', \'','\n').replace('[\'','').replace('\']','').strip()
                except:
                    data_dict['city_distinct']=' '

                #city_detail
                try:
                    data_dict['city_detail']=html.xpath('//*[@id="job_detail"]/dd[3]/input[3]/@value')[0].strip()
                except:
                    data_dict['city_detail']=' '

                #city_longitude
                try:
                    data_dict['city_longitude']=html.xpath('//*[@id="job_detail"]/dd[3]/input[1]/@value')[0].strip()
                except:
                    data_dict['city_longitude']=' '

                #city_latitude
                try:
                    data_dict['city_latitude']=html.xpath('//*[@id="job_detail"]/dd[3]/input[2]/@value')[0].strip()
                except:
                    data_dict['city_latitude']=' '

                #company_name
                try:
                    data_dict['company_name']=html.xpath('//*[@id="job_company"]/dt/a/div/h2/text()')[0].strip()
                except:
                    data_dict['company_name']=' '

                #field
                try:
                    data_dict['field']=str(html.xpath('//*[@id="job_company"]/dd/ul/li[1]/text()')).replace('\', \'','\n').replace('[\'','').replace('\']','').replace('\\n','').strip()
                except:
                    data_dict['field']=' '

                #development_stage
                try:
                    data_dict['development_stage']=html.xpath('//*[@id="job_company"]/dd/ul/li[2]/text()[2]')[0].strip()
                except:
                    data_dict['development_stage']=' '

                #company_scale
                try:
                    data_dict['company_scale']=html.xpath('//*[@id="job_company"]/dd/ul/li[3]/text()[2]')[0].strip()
                except:
                    data_dict['company_scale']=' '

                #company_page
                try:
                    data_dict['company_page']=html.xpath('//*[@id="job_company"]/dd/ul/li[4]/a/@href')[0].strip()
                except:
                    data_dict['company_page']=' '
                #爬取成功后并且读取没有错误后url变成下一个
                data_json=json.dumps(data_dict,ensure_ascii=False)
                with open(str(i)+'.json','w') as f:
                    f.write(data_json)
                i=i+1
                time.sleep(1)
            except RequestException as e:
                print(e)
                proxy_list.remove(proxy)
                if len(proxy_list)<proxy_len:
                        proxy_list_useful=GetProxy().getproxy()
                        proxy_list=list(proxy_list_useful*10)
                        print('proxies is ready!')
                continue
            except IndexError as e:
                print(e)
                proxy_list.remove(proxy)
                if len(proxy_list)<proxy_len:
                    proxy_list_useful=GetProxy().getproxy()
                    proxy_list=list(proxy_list_useful*10)
                    print('proxies is ready!')
                continue
            except Exception as e:
                print(e)
                continue




if __name__ == '__main__':
    LaGou().getCatUrls()




