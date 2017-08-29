import requests
import random
from bs4 import BeautifulSoup
from get_headers import GetHeaders
from lxml import etree
import re
import json
import chardet

headers=GetHeaders().getHeaders()
urls=[
# 'https://www.lagou.com/jobs/2971577.html',
# 'https://www.lagou.com/jobs/2755354.html',
# 'https://www.lagou.com/jobs/2748573.html',
# 'https://www.lagou.com/jobs/3221413.html',
# 'https://www.lagou.com/jobs/2790466.html',
# 'https://www.lagou.com/jobs/3180429.html',
# 'https://www.lagou.com/jobs/1956944.html',
# 'https://www.lagou.com/jobs/3053859.html',
# 'https://www.lagou.com/jobs/3514245.html',
# 'https://www.lagou.com/jobs/3088024.html',
# 'https://www.lagou.com/jobs/3056633.html',
    'https://www.lagou.com/jobs/1962657.html',
]

for url in urls:
    s=requests.get(url,headers=headers)
    html=etree.HTML(s.text)
    data_dict={}
    #company
    data_dict['company']=html.xpath('/html/body/div[2]/div/div[1]/div/div[1]/text()')[0].strip()

    #job_name
    data_dict['job_name']=html.xpath('/html/body/div[2]/div/div[1]/div/span/text()')[0].strip()

    #salary
    data_dict['salary']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[1]/text()')[0].strip()

    #city
    data_dict['city']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()')[0].replace('/','').strip()

    #experience
    data_dict['experience']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()')[0].replace('/','').strip()

    #educetion
    data_dict['educetion']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[4]/text()')[0].replace('/','').strip()

    #job_type
    data_dict['job_type']=html.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[5]/text()')[0].replace('/','').strip()

    #attractive_title
    data_dict['attractive_title']=html.xpath('//*[@id="job_detail"]/dd[1]/span/text()')[0].replace('：','').strip()

    #attractive_content
    data_dict['attractive_content']=html.xpath('//*[@id="job_detail"]/dd[1]/p/text()')[0].strip()

    #description_title
    data_dict['description_title']=html.xpath('//*[@id="job_detail"]/dd[2]/h3/text()')[0].replace('：','').strip()

    #description_content
    data_dict['description_content']=re.sub(r'\\xa\d','',str(html.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')).replace('\', \'','\n').replace('[\'','').replace('\']','')).strip()

    #city_distinct
    data_dict['city_distinct']=str(html.xpath('//*[@id="job_detail"]/dd[3]/div[1]/a/text()')[0:-1]).replace('\', \'','\n').replace('[\'','').replace('\']','').strip()

    #city_detail
    data_dict['city_detail']=html.xpath('//*[@id="job_detail"]/dd[3]/input[3]/@value')[0].strip()

    #city_longitude
    data_dict['city_longitude']=html.xpath('//*[@id="job_detail"]/dd[3]/input[1]/@value')[0].strip()

    #city_latitude
    data_dict['city_latitude']=html.xpath('//*[@id="job_detail"]/dd[3]/input[2]/@value')[0].strip()

    #company_name
    data_dict['company_name']=html.xpath('//*[@id="job_company"]/dt/a/div/h2/text()')[0].strip()

    #field
    data_dict['field']=str(html.xpath('//*[@id="job_company"]/dd/ul/li[1]/text()')).replace('\', \'','\n').replace('[\'','').replace('\']','').replace('\\n','').strip()

    #development_stage
    data_dict['development_stage']=html.xpath('//*[@id="job_company"]/dd/ul/li[2]/text()[2]')[0].strip()

    #company_scale
    data_dict['company_scale']=html.xpath('//*[@id="job_company"]/dd/ul/li[3]/text()[2]')[0].strip()

    #company_page
    # data_dict['company_page']=html.xpath('//*[@id="job_company"]/dd/ul/li[4]/a/@href')[0].strip()
    print(html.xpath('//*[@id="job_company"]/dd/ul/li[4]/a/@href'))
    print(url)
    print(data_dict)
    print('-------------------------------------')
